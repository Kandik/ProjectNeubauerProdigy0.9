from tetromino import Tetromino

import math
import cv2
import numpy as np
import pyautogui
import json


class CV:
    """
    Class covering CV attributes and functions
    """


    """
        Anchor points and dimensions
    """
    # Anchor point in the top left corner of the field
    fieldAP = [826, 247]

    # Field of view for the algorithm (for cropping)
    fieldFOV = [567, 660]

    # Size of the playing field in boxes (width*height)
    gridSize = [10, 20]

    # Dimensions of one box (width*height)
    boxSize = [33, 33]

    # Next piece box anchor point (in top left corner)
    npAP = [394, 259]

    # Observed field
    observedField = [False] * 200

    # Monitor - for showing what CV sees
    monitor = None
    
    # Distinguishers for "NEXT" box
    distinguishers = None

    def loadJSON(self, path):
        """
        Function to load JSON with "NEXT" pixel distinguishers
        :param path: Path to the JSON file
        :return: None
        """
        try:
            f = open(path)
            self.distinguishers = json.load(f)
            f.close()
        except:
            pass

    def getScreenData(self, show):
        """
        Function to get the data from the screen
        :param show: Boolean to toggle the CV window showing on the screen
        :return: Boolean to toggle action (doStuff), current field state,
        held piece, piece in the "NEXT" box
        """

        # Taking a screenshot
        screenshot = pyautogui.screenshot()

        # Converting the screenshot from RGB to BGR
        image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Cropping the image
        fov = image[self.fieldAP[1]:self.fieldAP[1] + self.fieldFOV[1],
              self.fieldAP[0]:self.fieldAP[0] + self.fieldFOV[0]]

        # Turning the image to grayscale
        grayScale = cv2.cvtColor(fov, cv2.COLOR_BGR2GRAY)

        if show:
            # Initializing the window if "show" is True
            self.monitor = grayScale.copy()

        # Calling CV functions
        fieldState = self.getFieldState(show, grayScale)
        heldPiece = self.getHeldPiece(show)
        nextPiece = self.getNextPiece(show, grayScale)

        if show:
            # Showing the CV window
            cv2.imshow("ComputerVision", self.monitor)
            # Setting the CV window to be always on top
            cv2.setWindowProperty("ComputerVision", cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(1)

        # Setting doStuff as True if any box in first two rows is taken
        doStuff = any(fieldState[0:20])

        # Deleting first two rows
        # (falling Tetromino can be there which can confuse the AI)
        for x in range(20):
            fieldState[x] = False

        return doStuff, fieldState, heldPiece, nextPiece


    def getFieldState(self, show, grayScale):
        """
        Function to get the current state of the field
        :param show: Boolean to toggle writing on the CV window
        :param grayScale: Grayscale image anchored on the field
        :return: Current field state (Boolean array with length of 200)
        """

        self.observedField = [False] * 200

        # Iterating over the field
        for x in range(200):

            # Calculating the position on the field
            # (column and row)
            xpos = x%10
            ypos = math.floor(x/10)

            # Calculating analysis points
            xap = int((xpos * self.boxSize[0]) + self.boxSize[0]/2)
            yap = int((ypos * self.boxSize[1]) + self.boxSize[1]/2)

            # Analysing the analysis point
            if grayScale[yap, xap] > 0:
                # If the grayscale value is higher than 0, mark the box as taken
                self.observedField[x] = True
                if show:
                    i = -1
            elif show:
                i = 1

            if show:
                # Drawing the square on the CV window if "show" is True
                cv2.rectangle(self.monitor, (xpos * self.boxSize[0], ypos * self.boxSize[1]),
                              ((xpos+1) * self.boxSize[0], (ypos+1) * self.boxSize[1]), (255, 225, 255), i)

        return self.observedField


    def getNextPiece(self, show, grayScale):
        """
        Function to get what is the piece in the "NEXT" box
        :param show: Boolean to toggle writing on the CV window
        :param grayScale: Grayscale image anchored on the field
        :return: ID of the Tetromino in the "NEXT" box
        or None if the distinguishers are not loaded
        """
        if self.distinguishers is not None:
            found = 6

            # Iterating over IDs in distinguishers
            for id in self.distinguishers:

                # Found Boolean
                foundB = True
    
                for distinguisher in self.distinguishers[id]:
                    if grayScale[self.npAP[1] + distinguisher[1], self.npAP[0] + distinguisher[0]] == 0:
                        # Turning Found Boolean False and breaking if any
                        # of the distingusiher pixels is black
                        foundB = False
                        break
    
                if foundB:
                    found = int(id)
                    break
    
            if show:
                # Writing the found piece letter to the monitor if "show" is True
                string = self.getIDString(found)
                cv2.putText(self.monitor, string, (400, 380), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)

            return found

    def getHeldPiece(self, show):
        """
        Function to get the currently held piece from first two rows of observed field
        :param show: Boolean to toggle writing on the CV window
        :return: Held Tetromino ID or None if no Tetromino is found
        """
        
        found = None

        # Iterating over Tetrominos
        for x in range(7):
            t = Tetromino(x)

            # Getting Tetromino anchor point
            ap = t.TAP%10

            # Checking if anchor point and every connected box is active
            if (self.observedField[ap] and self.observedField[ap + t.connected[0]] and
                    self.observedField[ap + t.connected[1]] and self.observedField[ap + t.connected[2]]):
                found = x
                break

        if show:
            # Writing the found piece letter next to the field if "show" is True
            string = self.getIDString(found)
            cv2.putText(self.monitor, string, (350, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2, cv2.LINE_AA)

        return found

    def getIDString(self, id):
        """
        Function to get the letter of the Tetromino from ID
        :param id: ID of the Tetromino
        :return: Letter of the Tetromino
        """
        if id == 0:
            return "I"
        elif id == 1:
            return "J"
        elif id == 2:
            return "L"
        elif id == 3:
            return "S"
        elif id == 4:
            return "T"
        elif id == 5:
            return "Z"
        elif id == 6:
            return "O"
        else:
            return "None"
