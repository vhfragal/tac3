import pygame
import sys
from .entities.player import Player
from .ui.background import Background
from .display import display
from .entities.tiles import TileMap
from .ui.levels import Level
from .ui.panel import Panel
from .config.sounds import sounds


class Game():
    def __init__(self):
        self.running = False
        self.level_idx = 1

    def init_assets(self): 
        self.bg = Background(*display.size)        
        self.player = Player(display.size[0]*0.2, display.size[1]*0.6)
        self.panel = Panel()
        
        # load tiles
        self.tile_map = TileMap()        
        self.tile_map.load_sprite_maps()
        self.level = Level(self.level_idx, self.tile_map)
        
        self.bg.add_cenario(self.level.tiles)

        #self.load_config()

              

    def start(self):
        self.running = True 
        sounds.play_music()


    def stop(self):
        self.running = False
        pygame.quit()
        sys.exit()



game = Game() 