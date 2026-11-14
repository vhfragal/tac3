'''import pygame
from ..utils import utils
from .cenario import Cenario
from ..display import display
from ..events.notify import notify
from ..constants import *'''
from ..entities.player import Player


class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.lerp_factor = 0.05 # Velocidade da fluidez (quanto menor, mais suave/atrasada)

    def update(self, dt:float, player:Player):
        # Centraliza a câmera no jogador
        target_x = player.rect.x + player.rect.w / 2 - self.width / 2
        target_y = player.rect.y + player.rect.h / 2 - self.height / 2

        # LERP (Interpolação Linear)
        self.x += int((target_x - self.x) * self.lerp_factor )
        self.y += int((target_y - self.y) * self.lerp_factor )
        #print(self.x, self.y)
 
        # Limites da câmera no mapa (Clamp)
        if self.x < 0: self.x = 0
        if self.x > player.MAP_WIDTH - self.width: self.x = player.MAP_WIDTH - self.width
        if self.y < 0: self.y = 0
        if self.y > player.MAP_HEIGHT - self.height: self.y = player.MAP_HEIGHT - self.height

    def reset_camera(self):
        self.x = 0
        self.y = 0

    def set_camera(self, x, y):
        self.x = x
        self.y = y



'''class Camera():
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
        utils.draw_textured_quad(self.texture_id, x,y,w,h)'''