from tetromino import Tetromino

import time
import numpy as np
import math
import cv2
import json


colorful = False
dimensions = [700, 500]
gridsize = [35, 34]

algdebug = False


class GameManager:
    """
    Class with main game mechanics and functions
    """
    gp = [0, 0]

    gamePanel = np.zeros(shape=[dimensions[0], dimensions[1], 3], dtype=np.uint8)

    t = Tetromino(0)


    placed = False

    badness = 0

    burn = False

    holdPiece = -1

    # fieldQuality
    fieldHeight = 0
    holesN = 0
    blocksAboveHole = 0

    columnHeight = [0] * 10
    bumpiness = 0
    linesCleared = 0

    # fieldQualityMultipliers
    heightM = 50
    holeM = 200
    blocksAboveHoleM = 20
    bumpinessM = 50

    staticGrid = [False] * 200
    dynamicGrid = [False] * 200
    holes = [False] * 200

    def resetGP(self):
        """
        Function to reset game panel drawing pointer position
        :return: None
        """
        self.gp = [0, 0]

    def loadJSON(self, path):
        """
        Function to load JSON containing multipliers to the game manager
        :param path: Path to the JSON file
        :return: None
        """
        try:
            f = open(path)
            data = json.load(f)
            f.close()

            self.heightM = data["height"]
            self.holeM = data["holes"]
            self.blocksAboveHoleM = data["blocksAboveHoles"]
            self.bumpinessM = data["bumpiness"]

        except:
            pass

    def addTetromino(self, t=None):
        """
        Function to add Tetromino to the field
        :param t: Tetromino class to add
        :return: None
        """
        if t is not None:
            self.t = t

        self.dynamicGrid = [False] * 200

        self.dynamicGrid[self.t.TAP] = True

        for x in range(3):
            self.dynamicGrid[self.t.TAP + self.t.connected[x]] = True

    def checkPlaced(self):
        """
        Function to check whether the Tetromino in the field is placed
        :return: None
        """
        self.placed = False

        for x in range(200):
            if self.dynamicGrid[x] and x > 189:
                self.placed = True
            elif self.dynamicGrid[x] and self.staticGrid[x + 10]:
                self.placed = True

        if self.placed:
            self.staticGrid[self.t.TAP] = True
            for x in range(3):
                self.staticGrid[self.t.TAP + self.t.connected[x]] = True

    def hardDrop(self):
        """
        Function to hard drop a Tetromino (push it down until it lands)
        :return: None
        """
        while not self.placed:
            self.t.TAP += 10
            self.addTetromino()
            self.checkPlaced()

    def getGridHeight(self):
        """
        Function to calculate the height of the field
        :return: None
        """
        x = 0
        while not self.staticGrid[x] and x < 199:
            x += 1

        self.fieldHeight = math.ceil((199 - x) / 10)

    def findHoles(self):
        """
        Function to find holes in the field
        :return: None
        """
        self.holesN = 0
        self.blocksAboveHole = 0

        for x in range(20, 200):
            if (self.staticGrid[x - 10] or self.holes[x - 10]) and not (self.staticGrid[x] or self.dynamicGrid[x]):
                self.holes[x] = True
                self.holesN += 1
            else:
                self.holes[x] = False

            if self.holes[x] and self.staticGrid[x - 10]:
                y = x
                while y > 0:
                    if self.staticGrid[y]:
                        self.blocksAboveHole += 1
                    y -= 10

    def getBumpiness(self):
        """
        Function to calculate bumpiness of the field (mean difference in column height)
        :return: None
        """
        done = False
        column = 0
        x = 0
        while not done:
            if self.staticGrid[x]:
                self.columnHeight[column] = math.ceil((199 - x) / 10)
                column += 1
                if column == 10:
                    done = True
                x = column
            else:
                x += 10

            if x > 199:
                self.columnHeight[column] = 0
                column += 1
                if column == 10:
                    done = True
                x = column

        self.bumpiness = 0

        for y in range(1, 10):
            self.bumpiness += abs(self.columnHeight[y] - self.columnHeight[y - 1])

    def clearField(self):
        """
        Function to clear field - remove rows that are full
        :return: None
        """
        full = 0
        for x in range(200):

            if self.staticGrid[x]:
                full += 1

            if (x + 1) % 10 == 0:

                if full == 10:
                    y = x - 10
                    self.linesCleared += 1
                    while y > 0:
                        self.staticGrid[y + 10] = self.staticGrid[y]
                        self.staticGrid[y] = False
                        y -= 1
                else:
                    full = 0

    def analyseField(self):
        """
        Function to analyse the field and update "badness" - reverse fitness
        :return: None
        """
        self.clearField()

        self.getGridHeight()
        self.findHoles()
        self.getBumpiness()

        self.badness = 0
        self.badness += self.heightM * self.fieldHeight
        self.badness += self.holeM * self.holesN
        self.badness += self.blocksAboveHoleM * self.blocksAboveHole
        self.badness += self.bumpinessM * self.bumpiness

        for x in range(10):
            if self.staticGrid[x]:
                self.staticGrid = [False] * 200
                self.linesCleared = 0

    def printBadness(self):
        """
        Function to print "badness" - reverse fitness and field analysis to the console
        :return: None
        """
        print("\n\nBadness:\nHeight: ", self.heightM * self.fieldHeight)
        print("Holes: ", self.holeM * self.holesN)
        print("Blocks above holes: ", self.blocksAboveHoleM * self.blocksAboveHole)
        print("Bumpiness: ", self.bumpinessM * self.bumpiness)
        print("Total: ", self.badness)

    def testMove(self, t):
        """
        Function to test a move on the field with a given Tetromino
        :param t: Tetromino class with set state and position
        :return: Badness if the move was made
        """
        linesave = self.linesCleared
        cachegrid = self.staticGrid.copy()
        self.addTetromino(t)
        self.hardDrop()
        self.analyseField()

        if algdebug:
            self.redrawGP()
            self.resetGP()
            time.sleep(0.01)

        thisbadness = self.badness

        self.staticGrid = cachegrid.copy()
        self.linesCleared = linesave
        self.placed = False

        self.analyseField()

        return thisbadness

    def redrawGP(self):
        """
        Function to redraw the game panel
        :return: None
        """

        self.gamePanel = np.zeros(shape=[dimensions[0], dimensions[1], 3], dtype=np.uint8)

        for x in range(200):

            color = (255, 225, 255)
            if colorful and self.holes[x]:
                color = (0, 0, 255)
                i = -1


            elif self.staticGrid[x] or self.dynamicGrid[x]:
                i = -1

            else:
                i = 1

            cv2.rectangle(self.gamePanel, (self.gp[0], self.gp[1]), (self.gp[0] + gridsize[0], self.gp[1] + gridsize[1]), color, i)

            self.gp[0] += gridsize[0] + 1

            if (x + 1) % 10 == 0:
                self.gp[1] += gridsize[1] + 1
                self.gp[0] = 0

            cv2.putText(self.gamePanel, str(self.linesCleared), (400, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Game Panel", self.gamePanel)
        cv2.waitKey(1)
