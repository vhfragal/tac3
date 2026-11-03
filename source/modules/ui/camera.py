import pygame
from ..utils import utils
from .cenario import Cenario
from ..display import display
from ..events.notify import notify
from ..constants import *

class Camera():
    def __init__(self, cenario:Cenario):
        self.cenario = cenario
        
        self.rect = pygame.Rect(0, 0, display.w, display.h)
        self.rect.bottomleft = self.cenario.rect.bottomleft     

        self.image = pygame.Surface(display.size, pygame.SRCALPHA)
        self.image.blit(cenario.image, area=self.rect)
        self.texture_id = utils.surface_to_texture(self.image)

    def update(self, dt:float):
        for event in notify.get_events():           
            camera = event.type == EVENT_CAMERA

            if camera:                
                self.image.fill("black")
                self.image.blit(self.cenario.image, area=self.rect)
                self.texture_id = utils.update_texture(self.texture_id, self.image)
                
   
    def draw(self):
        x,y,w,h = 0,0, self.rect.w, self.rect.h              
        utils.draw_textured_quad(self.texture_id, x,y,w,h)