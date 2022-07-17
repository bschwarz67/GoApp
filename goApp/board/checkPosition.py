class Check:

    visited = set()
    visitedThisCheck = set()
    taken = set()

    def __init__(self, position, coordinate, color):
        self.position = position
        self.coordinate = coordinate
        self.color = color

        print('{} {} {}'.format(self.position, self.coordinate, self.color))

    def checkPlayValidity(self):
        print('checking validity')
        self.position2dList = []
        self.position2dList.append(self.position[0:7])
        self.position2dList.append(self.position[7:14])
        self.position2dList.append(self.position[14:21])
        self.position2dList.append(self.position[21:28])
        self.position2dList.append(self.position[28:35])
        self.position2dList.append(self.position[35:42])
        self.position2dList.append(self.position[42:49])

        for x in range(49):
            if "{}{}".format(x // 7, x % 7) not in self.visited and self.position2dList[x // 7][x % 7] != self.color and self.position2dList[x // 7][x % 7] != '0':
                print(self.checkTakes(x // 7, x % 7))
                self.visitedThisCheck.clear()
        
        self.visited.clear()
        
        return

    def checkTakes(self, ycoordinate, xcoordinate):
        print('one check')
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

        if ycoordinate != 5:
            if "{}{}".format(ycoordinate + 1, xcoordinate) not in self.visited:
                if self.position2dList[ycoordinate + 1][xcoordinate] == '0':
                    exposedToLiberties = True
                if self.position2dList[ycoordinate + 1][xcoordinate] != self.color:
                    if self.checkTakes(ycoordinate + 1, xcoordinate) == True:
                        exposedToLiberties = True

        if xcoordinate != 0:
            if "{}{}".format(ycoordinate, xcoordinate - 1) not in self.visited:
                if "{}{}".format(ycoordinate, xcoordinate - 1) not in self.visited:
                    if self.position2dList[ycoordinate][xcoordinate - 1] == '0':
                        exposedToLiberties = True
                    if self.position2dList[ycoordinate][xcoordinate - 1] != self.color:
                        if self.checkTakes(ycoordinate, xcoordinate - 1) == True:
                            exposedToLiberties = True

        if xcoordinate != 5:
            if "{}{}".format(ycoordinate, xcoordinate + 1) not in self.visited:
                if "{}{}".format(ycoordinate, xcoordinate + 1) not in self.visited:
                    if self.position2dList[ycoordinate][xcoordinate + 1] == '0':
                        exposedToLiberties = True
                    if self.position2dList[ycoordinate][xcoordinate + 1] != self.color:
                        if self.checkTakes(ycoordinate, xcoordinate + 1) == True:
                            exposedToLiberties = True


        return exposedToLiberties