import pygame
from ..game import game
from ..constants import *
from ..display import display
from ..ui.background import Background
from ..config.sounds import sounds
from OpenGL.GL import *
from ..utils import utils

   
class Basic_menu_all():
    def __init__(self, list: list[str]):        
        # rotating icon
        self.counter = 0        
        pos = [display.size[0]*0.5-200, display.size[1]*0.5]
        self.icon1 = Menu_icon(pos)
        pos = [display.size[0]*0.5+200, display.size[1]*0.5]
        self.icon2 = Menu_icon(pos)
        self.list = list
                
        self.select = 1
        self.select_max = len(list)

        self.bg = Background(*display.size, COLOR_MENU_BACKGROUND)

        # rectangular select
        self.select_image = pygame.Surface((300, game.font_size), pygame.SRCALPHA)
        self.select_rect = self.select_image.get_rect()
        pygame.draw.rect(self.select_image, 'red', self.select_rect, 1)
        self.texture_select = utils.surface_to_texture(self.select_image)

        # create text textures
        pos = display.size
        offset = game.font_size
        c = 0
        self.textures = []
        self.texture_rects = []
        self.font = pygame.font.Font("assets/fonts/Call of Ops Duty II.otf", 130)
        for item in self.list:
            text_surf = self.font.render(item, True, pygame.Color("green")) 
            text_surf = pygame.transform.smoothscale_by(text_surf, 1/4)
            text_rect = text_surf.get_rect()
            text_rect.center = (pos[0]/2),(pos[1]/2)+offset*c
            texture = utils.surface_to_texture(text_surf)
            self.textures.append(texture)
            self.texture_rects.append(text_rect)
            c += 1
        
                
    def run(self):  
        sounds.play_menu_music()
        game.sound_on = True  
        while True:    
            dt = display.game_tick()

            select = self.check_keys()
            if select != 0:
                pygame.mixer.music.stop() 
                return select
            
            self.update(dt)
            self.draw()
         
    
    def update(self, dt):
        self.icon1.update(dt)
        self.icon2.update(dt)
        
            
    def draw(self):
        """Loop de Renderização: Onde desenhamos na tela"""                 
        # Render Phase
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # ordem importa - cada layer por vez - pode organizar
        self.bg.draw()       

        # draw select
        offset = game.font_size
        x = display.size[0]*0.5-150
        y = display.size[1]*0.5-(int(offset/2))+(offset*(self.select-1))        
        w,h = self.select_rect.w, self.select_rect.h        
        utils.draw_textured_quad(self.texture_select, x,y,w,h)

        # draw text
        i = 0
        for texture in self.textures:
            utils.draw_textured_quad(texture, *self.texture_rects[i])
            i += 1

        # draw icons
        self.icon1.draw()
        self.icon2.draw()

        pygame.display.flip()
        # forçar sincronização de hardware CPU e GPU - chamadas assincronas
        #glFinish()

            
    def check_keys(self):
        for evento in pygame.event.get():            
            # Se for um evento QUIT
            if evento.type == pygame.QUIT:
                self.exit()  
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.exit()  
                if evento.key == pygame.K_RETURN:                    
                    return self.select
                if evento.key == pygame.K_DOWN:
                    if self.select < self.select_max:
                        self.select += 1
                        self.icon1.change_pos((self.icon1.getx(),self.icon1.gety()+50))
                        self.icon2.change_pos((self.icon2.getx(),self.icon2.gety()+50))
                if evento.key == pygame.K_UP:
                    if self.select > 1:
                        self.select -= 1
                        self.icon1.change_pos((self.icon1.getx(),self.icon1.gety()-50))
                        self.icon2.change_pos((self.icon2.getx(),self.icon2.gety()-50))
                if evento.key == pygame.K_LEFT:
                    pass
                if evento.key == pygame.K_RIGHT:
                    pass
        return 0
    
   
            
    def exit(self):
        # Termina o programa.        
        pygame.quit()
        exit()
       

 

class Menu_icon():
    def __init__(self,pos:list):
        self.pos = pos
        self.size = (30,30)

        # rectangular select
        self.image = pygame.transform.smoothscale(game.tile_map.box[0], self.size)        
        self.rect = self.image.get_rect(center=self.pos)
        self.texture = utils.surface_to_texture(self.image)
               
        self.orig_image = self.image
        self.angle = 0

    def update(self, dt):
        self.angle += 30 * dt
        
        # rotate
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.texture = utils.update_texture(self.texture, self.image)

           
    def change_pos(self, pos:list):
        self.pos = pos
        self.rect.center = pos
    
    def getx(self):
        return self.pos[0]
    
    def gety(self):
        return self.pos[1]

    def draw(self):        
        utils.draw_textured_quad(self.texture, *self.rect) 
    