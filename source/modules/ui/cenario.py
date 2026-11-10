import pygame
from ..constants import *
from ..utils import utils
from ..ui.levels import Level
from ..entities.objects import FixObj
from ..display import display

class Cenario():
    def __init__(self, level:Level):
        self.level = level
        self.w = TILE_MAP_LEVELS[level.idx][0] * TILE_SIZE
        self.h = TILE_MAP_LEVELS[level.idx][1] * TILE_SIZE
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)        
        
        self.rect = self.image.get_rect()
        
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
        
        for line in level.tiles:
            for tile in line:
                if tile:
                    if tile.desc.startswith("background"):
                        self.image.blit(tile.image, tile.rect)
                    elif tile.desc.startswith(TILE_TYPE_GROUND):
                        self.ground.add(FixObj(tile))
                        self.image.blit(tile.image, tile.rect)
                        pass

        borda_mapa = pygame.Rect(0, 0, self.w, self.h)
        pygame.draw.rect(self.image, (50, 50, 50), borda_mapa, 4) # Retângulo vazado mostrando a borda do mundo
        

        #pygame.image.save(self.image, "test.png")
        

        # aux lists
        self.loot = pygame.sprite.Group()
        self.loot.add(self.items)
        self.loot.add(self.coins)
        self.solid = pygame.sprite.Group()
        self.solid.add(self.ground)
        self.solid.add(self.items)
        self.hazard = pygame.sprite.Group()
        self.hazard.add(self.enemies) 

        # Converte e guarda o ID da GPU
        self.texture_id = utils.surface_to_texture(self.image) 


    def update(self, dt:float):
        pass


    def draw(self):
        #borda_mapa = pygame.Rect(0 - int(offset_camera.x), 0 - int(offset_camera.y),
        #                            self.MAP_WIDTH, self.MAP_HEIGHT)
        
        #x, y = 0 - int(offset_camera.x), 0 - int(offset_camera.y)
        #w, h = self.w, self.h

        x,y,w,h = 0,0, self.rect.w, self.rect.h              
        utils.draw_textured_quad(self.texture_id, x,y,w,h)
