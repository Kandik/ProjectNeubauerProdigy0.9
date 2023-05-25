from gamemanager import GameManager
from tetromino import Tetromino

import math


class AI:
    """
    Class covering AI attributes and functions
    """

    # Game manager used by AI
    g = GameManager()

    def loadJSON(self, path):
        """
        Function to load JSON with multipliers into the AI
        :param path: Path to the JSON file
        :return: None
        """
        # Sending the JSON to the game manager
        self.g.loadJSON(path)

    def getMBmove(self, field, tID):
        """
        Function to get minimum badness move for the current field state and held piece
        :param field: Current field state (Boolean array with length of 200)
        :param tID: Held Tetromino ID
        :return: Minimum badness achieved, minimum badness state (rotation),
        minimum badness Tetromino anchor point
        """

        # Creating a Tetromino with given tID
        t = Tetromino(tID)

        # Copying the field state into AI game manager
        self.g.staticGrid = field.copy()

        # Return variables
        MBTAP = 0
        MBState = 0
        minBadness = math.inf

        # Iterating over states (rotations)
        for x in range(t.states):
            # Setting the state of the Tetromino
            t.setState(x)

            # Iterating for every possible position for the current
            # piece and its current rotation
            for y in range(t.hitbox[0], 10 - t.hitbox[1]):
                # Setting the state of the Tetromino
                t.setState(x)

                # Setting the position of the Tetromino
                t.TAP = y

                # Calculating the reverse fitness for
                # the current configuration
                thisbadness = self.g.testMove(t)

                # If the reverse fitness is lower
                # than currently lowest found
                if thisbadness < minBadness:
                    # Saving the variables
                    MBState = x
                    MBTAP = y
                    minBadness = thisbadness

                # Resetting the Tetromino
                t = Tetromino(t.id)

        return minBadness, MBState, MBTAP
