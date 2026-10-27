import pygame
from ..display import display
from ..constants import *
from ..utils import utils
from .grid import Grid
from .pallet import Pallet
from .notify import notify

class Info():
    def __init__(self, grid:Grid, pallet:Pallet):   
        self.delay:int = 1
        self.counter = self.delay  
        self.grid = grid   
        self.pallet = pallet      
        
        # Initialize a font (system default or custom font file)
        #self.font = pygame.font.SysFont("Arial", 14)
        fps_text = f"FPS:{str(int(display.clock.get_fps()))}"
        self.font = pygame.font.Font("assets/fonts/Call of Ops Duty II.otf", 150)        
        self.image_fps = self.font.render(fps_text, True, pygame.Color("green"))       
        self.rect_fps = self.image_fps.get_rect()
        # Converte e guarda o ID da GPU
        self.texture_id_fps = utils.surface_to_texture(self.image_fps)


        grid_text = f"({grid.x_tiles},{grid.y_tiles})"
        self.font2 = pygame.font.Font("assets/fonts/Call of Ops Duty II.otf", 130)
        self.image_grid_tiles = self.font2.render(grid_text, True, pygame.Color("green")) 
        self.image_grid_tiles = pygame.transform.smoothscale_by(self.image_grid_tiles, 1/4)
        self.rect_grid_tiles = self.image_grid_tiles.get_rect()
        # Converte e guarda o ID da GPU
        self.texture_id_grid_tiles = utils.surface_to_texture(self.image_grid_tiles)


        grid_text = f"X,Y:{TILE_MAP_LEVELS[self.grid.level.idx]}"        
        self.image_lv1_tiles = self.font2.render(grid_text, True, pygame.Color("green")) 
        self.image_lv1_tiles = pygame.transform.smoothscale_by(self.image_lv1_tiles, 1/4)
        self.rect_lv1_tiles = self.image_lv1_tiles.get_rect()
        # Converte e guarda o ID da GPU
        self.texture_id_lv1_tiles = utils.surface_to_texture(self.image_lv1_tiles)

        grid_text = f"{grid.anchor}"       
        self.image_anchor_tiles = self.font2.render(grid_text, True, pygame.Color("green")) 
        self.image_anchor_tiles = pygame.transform.smoothscale_by(self.image_anchor_tiles, 1/4)
        self.rect_anchor_tiles = self.image_anchor_tiles.get_rect()
        # Converte e guarda o ID da GPU
        self.texture_id_anchor_tiles = utils.surface_to_texture(self.image_anchor_tiles)

        # pallet
        pallet_text = f"{pallet.anchor}"       
        self.image_anchor_tiles_pallet = self.font2.render(pallet_text, True, pygame.Color("green")) 
        self.image_anchor_tiles_pallet = pygame.transform.smoothscale_by(self.image_anchor_tiles_pallet, 1/4)
        self.rect_anchor_tiles_pallet = self.image_anchor_tiles_pallet.get_rect()
        # Converte e guarda o ID da GPU
        self.texture_id_anchor_tiles_pallet = utils.surface_to_texture(self.image_anchor_tiles_pallet)

        pallet_text = f"({pallet.x_tiles},{pallet.y_tiles})"        
        self.image_pallet_tiles = self.font2.render(pallet_text, True, pygame.Color("green")) 
        self.image_pallet_tiles = pygame.transform.smoothscale_by(self.image_pallet_tiles, 1/4)
        self.rect_pallet_tiles = self.image_pallet_tiles.get_rect()
        # Converte e guarda o ID da GPU
        self.texture_id_pallet_tiles = utils.surface_to_texture(self.image_pallet_tiles)

        # level
        text = f"LEVEL {self.grid.level.idx}"       
        self.image_level = self.font2.render(text, True, pygame.Color("green")) 
        self.image_level = pygame.transform.smoothscale_by(self.image_level, 1/4)
        self.rect_level = self.image_level.get_rect()
        # Converte e guarda o ID da GPU
        self.texture_id_level = utils.surface_to_texture(self.image_level)



    def update(self, dt:float):        
        self.counter += dt 
        if self.counter >= self.delay:  
            fps = display.clock.get_fps()
            valor = int(min(fps,10000))
            fps_text = f"FPS:{valor}"
            # Render the text (Text, Anti-aliasing, Color)
            self.image_fps = self.font.render(fps_text, True, pygame.Color("green"))
            self.image_fps = pygame.transform.smoothscale_by(self.image_fps, 1/4) 
            self.rect_fps = self.image_fps.get_rect()    
            self.texture_id_fps = utils.update_texture(self.texture_id_fps, self.image_fps)    
            self.counter = 0

        for event in notify.get_events():
            anchor_v = event.type == EVENT_ANCHOR_VERTICAL
            anchor_h = event.type == EVENT_ANCHOR_HORIZONTAL
            
            if (anchor_v or anchor_h) and event.value == self.grid:
                # atualizar anchor - condicao de evento                
                grid_text = f"{self.grid.anchor}"                
                self.image_anchor_tiles = self.font2.render(grid_text, True, pygame.Color("green")) 
                self.image_anchor_tiles = pygame.transform.smoothscale_by(self.image_anchor_tiles, 1/4)
                self.rect_anchor_tiles = self.image_anchor_tiles.get_rect()
                # Converte e guarda o ID da GPU
                self.texture_id_anchor_tiles = utils.update_texture(self.texture_id_anchor_tiles, self.image_anchor_tiles)

            if (anchor_v) and event.value == self.pallet:
                # atualizar anchor - condicao de evento                
                pallet_text = f"{self.pallet.anchor}"                
                self.image_anchor_tiles_pallet = self.font2.render(pallet_text, True, pygame.Color("green")) 
                self.image_anchor_tiles_pallet = pygame.transform.smoothscale_by(self.image_anchor_tiles_pallet, 1/4)
                self.rect_anchor_tiles_pallet = self.image_anchor_tiles_pallet.get_rect()
                # Converte e guarda o ID da GPU
                self.texture_id_anchor_tiles_pallet = utils.update_texture(self.texture_id_anchor_tiles_pallet,
                                                                            self.image_anchor_tiles_pallet)

       

    def draw(self):
        # topleft position
        x,y,w,h = 0, 0, self.rect_fps.w, self.rect_fps.h        
        utils.draw_textured_quad(self.texture_id_fps, x,y,w,h) 

        x,y,w,h = 0, self.rect_fps.h, self.rect_lv1_tiles.w, self.rect_lv1_tiles.h        
        utils.draw_textured_quad(self.texture_id_lv1_tiles, x,y,w,h)

        x,y,w,h = 0, self.rect_fps.h + self.rect_lv1_tiles.h, self.rect_grid_tiles.w, self.rect_grid_tiles.h        
        utils.draw_textured_quad(self.texture_id_grid_tiles, x,y,w,h)

        x,y = 0, self.rect_fps.h + self.rect_grid_tiles.h + self.rect_lv1_tiles.h 
        w,h = self.rect_anchor_tiles.w, self.rect_anchor_tiles.h        
        utils.draw_textured_quad(self.texture_id_anchor_tiles, x,y,w,h)

        # pallet
        x,y = display.size[0] - self.rect_anchor_tiles_pallet.w-5, 0
        w,h = self.rect_pallet_tiles.w, self.rect_pallet_tiles.h        
        utils.draw_textured_quad(self.texture_id_pallet_tiles, x,y,w,h)

        x,y = display.size[0] - self.rect_anchor_tiles_pallet.w-5, self.rect_pallet_tiles.h
        w,h = self.rect_anchor_tiles_pallet.w, self.rect_anchor_tiles_pallet.h        
        utils.draw_textured_quad(self.texture_id_anchor_tiles_pallet, x,y,w,h)


        # level
        x,y = display.size[0] - self.rect_level.w -5, display.size[1] - self.rect_level.h
        w,h = self.rect_level.w, self.rect_level.h        
        utils.draw_textured_quad(self.texture_id_level, x,y,w,h)

        
