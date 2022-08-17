from home.models import Player
from board.models import Game

class Check:

    visited = set()
    visitedThisCheck = set()
    taken = set()

    def __init__(self, game, player, coordinate, color):
        self.game = game
        self.player = player
        self.coordinate = coordinate
        self.color = color

    def checkPlay(self):
        resultList = []
        checkKoFlag = True

        self.possiblePosition = self.game.piecePositions
        if self.color == '1':
            self.possiblePosition = self.possiblePosition[:self.coordinate] + '1' + self.possiblePosition[self.coordinate + 1:]
            if self.player == self.game.blackPlayer:
                self.color = '2'
                checkKoFlag = False
        else:
            self.possiblePosition = self.possiblePosition[:self.coordinate] + '2' + self.possiblePosition[self.coordinate + 1:]
            if self.player == self.game.whitePlayer:
                self.color = '1'
                checkKoFlag = False
        


        self.position2dList = []
        self.position2dList.append(self.possiblePosition[0:7])
        self.position2dList.append(self.possiblePosition[7:14])
        self.position2dList.append(self.possiblePosition[14:21])
        self.position2dList.append(self.possiblePosition[21:28])
        self.position2dList.append(self.possiblePosition[28:35])
        self.position2dList.append(self.possiblePosition[35:42])
        self.position2dList.append(self.possiblePosition[42:49])


        for x in range(49):
            if "{}{}".format(x // 7, x % 7) not in self.visited and self.position2dList[x // 7][x % 7] != self.color and self.position2dList[x // 7][x % 7] != '0':
                result = self.checkTakes(x // 7, x % 7)
                if result == False: 
                    for x in self.visitedThisCheck:
                        self.taken.add(x)
                self.visitedThisCheck.clear()
        
        
        if checkKoFlag == True:
            if self.checkKo() == True:
                resultList.append(False)
                self.visited.clear()
                self.taken.clear()
                return resultList

            else:
                resultList.append(True)
                for x in self.taken:
                    resultList.append(x)
                self.visited.clear()
                self.taken.clear()
                return resultList
        else:
            resultList.append(True)
            for x in self.taken:
                resultList.append(x)
            self.visited.clear()
            self.taken.clear()
            return resultList
    
    
    def checkKo(self):
        for x in self.taken:
            coordinate = 7 * int(list(x)[0]) + int(list(x)[1])
            self.possiblePosition = self.possiblePosition[:coordinate] + '0' + self.possiblePosition[coordinate + 1:]
        if self.possiblePosition != self.player.previousPiecePositions:
            return False
        else:
            return True
        
    def finalizeNewMove(self):
        
        if self.game.movingPlayer == self.game.whitePlayer:
            self.game.movingPlayer = self.game.blackPlayer         
            self.game.save()
        else: 
            self.game.movingPlayer = self.game.whitePlayer         
            self.game.save()

        self.game.piecePositions = self.possiblePosition
        self.game.save()
        self.possiblePosition = ""

        self.player.previousPiecePositions = self.game.piecePositions
        self.player.save()

    def checkTakes(self, yCoordinate, xCoordinate):
        self.visited.add("{}{}".format(yCoordinate, xCoordinate))
        self.visitedThisCheck.add("{}{}".format(yCoordinate, xCoordinate))

        exposedToLiberties = False

        if yCoordinate != 0:
            if "{}{}".format(yCoordinate - 1, xCoordinate) not in self.visited:
                if self.position2dList[yCoordinate - 1][xCoordinate] == '0':
                    exposedToLiberties = True
                if self.position2dList[yCoordinate - 1][xCoordinate] != self.color:
                    if self.checkTakes(yCoordinate - 1, xCoordinate) == True:
                        exposedToLiberties = True

        if yCoordinate != 6:
            if "{}{}".format(yCoordinate + 1, xCoordinate) not in self.visited:
                if self.position2dList[yCoordinate + 1][xCoordinate] == '0':
                    exposedToLiberties = True
                if self.position2dList[yCoordinate + 1][xCoordinate] != self.color:
                    if self.checkTakes(yCoordinate + 1, xCoordinate) == True:
                        exposedToLiberties = True

        if xCoordinate != 0:
            if "{}{}".format(yCoordinate, xCoordinate - 1) not in self.visited:
                if self.position2dList[yCoordinate][xCoordinate - 1] == '0':
                    exposedToLiberties = True
                if self.position2dList[yCoordinate][xCoordinate - 1] != self.color:
                    if self.checkTakes(yCoordinate, xCoordinate - 1) == True:
                        exposedToLiberties = True

        if xCoordinate != 6:
            if "{}{}".format(yCoordinate, xCoordinate + 1) not in self.visited:
                if self.position2dList[yCoordinate][xCoordinate + 1] == '0':
                    exposedToLiberties = True
                if self.position2dList[yCoordinate][xCoordinate + 1] != self.color:
                    if self.checkTakes(yCoordinate, xCoordinate + 1) == True:
                        exposedToLiberties = True

            
        return exposedToLiberties