import pygame

TITLE = "Game TAC3"
FPS = 60
SCALE = 2
GRAVITY = 1200

COLOR_TEXT = pygame.Color("#087204")
COLOR_BG = pygame.Color("#5C94FC")
COLOR_SCROLL = pygame.Color("#0E6303")

SIZE_PLAYER = (60*SCALE, 100*SCALE)
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


