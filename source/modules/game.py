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
import math
from OpenGL.GL import *


class Game():
    def __init__(self):
        self.running = False
        self.level:Level = None
        self.cenario:Cenario = None
        self.camera:Camera = None
        

    def init_assets(self): 
        self.panel = Panel()

        self.font_size = 48 
        self.font = pygame.font.Font(None, self.font_size)

        # load tiles
        self.tile_map = TileMap()        
        self.tile_map.load_sprite_maps()
        self.load_level(1)  
        #self.player.set_map_size(TILE_MAP_LEVELS[1])

        # player
        self.MAP_WIDTH = TILE_MAP_LEVELS[1][0] * TILE_SIZE
        self.MAP_HEIGHT = TILE_MAP_LEVELS[1][1] * TILE_SIZE
        self.camera_init_pos = (self.MAP_WIDTH*0.01, self.MAP_HEIGHT*0.9)
        #self.camera.set_camera(*pos)
        self.player = Player(self.MAP_WIDTH, self.MAP_HEIGHT, self.camera_init_pos)
        self.bg = Background(self.MAP_WIDTH, self.MAP_HEIGHT)   
               
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
                       
        


    def load_level(self, idx:int):
        self.level = Level(idx, self.tile_map)
        self.cenario = Cenario(self.level)
        #self.camera = Camera(self.cenario)
        self.camera = Camera(display.w, display.h)


    def start(self):        
        self.camera.set_camera(0, self.camera_init_pos[1])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                
        glLoadIdentity()
        glTranslatef(-int(self.camera.x), -int(self.camera.y), 0)

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
        self.player.update(dt)
        self.panel.update(dt)

        self.camera.update(dt, self.player)


    def draw(self):      
        # Render Phase
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        
        glLoadIdentity()

        # Save the base matrix state
        glPushMatrix()
        # Apply camera translations (moves the world relative to camera)
        glTranslatef(-int(self.camera.x), -int(self.camera.y), 0)
        
        self.bg.draw()
        self.cenario.draw()        
        self.player.draw()

        # Restore matrix state to clear the translation for UI elements
        glPopMatrix()

        self.panel.draw()


game = Game() 