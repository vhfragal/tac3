import pygame
from ..display import display
from ..constants import TILE_SIZE, COLOR_BG
from ..utils import utils
from ..ui.levels import Level
from ..entities.tiles import Tile
from .button import Button
from .scroll import Scroll
from ..constants import *
from .notify import notify


class Grid():
    def __init__(self, level:Level):         
        self.size = (display.size[0]*0.7, display.size[1]*0.8)
        self.x_tiles = int(self.size[0]//TILE_SIZE)
        self.y_tiles = int(self.size[1]//TILE_SIZE)
        # ajuste de grade perfeita
        self.size = (self.x_tiles * TILE_SIZE, self.y_tiles*TILE_SIZE)

        self.image = pygame.Surface(self.size).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect_orig = self.image.get_rect()
        
        self.anchor = pygame.Vector2(0,0)
        self.level = level        
        self.tiles:list[Tile] = []
        self.clicked = False
        
        # Converte e guarda o ID da GPU
        self.texture_id = utils.surface_to_texture(self.image)

        self.clear()
        self.update_tiles()
        self.rect.topleft = (display.size[0]*0.1, display.size[1]*0.1)      

        self.create_collision_tiles() 

        # move buttons      
        self.button_left = Button(icon=ICON_ARROW_GREEN, rotate_icon_dg=180)
        self.button_left.rect.midleft = (0, display.size[1]//2)
        self.button_up = Button(icon=ICON_ARROW_GREEN, rotate_icon_dg=90)
        self.button_up.rect.bottomleft = self.button_left.rect.topright
        self.button_down = Button(icon=ICON_ARROW_GREEN, rotate_icon_dg=270)
        self.button_down.rect.topleft = self.button_left.rect.bottomright        
        self.button_right = Button(icon=ICON_ARROW_GREEN, rotate_icon_dg=0)
        self.button_right.rect.topleft = self.button_up.rect.bottomright

        #scroll bars        
        self.vertical_bar = Scroll((SIZE_SCROLL, self.rect.h))
        self.vertical_bar.rect.topleft = self.rect.topright
        self.horizontal_bar = Scroll((self.rect.w, SIZE_SCROLL))
        self.horizontal_bar.rect.topleft = self.rect.bottomleft

        self.vertical_bar.update_slider_vertical(self.y_tiles, 
                                                 self.anchor, TILE_MAP_LEVELS[self.level.idx][1])
        self.horizontal_bar.update_slider_horizontal(self.x_tiles, 
                                                     self.anchor, TILE_MAP_LEVELS[self.level.idx][0])


    #def change_level(self, level:Level):
    #    self.level = level
        

    def create_collision_tiles(self):
        for lin in range(self.y_tiles):                       
            for col in range(self.x_tiles):     
                s = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
                pos = f"{col},{lin}"                         
                tile = Tile(0, s, pos)
                l = col*TILE_SIZE + self.rect.left
                t = lin*TILE_SIZE + self.rect.top
                tile.rect.topleft = (l, t)
                self.tiles.append(tile)  
                


    def clear(self):
        self.image.fill(COLOR_BG)
        for linha in range(self.y_tiles):
            pygame.draw.line(self.image, "white", (0,linha * TILE_SIZE), (self.size[0], linha * TILE_SIZE))
        for col in range(self.x_tiles):
            pygame.draw.line(self.image, "white", (col * TILE_SIZE, 0), (col * TILE_SIZE, self.size[1]))
        pygame.draw.rect(self.image, "green", self.rect_orig, 5)


    def set_clicked(self):
        self.clicked = True

    def unset_clicked(self):
        self.clicked = False
    
     
    def update(self, dt):  
        for event in notify.get_events():
            anchor_v = event.type == EVENT_ANCHOR_VERTICAL
            anchor_h = event.type == EVENT_ANCHOR_HORIZONTAL
            fill = event.type == EVENT_GRID_FILL

            if anchor_v or anchor_h or fill:
                self.clear()             
                self.update_tiles()
            if anchor_v and event.value == self:                
                self.vertical_bar.update_slider_vertical(self.y_tiles, 
                                                         self.anchor, TILE_MAP_LEVELS[self.level.idx][1])                
            if anchor_h and event.value == self:                
                self.horizontal_bar.update_slider_horizontal(self.x_tiles, 
                                                             self.anchor, TILE_MAP_LEVELS[self.level.idx][0])
            

        self.button_left.update(dt)
        self.button_up.update(dt)
        self.button_down.update(dt)
        self.button_right.update(dt) 

        self.vertical_bar.update(dt)
        self.horizontal_bar.update(dt)

      

    def update_tiles(self):
        for lin in range(self.y_tiles):                       
            for col in range(self.x_tiles):
                c = int(self.anchor.x) + col
                l = int(self.anchor.y) + lin                
                tile = self.level.tiles[l][c]
                if tile:                    
                    l = tile.rect.left - (int(self.anchor.x)*TILE_SIZE)
                    t = tile.rect.top - (int(self.anchor.y)*TILE_SIZE)
                    rect = (l, t, tile.rect.w, tile.rect.h)                    
                    self.image.blit(tile.image, rect)
        self.texture_id = utils.update_texture(self.texture_id, self.image)

   

    def draw(self):
        x,y,w,h = self.rect.x, self.rect.y, self.rect.w, self.rect.h        
        utils.draw_textured_quad(self.texture_id, x,y,w,h) 

        self.button_left.draw()
        self.button_up.draw()
        self.button_down.draw()
        self.button_right.draw()

        self.vertical_bar.draw()
        self.horizontal_bar.draw()
       

