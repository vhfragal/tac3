import pygame
from ..utils import utils
from ..display import display
from ..constants import *
from .notify import notify

class Button():
    def __init__(self,                  
                 text:str = "",
                 message:str = "",
                 icon: str = "",
                 rotate_icon_dg: int = 0):        
        w, h = 0, SIZE_ICON[1]
        self.over = False
        self.clicked = False
        self.working = True
        self.message = message
        self.font = pygame.font.Font("assets/fonts/Call of Ops Duty II.otf", 200)
        
        if text != "":                    
            self.text_surf = self.font.render(text, True, pygame.Color("green")) 
            self.text_surf = pygame.transform.smoothscale_by(self.text_surf, 1/4)
            self.text_rect = self.text_surf.get_rect()
            w += self.text_rect.w
        if icon != "":
            self.icon_surf = utils.load_image(icon)
            self.icon_surf = pygame.transform.smoothscale(self.icon_surf, SIZE_ICON)
            if rotate_icon_dg != 0:
                self.icon_surf = pygame.transform.rotate(self.icon_surf, rotate_icon_dg)
            self.icon_rect = self.icon_surf.get_rect()
            w += self.icon_rect.w

        # adaptative button size       
        self.image = pygame.Surface((w,h)).convert_alpha()
        self.rect = self.image.get_rect()
        #pygame.draw.rect(self.image, "green", self.rect, 1)

        self.clicked_image = pygame.Surface((w,h)).convert_alpha()
        
        if text != "":
            self.text_rect.midright = (w, h//2)
            self.image.blit(self.text_surf, self.text_rect)
            self.text_rect.midright = (w+1, (h//2)+1)
            self.clicked_image.blit(self.text_surf, self.text_rect)
        if icon != "":
            self.image.blit(self.icon_surf, self.icon_rect)
            self.icon_rect.topleft = (1,1)  # deslocamento efeito 
            self.clicked_image.blit(self.icon_surf, self.icon_rect)

        self.clicked_image = pygame.transform.hsl(self.clicked_image, 270, 0.2, 0.2)
        # overlay mouse        
        self.over_image = pygame.transform.hsl(self.image, 270, 0.2, 0.2)

        # invalid icon 
        self.invalid_image = pygame.transform.grayscale(self.image)
    
        # Converte e guarda o ID da GPU
        self.texture_id = utils.surface_to_texture(self.image)
        self.texture_id_over = utils.surface_to_texture(self.over_image)
        self.texture_id_invalid = utils.surface_to_texture(self.invalid_image)
        self.texture_id_clicked = utils.surface_to_texture(self.clicked_image)

        # message 
        self.delay:int = 2
        self.counter = 0

        if message != "": 
            self.text_surf_message = self.font.render(message, True, pygame.Color("green")) 
            self.text_surf_message = pygame.transform.smoothscale_by(self.text_surf_message, 1/4)
            self.text_rect_message = self.text_surf_message.get_rect()
            self.text_rect_message.midbottom = (display.size[0]//2, display.size[1])
            
            # Converte e guarda o ID da GPU
            self.texture_id_message = utils.surface_to_texture(self.text_surf_message)


    def set_working(self, working:bool):
        self.working = working

    def set_clicked(self):
        self.clicked = True

    def unset_clicked(self):
        self.clicked = False

    
    def update(self, dt:float):
        self.over = False         

        for event in notify.get_events():
            message = event.type == EVENT_BUTTON_MESSAGE
            over = event.type == EVENT_BUTTON_OVER
           
            if message:
                if event.value == self: self.counter = self.delay
                else: self.counter = 0
            if over and event.value == self:
                self.over = True
           

        if self.counter > 0:
            self.counter -= dt


    def draw(self):    
        if not self.working:
            utils.draw_textured_quad(self.texture_id_invalid, *self.rect) 
        else:
            if self.clicked: utils.draw_textured_quad(self.texture_id_clicked, *self.rect) 
            elif self.over: utils.draw_textured_quad(self.texture_id_over, *self.rect) 
            else: utils.draw_textured_quad(self.texture_id, *self.rect) 

        if self.counter > 0:              
            utils.draw_textured_quad(self.texture_id_message, *self.text_rect_message)