import array


class Tetromino:
    """
    Class for attributes of Tetromino (Tetris piece)
    """

    # ID of Tetromino
    id = 0

    # State (rotation) of Tetromino
    state = 0

    # Number of possible states for the Tetromino
    states = 0

    # Hitboxes from left and right for the Tetromino
    hitbox = [0, 0]

    # Tetromino anchor point
    TAP = 15

    # Default Tetromino anchor point
    defTAP = 15

    # Array of relative positions of connected pieces
    connected = array.array('i', [0, 0, 0])

    def setState(self, state):
        """
        Function to set the state (rotation) of the Tetromino
        :param state: Number of state (rotation) of the Tetromino
        :return: None
        """

        # Long bar
        if self.id == 0:

            if state == 0:
                self.connected = [-2, -1, 1]
                self.hitbox = [2, 1]

            elif state == 1:
                self.connected = [-10, 10, 20]
                self.hitbox = [0, 0]

            else:
                print("Invalid state for long bar")

        # J piece
        elif self.id == 1:

            if state == 0:
                self.connected = [-1, 1, 11]
                self.hitbox = [1, 1]

            elif state == 1:
                self.connected = [-9, -10, 10]
                self.hitbox = [0, 1]

            elif state == 2:
                self.connected = [-11, -1, 1]
                self.hitbox = [1, 1]

            elif state == 3:
                self.connected = [-10, 10, 9]
                self.hitbox = [1, 0]

            else:
                print("Invalid state for J piece")

        # L piece
        elif self.id == 2:

            if state == 0:
                self.connected = [9, -1, 1]
                self.hitbox = [1, 1]

            elif state == 1:
                self.connected = [-10, 10, 11]
                self.hitbox = [0, 1]

            elif state == 2:
                self.connected = [-9, 1, -1]
                self.hitbox = [1, 1]

            elif state == 3:
                self.connected = [-11, -10, 10]
                self.hitbox = [1, 0]

            else:
                print("Invalid state for L piece")

        # S piece
        elif self.id == 3:

            if state == 0:
                self.connected = [ 9, 10, 1]
                self.hitbox = [1, 1]

            elif state == 1:
                self.connected = [-10, 1, 11]
                self.hitbox = [0, 1]

            else:
                print("Invalid state for S piece")

        # T piece
        elif self.id == 4:

            if state == 0:
                self.connected = [-1, 10, 1]
                self.hitbox = [1, 1]

            elif state == 1:
                self.connected = [-10, 1, 10]
                self.hitbox = [0, 1]

            elif state == 2:
                self.connected = [-1, -10, 1]
                self.hitbox = [1, 1]

            elif state == 3:
                self.connected = [-1, -10, 10]
                self.hitbox = [1, 0]

            else:
                print("Invalid state for T piece")

        # Z piece
        elif self.id == 5:

            if state == 0:
                self.connected = [-1, 10, 11]
                self.hitbox = [1, 1]

            elif state == 1:
                self.connected = [-9, 1, 10]
                self.hitbox = [0, 1]

            else:
                print("Invalid state for Z piece")

        # Square
        elif self.id == 6:

            self.connected = [-1, 9, 10]
            self.hitbox = [1, 0]

            if state != 0:
                print("U tryna rotate a square, lol")

    def __init__(self, id):
        """
        Init function for the Tetromino class
        :param id: ID of the Tetromino
        """

        # Val checking the ID
        if id < 0 or id > 6:
            print("Invalid ID for Tetromino")
        else:
            self.id = id

            # Setting number of possible states
            if id == 1 or id == 2 or id == 4:
                self.states = 4

            elif id == 6:
                self.states = 1

            else:
                self.states = 2

            # Setting the default rotation
            self.setState(0)
