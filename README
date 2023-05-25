University of Eastern Finland
Artificial Intelligence 2022
"Stefan's group"


██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗
██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝
██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║
██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║
██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝

███╗   ██╗███████╗██╗   ██╗██████╗  █████╗ ██╗   ██╗███████╗██████╗
████╗  ██║██╔════╝██║   ██║██╔══██╗██╔══██╗██║   ██║██╔════╝██╔══██╗
██╔██╗ ██║█████╗  ██║   ██║██████╔╝███████║██║   ██║█████╗  ██████╔╝
██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██╔══██║██║   ██║██╔══╝  ██╔══██╗
██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║╚██████╔╝███████╗██║  ██║
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝

██████╗ ██████╗  ██████╗ ██████╗ ██╗ ██████╗██╗   ██╗
██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║██╔════╝╚██╗ ██╔╝
██████╔╝██████╔╝██║   ██║██║  ██║██║██║  ███╗╚████╔╝
██╔═══╝ ██╔══██╗██║   ██║██║  ██║██║██║   ██║ ╚██╔╝
██║     ██║  ██║╚██████╔╝██████╔╝██║╚██████╔╝  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝   ╚═╝


+--------------+
| Team members |
+--------------+

Štefan Kando - lead developer, team leader
Quazi Shahidul Islam - pair programmer, documentation
Samina Yasmin - documentation



+----------+
| Abstract |
+----------+

In our group, we found interest in artificial intelligence playing games.
We see the idea of a machine playing a game meant for a human as fascinating.
For this project, we have decided to make an artificial intelligence for
one of the best-selling games in the world - Tetris.

Jonas Neubauer was a seven-time champion in Classic Tetris World Championship (CTWC).
He died from sudden cardiac arrest in 2021 at the age of 39.
This project is meant to be a tribute to him.

Although at the current state, the AI is not half as good as him,
but with further development, it has the potential to get close to his skill.

This project focuses on the NES version of Tetris, released in 1984.
This version is one of the most popular and recognizable among the Tetris
community and has been selected as the version on which the CTWC is played
yearly even now, after nearly 40 years.

This application is capable of reading the data from an NES emulator running
NES Tetris, figure out an "optimal" placement and send the output as
keystrokes to the emulator.



+------------+
| How to use |
+------------+

To run the application in this state, you need a Windows 10 machine
with a 1920x1080 screen on a 100% scale (not enlarged).
You also need a Mesen NES emulator: https://www.mesen.ca/
running NES Tetris: https://www.emulatorgames.net/roms/nintendo/tetris/

The controls need to be as follows:
D-pad - WASD
B - J
A - L
Start - I

Run the emulator fullscreen windowed, and get to the level selection.
Scroll with D-pad to level 5 and run main.py.
You have 3 seconds to return to the emulator.
After 3 seconds, the algorithm will battle to its last breath for the world record.

Demo video: https://www.youtube.com/watch?v=VEWS5IWhJ1E



+-------------------+
| How does it work? |
+-------------------+

CV:
In this state, the CV works by analysing exact pixels.
It has a defined anchor point in the top left corner of the playing field,
from where it analyses the centre of each box in a 10x20 grid.
If the box is empty, the centre of an empty box will have a grayscale value of 0 exactly.
Any grayscale value higher than 0 is marked as a taken box.

CV algorithm also analyses the first two rows to determine what Tetromino (piece) is being held.
It also analyses the "NEXT" piece box and determines what piece goes next.
"NEXT" box analysis works based on distinguisher pixels.
Each piece has 1-3 distinguisher pixels. If all are active for one piece,
the algorithm is certain that this piece is in the "NEXT" box.
In this state, this does not have other use than telling the algorithm
what piece it holds if it fails to find out from the first two rows (not catching the exact frame).
If the first two rows have any boxes active in them, it tells the AI to "do stuff".


AI:
The artificial intelligence algorithm takes the current field
state and the currently held piece as input.
Then it tries every possible position for the piece by brute force,
taking both rotation and position into account. For every position,
it calculates the reverse fitness and this way it finds out the rotation
and position with the lowest reverse fitness (called "badness" in the code).

The reversed fitness is calculated by these factors:
    - height of the field
    - N of holes in the field
    - N of blocks above holes
    - "bumpiness" of the field - mean of difference between heights of each column

Each factor has its own multiplier, which was only set manually at the moment.
A genetic algorithm can be implemented to improve these multipliers,
but we did not manage to make it in the given time. :(
The algorithm then rotates the piece as needed. Every Tetromino has its own anchor point,
so the algorithm can calculate how much it has to move the piece to get it to the desired position.
It then sends the amount of keystrokes to the emulator and waits for the next input from the CV.



+----------------+
| Used libraries |
+----------------+
- opencv-python (cv2) - for computer vision
- pyautogui - for making a screenshot
- win32api, win32con - for output functions

- json - for loading and writing to json files
- random (for generating random pieces for debug)

- array
- math
- time
- numpy



+-------+
| Files |
+-------+

main.py
    - Main file, run this script to run the algorithm
    - Check and edit parameters in this file
train.py
    - File where the genetic algorithm would have been implemented :(

gamemanager.py
    - File containing GameManager class with main
    game mechanics and functions implemented
tetromino.py
    - File containing Tetromino class, with attributes and functions
    regarding a Tetromino (Tetris piece)
ai.py
    - File containing AI class and functions
cv.py
    - File containing CV class and functions
output.py
    - File containing output (keystroke) functions

distinguishers.json
    - File containing pixel distinguishers for the "NEXT" box
    - Keys are Tetromino IDs, content is the distinguisher pixel
    coordinates ([x,y])
multipliers.json
    - File containing reverse fitness multipliers
    - Keys are reverse fitness factors, values are the multipliers
    - Used for loading the multipliers to the AI, would be used
    to save them during training
