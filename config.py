# COLOURS (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
K_LIGHTGREY = (180, 180, 180)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (250, 200, 0)
BGCOLOUR = DARKGREY

# Game settings
WIDTH = 650
HEIGHT = 900
FPS = 60
TITLE = "PyWordle"

# Coefficient for determining how long the error text is shown at full opacity
ERROR_TEXT_FPS_DUR_COEF = 1.5

TILESIZE = 70
GAPSIZE = 10

K_TILESIZE = 50
K_GAPSIZE = 8

NUM_COLS = 5
NUM_ROWS = 6

# Padding margins for the 6x5 array of tiles for user to enter letters
# Set to centre in x and slightly above centre in y
MARGIN_X = int((WIDTH - (NUM_COLS * (TILESIZE + GAPSIZE))) / 2)
MARGIN_Y = int((HEIGHT - (NUM_ROWS * (TILESIZE + GAPSIZE))) / 2) - 50

# Keyboard tile layout x positions
K_MARGIN_X = [int((WIDTH - (10 * (K_TILESIZE + K_GAPSIZE))) / 2),
              int((WIDTH - (9 * (K_TILESIZE + K_GAPSIZE))) / 2),
              int((WIDTH - (7 * (K_TILESIZE + K_GAPSIZE))) / 2)]

# y position of top of QWERTY keyboard
K_Y_OFFSET = 680

# Parameters for row shaking animation
ROW_MOVE_AMOUNT = 6
ROW_MOVE_STEP = 3