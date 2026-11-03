import pygame
from .entities.player import Player
from .ui.background import Background
from .display import display
from .entities.tiles import TileMap
from .ui.levels import Level
from .ui.panel import Panel
from .config.sounds import sounds
from .constants import *
from .ui.cenario import Cenario
from .ui.camera import Camera


class Game():
    def __init__(self):
        self.running = False
        self.level:Level = None
        self.cenario:Cenario = None
        self.camera:Camera = None
        

    def init_assets(self): 
        self.bg = Background(*display.size)        
        self.player = Player(display.size[0]*0.2, display.size[1]*0.6)
        self.panel = Panel()

        self.font_size = 48 
        self.font = pygame.font.Font(None, self.font_size)

        # load tiles
        self.tile_map = TileMap()        
        self.tile_map.load_sprite_maps()
        self.load_level(1)  
        #self.player.set_map_size(TILE_MAP_LEVELS[1])
        

        #game globals  
        self.client = False
        self.server = False
        self.client_socket = None
        self.server_socket = None
        self.multiplayer = False        
        self.buffer_in = []
        self.buffer_in_max = 100
        #self.buffer_out = []
        #self.buffer_out_max = 100
        self.event_p2 = []
        self.size = 30
        self.sep = '|'
        self.client_connected = False

        self.item_id = 1
        self.enemy_id = 1
        self.fire_dmg = 20
        self.mob_aggro_range = 1000
        
        # warp XY        
        self.warp_left = 0
        self.warp_top = 0
        
        # moving background
        self.scroll = 0
        self.tiles = 2

        self.sound_on = False

        self.life_counter = 0
        self.life_delay = 20
        self.life_show = True
                       
        self.ground = pygame.sprite.Group() 
        self.background = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group() 
        #self.fire_pit = pygame.sprite.Group() 
        self.fire_pit = []    
        self.boss_fire_list = pygame.sprite.Group() 
        
        #load map and get boundary limits
        #self.map_size = self.open_map()
        
        # aux lists
        self.loot = pygame.sprite.Group()
        self.loot.add(self.items)
        self.loot.add(self.coins)
        self.solid = pygame.sprite.Group()
        self.solid.add(self.ground)
        self.solid.add(self.items)
        self.hazard = pygame.sprite.Group()
        self.hazard.add(self.enemies) 



    def load_level(self, idx:int):
        self.level = Level(idx, self.tile_map)
        self.cenario = Cenario(self.level)
        self.camera = Camera(self.cenario)


    def start(self):
        self.running = True 
        self.sound_on = True
        sounds.play_new_game_music()


    def restart(self):
        pass


    def stop(self):
        self.running = False
        pygame.mixer.stop()
        pygame.quit()
        #sys.exit()
        exit()


    def update(self, dt):
        self.camera.update(dt)        
        self.player.update(dt)
        self.panel.update(dt)


    def draw(self):        
        self.bg.draw()
        self.camera.draw()
        self.panel.draw()
        self.player.draw()


game = Game() 