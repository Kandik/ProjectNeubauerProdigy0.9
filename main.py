from gamemanager import GameManager  # Game manager with main game mechanics and functions implemented
from tetromino import Tetromino  # Class for a Tetromino (Tetris playing piece)
from cv import CV  # CV implementation
from ai import AI  # Artificial intelligence implementation
from output import startGame, execMove  # Keyboard output functions

import random
import time


"""
    Set True if you want to debug the game panel
    - game panel mechanics, and AI algorithm
    Basically creates a game simulation
"""
gamePanelDebug = False

"""
    Set True if you want to debug the computer vision
    Shows a window showing what the computer sees at the moment
"""
screenshotDebug = False

"""
    Set True if you want the algorithm to play the game
"""
play = True

"""
    Set True if you want to see the CV while the algorithm
    is playing the game
"""
showCV = True


# Delay in seconds from starting the alg to starting the game
gameStartDelay = 3


if gamePanelDebug or play:
    # AI initialization
    ai = AI()
    # Loading multipliers to the AI
    ai.loadJSON("multipliers.json")

if screenshotDebug or play:
    # CV initialization
    cv = CV()
    # Loading distinguishers to CV
    cv.loadJSON("distinguishers.json")

# Variables and init functions for AI playing the game
if play:
    lastNextPiece = 0
    lastDoStuff = False

    # Delaying the start of the game
    time.sleep(gameStartDelay)

    # Sending keystrokes to start the game
    startGame()

# Variables for game panel debug
if gamePanelDebug:
    g = GameManager()
    t = Tetromino(0)


# Main cycle
while True:

    # Game panel debug
    if gamePanelDebug:

        # Generating a random Tetromino
        t = Tetromino(random.randint(0, 6))

        # Resetting game panel
        g.resetGP()
        g.placed = False

        # Fetching minimal badness move
        mbmove = ai.getMBmove(g.staticGrid, t.id)

        # Moving the Tetromino
        t.setState(mbmove[1])
        t.TAP = mbmove[2]

        # Adding and placing the Tetromino
        g.addTetromino(t)
        g.hardDrop()

        # Analysing and outputing field state
        g.analyseField()
        g.printBadness()

        # Redrawing game panel
        g.redrawGP()

    # Screenshot debug
    if screenshotDebug:
        # Calling the function to fetch the screen data and show them on screen
        cv.getScreenData(True)

    # AI playing the game
    if play:

        # Fetching data from the screen
        doStuff, fieldState, heldPiece, nextPiece = cv.getScreenData(showCV)

        # If the algorithm is supposed to do stuff
        if not lastDoStuff and doStuff:

            # Determining the held piece
            if heldPiece is not None:
                thispiece = heldPiece
            else:
                # Getting the piece from previous "NEXT" field
                # if the algorithm failed to determine
                # the held piece
                thispiece = lastNextPiece

            # Determining minimal badness move
            mbmove = ai.getMBmove(fieldState, thispiece)

            # Executing a move with minimal badness
            execMove(mbmove[1], mbmove[2], thispiece)

            # Saving tne "NEXT" piece
            lastNextPiece = nextPiece

        # Help variable so the algorithm does not execute
        # its move twice
        lastDoStuff = doStuff
