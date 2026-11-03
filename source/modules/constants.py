import pygame

TITLE = "Game TAC3"
FPS = 60
SCALE = 2       # clear config file if changed
GRAVITY = 1500
GRAVITY_EXTRA = 4000


COLOR_TEXT = pygame.Color("#087204")
COLOR_BG = pygame.Color("#5C94FC")
COLOR_SCROLL = pygame.Color("#0E6303")
COLOR_MENU_BACKGROUND = (50, 100, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 150, 50)
COLOR_TEXT_1 = WHITE
COLOR_TEXT_2 = ORANGE
COLOR_TEXT_3 = RED

SIZE_PLAYER = (45*SCALE, 75*SCALE)
SIZE_ICON = (40,40)
SIZE_SCROLL = 30

TILE_CROP = 16  # pixels
TILE_SIZE = 32*SCALE  # pixels
TILE_MAP_LEVELS = [
    (0,0),      # level 0 -idx
    (300, 50),  # x,y - col,lin
    (200, 50),
    (100, 300),
]
TILE_MAP_PALLET = 50

FILE_CONFIG = "source/data/config.json"
FILE_MAP_1 = "assets/image/bg-1-1.png"
FILE_MAP_2 = "assets/image/bg-1-1-cutout.png"
FILE_MAP_3 = "assets/image/bg-trees-cutout.png"
FILE_ITEMS_OBJECTS_1 = "assets/image/items-objects.png"
FILE_ITEMS_OBJECTS_2 = "assets/image/blocks.png"
FILE_ITEMS_OBJECTS_3 = "assets/image/full-cutout.png"
FILE_MOBS_1 = "assets/image/mobs-cutout.png"
FILE_PLAYER_1 = "assets/image/player.png"
FILE_SPRITES_PLAYER = "assets/image/sprites3.png"

FILE_LEVELS = [
    "",
    "source/data/lv1.npz", 
    "source/data/lv2.npz",
    "source/data/lv3.npz",
    ]

ICON_LOAD = "assets/image/load.png"
ICON_SAVE = "assets/image/save.png"
ICON_ARROW_BLACK = "assets/image/seta1.png"
ICON_ARROW_GRAY = "assets/image/seta2.png"
ICON_ARROW_GREEN = "assets/image/seta3.png"


EVENT_ANCHOR_VERTICAL:int = 0
EVENT_ANCHOR_HORIZONTAL:int = 1

EVENT_GRID_FILL:int = 100

EVENT_PALLET_SELECT:int = 200

EVENT_BUTTON_SAVE:int = 300
EVENT_BUTTON_MESSAGE:int = 301
EVENT_BUTTON_OVER:int = 302


# events in game
EVENT_CAMERA:int = 400



# menu
MENU_MAIN = ['START GAME', 'MULTIPLAYER', 'OPTIONS', 'EDITOR', 'EXIT']
MENU_MULTIPLAYER = ['HOST', 'JOIN', 'BACK']

