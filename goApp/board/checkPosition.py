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

        self.possiblePosition = self.game.piecePositions
        if self.color == '1':
            self.possiblePosition = self.possiblePosition[:self.coordinate] + '1' + self.possiblePosition[self.coordinate + 1:]
        else:
            self.possiblePosition = self.possiblePosition[:self.coordinate] + '2' + self.possiblePosition[self.coordinate + 1:]
        print('possiblePosition before takes: ')
        print(self.possiblePosition[0:7])
        print(self.possiblePosition[7:14])
        print(self.possiblePosition[14:21])
        print(self.possiblePosition[21:28])
        print(self.possiblePosition[28:35])
        print(self.possiblePosition[35:42])
        print(self.possiblePosition[42:49])

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
    
    def checkKo(self):
        for x in self.taken:
            coordinate = 7 * int(list(x)[0]) + int(list(x)[1])
            self.possiblePosition = self.possiblePosition[:coordinate] + '0' + self.possiblePosition[coordinate + 1:]
        print("possiblePosition after takes")
        print(self.possiblePosition[0:7])
        print(self.possiblePosition[7:14])
        print(self.possiblePosition[14:21])
        print(self.possiblePosition[21:28])
        print(self.possiblePosition[28:35])
        print(self.possiblePosition[35:42])
        print(self.possiblePosition[42:49])
        print(self.player.previousPiecePositions)
        if self.possiblePosition != self.player.previousPiecePositions:
            self.game.piecePositions = self.possiblePosition
            self.game.save()
            return False
        else:
            return True
        

    def checkTakes(self, ycoordinate, xcoordinate):
        self.visited.add("{}{}".format(ycoordinate, xcoordinate))
        self.visitedThisCheck.add("{}{}".format(ycoordinate, xcoordinate))

        exposedToLiberties = False

        if ycoordinate != 0:
            if "{}{}".format(ycoordinate - 1, xcoordinate) not in self.visited:
                if self.position2dList[ycoordinate - 1][xcoordinate] == '0':
                    exposedToLiberties = True
                if self.position2dList[ycoordinate - 1][xcoordinate] != self.color:
                    if self.checkTakes(ycoordinate - 1, xcoordinate) == True:
                        exposedToLiberties = True

        if ycoordinate != 6:
            if "{}{}".format(ycoordinate + 1, xcoordinate) not in self.visited:
                if self.position2dList[ycoordinate + 1][xcoordinate] == '0':
                    exposedToLiberties = True
                if self.position2dList[ycoordinate + 1][xcoordinate] != self.color:
                    if self.checkTakes(ycoordinate + 1, xcoordinate) == True:
                        exposedToLiberties = True

        if xcoordinate != 0:
            if "{}{}".format(ycoordinate, xcoordinate - 1) not in self.visited:
                if self.position2dList[ycoordinate][xcoordinate - 1] == '0':
                    exposedToLiberties = True
                if self.position2dList[ycoordinate][xcoordinate - 1] != self.color:
                    if self.checkTakes(ycoordinate, xcoordinate - 1) == True:
                        exposedToLiberties = True

        if xcoordinate != 6:
            if "{}{}".format(ycoordinate, xcoordinate + 1) not in self.visited:
                if self.position2dList[ycoordinate][xcoordinate + 1] == '0':
                    exposedToLiberties = True
                if self.position2dList[ycoordinate][xcoordinate + 1] != self.color:
                    if self.checkTakes(ycoordinate, xcoordinate + 1) == True:
                        exposedToLiberties = True

            
        return exposedToLiberties