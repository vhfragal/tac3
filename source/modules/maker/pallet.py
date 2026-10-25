import pygame
from ..display import display
from ..constants import *
from ..utils import utils
from ..entities.tiles import TileMap, Tile
from .notify import notify
from .scroll import Scroll


class Pallet():
    def __init__(self, tilemap:TileMap):         
        self.size = (display.size[0]*0.15, display.size[1]*0.8)
        self.x_tiles = int(self.size[0]//TILE_SIZE)
        self.y_tiles = int(self.size[1]//TILE_SIZE)
        # ajuste de grade perfeita
        self.size = (self.x_tiles * TILE_SIZE, self.y_tiles*TILE_SIZE)

        self.image = pygame.Surface(self.size).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect_orig = self.image.get_rect()
        
        self.anchor = pygame.Vector2(0,0)        
        self.tilemap = tilemap   
        self.tilemap.create_tile_matrix(self.x_tiles) 
                        
        # Converte e guarda o ID da GPU
        self.texture_id = utils.surface_to_texture(self.image)

        self.clear()
        self.update_tiles()
        self.rect.topright = (display.size[0]*1.0-SIZE_SCROLL, display.size[1]*0.1)

        self.tiles:list[Tile] = []  # tiles to check collision
        self.create_collision_tiles()         

        # set first tile as default
        self.select:Tile = self.tilemap.tiles[0][0]
        self.select_pos = (0,0)
        self.update_select()
         

        #scroll bars        
        self.vertical_bar = Scroll((SIZE_SCROLL, self.rect.h))
        self.vertical_bar.rect.topleft = self.rect.topright
        #self.horizontal_bar = Scroll((self.rect.w, SIZE_SCROLL))
        #self.horizontal_bar.rect.topleft = self.rect.bottomleft

        self.vertical_bar.update_slider_vertical(self.y_tiles, self.anchor, TILE_MAP_PALLET)
        #self.horizontal_bar.update_slider_horizontal(self.x_tiles, self.anchor, TILE)


    def create_collision_tiles(self):
        for lin in range(self.y_tiles):                       
            for col in range(self.x_tiles):     
                s = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
                pos = f"{col},{lin}"                         
                tile = Tile(0, s, pos)
                l = col*TILE_SIZE + self.rect.left
                t = lin*TILE_SIZE + self.rect.top
                tile.rect.topleft = (l, t)
                #print(tile.rect)
                self.tiles.append(tile)  

 

    def clear(self):
        self.image.fill("black")
        for linha in range(self.y_tiles):
            pygame.draw.line(self.image, "white", (0,linha * TILE_SIZE), (self.size[0], linha * TILE_SIZE))
        for col in range(self.x_tiles):
            pygame.draw.line(self.image, "white", (col * TILE_SIZE, 0), (col * TILE_SIZE, self.size[1]))
        pygame.draw.rect(self.image, "blue", self.rect_orig, 5)

     
    def update(self, dt): 
        for event in notify.get_events():
            anchor_v = event.type == EVENT_ANCHOR_VERTICAL
            select = event.type == EVENT_PALLET_SELECT
            if (anchor_v or select) and event.value == self:
                self.clear()             
                self.update_tiles()
                self.update_select()
            
            if anchor_v and event.value == self:                                
                self.vertical_bar.update_slider_vertical(self.y_tiles, self.anchor, TILE_MAP_PALLET)

        self.vertical_bar.update(dt)
        #self.horizontal_bar.update(dt)
        
               
    def update_select(self):
        lin, col = self.select_pos 
        self.select = self.tilemap.tiles[lin][col]      
        tile = self.select               
        if tile:
            x,y,w,h = tile.rect      
            y -= int(self.anchor.y) * TILE_SIZE
            pygame.draw.rect(self.image, "gold", (x,y,w,h), 5)   
            #pygame.draw.rect(self.image, "gold", tile.rect, 5)     
        self.texture_id = utils.update_texture(self.texture_id, self.image)
              

    def update_tiles(self):
        for lin in range(self.y_tiles):                       
            for col in range(self.x_tiles):
                c = int(self.anchor.x) + col
                l = int(self.anchor.y) + lin                        
                tile = self.tilemap.tiles[l][c]
                if tile:                    
                    l = tile.rect.left - (int(self.anchor.x)*TILE_SIZE)
                    t = tile.rect.top - (int(self.anchor.y)*TILE_SIZE)
                    rect = (l, t, tile.rect.w, tile.rect.h)                    
                    self.image.blit(tile.image, rect)
        self.texture_id = utils.update_texture(self.texture_id, self.image)

         

    def draw(self):
        #x,y,w,h = self.rect.x, self.rect.y, self.rect.w, self.rect.h        
        utils.draw_textured_quad(self.texture_id, *self.rect) 

        self.vertical_bar.draw()
        #self.horizontal_bar.draw()
       

