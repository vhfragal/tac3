import pygame
from ..constants import COLOR_BG
from ..utils import utils
#from ..entities.tiles import Tile

class Background():
    def __init__(self, w:int, h:int, color=COLOR_BG):
        self.image = pygame.Surface((w, h))
        self.image.fill(color) 
        
        self.rect = self.image.get_rect()

        # Converte e guarda o ID da GPU
        self.texture_id = utils.surface_to_texture(self.image)        
        

    def draw(self):
        x,y,w,h = self.rect.x, self.rect.y, self.rect.w, self.rect.h        
        utils.draw_textured_quad(self.texture_id, x,y,w,h)
        
#bg = Background()