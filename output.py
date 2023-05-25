from tetromino import Tetromino

import win32api
import win32con
import time


"""
    Output delays in milliseconds
"""
# Delay for input from doStuff
inputDelay = 5/1000

# Delay between pressing and releasing a key
keyPressDelay = 25/1000

# Delay for pressing another key
afterKeyPressDelay = 30/1000

# Delay after starting the game
startGameDelay = 200/1000


# Dictionary with keys
keys = {
    "A": 0x41,
    "D": 0x44,
    "J": 0x4A,
    "L": 0x4C,
    "I": 0x49
}


def startGame():
    """
    Function to start the game (press A + start) and delay a bit
    :return: None
    """
    win32api.keybd_event(keys["L"], win32api.MapVirtualKey(keys["L"], 0), 0, 0)
    time.sleep(keyPressDelay)
    press("I")
    win32api.keybd_event(keys["L"], win32api.MapVirtualKey(keys["L"], 0), win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(startGameDelay)


def execMove(MBState, MBTAP, tID):
    """
    Function to execute a move with held piece
    :param MBState: Desired state of the Tetromino
    :param MBTAP: Desired anchor point position of the Tetromino
    :param tID: ID of the held piece
    :return: None
    """
    time.sleep(inputDelay)

    if MBState == 1:
        press("J")
    elif MBState == 2:
        press("J", presses=2)
    elif MBState == 3:
        press("L")

    t = Tetromino(tID)
    move = MBTAP%10 - t.defTAP%10

    if move > 0:
        press("D", presses=move)
    else:
        press("A", presses=abs(move))


def press(key, presses=1):
    """
    Function to press a key
    :param key: Key to press (refer to dictionary above)
    :param presses: Number of presses
    :return: None
    """
    for _ in range(presses):
        win32api.keybd_event(keys[key], win32api.MapVirtualKey(keys[key], 0), 0, 0)
        time.sleep(keyPressDelay)
        win32api.keybd_event(keys[key], win32api.MapVirtualKey(keys[key], 0), win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(afterKeyPressDelay)
