import pygame
from ..utils import utils
from ..constants import TILE_SIZE
from ..constants import *#TILE_CROP, FILE_MAP_1


class Tile():
    def __init__(self,
                 id:int, 
                 surf:pygame.Surface,
                 desc:str,
                 w=TILE_SIZE,
                 h=TILE_SIZE):
        
        self.id = id
        self.image = surf
        self.desc = desc

        if w != TILE_CROP or h != TILE_CROP:            
            self.image = pygame.transform.smoothscale(self.image, (w,h))
        self.rect = self.image.get_rect()

        # Converte e guarda o ID da GPU        
        self.texture_id = utils.surface_to_texture(self.image)


    def get(self):
        return self.id, self.image, self.desc 
         
       
    def draw(self):
        x,y = self.rect.x, self.rect.y
        w,h = self.rect.w, self.rect.h                
        utils.draw_textured_quad(self.texture_id, x,y,w,h)



class TileMap():
    def load_sprite_maps(self):
        self.map_items = utils.load_image(FILE_MAP_1)
        self.map_items2 = utils.load_image(FILE_MAP_2)
        self.map_items3 = utils.load_image(FILE_MAP_3)
        self.map_items_objects1 = utils.load_image(FILE_ITEMS_OBJECTS_1)
        self.map_items_objects2 = utils.load_image(FILE_ITEMS_OBJECTS_2)
        self.map_items_objects3 = utils.load_image(FILE_ITEMS_OBJECTS_3)
        self.map_mobs1 = utils.load_image(FILE_MOBS_1)
                
        #pygame.image.save(self.floor1,"1.png")              
        # object codes
        self.codes = [] 
        i = 0
        
        # collide objects        
        left = [0,0,3235,768,832,448,464,448,464,2192,976,976,992,992,1008,1008]        
        top = [208,176,139,416,368,144,144,160,160,128,384,400,384,400,384,400]
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.objects, self.objects_mask = self.cut_sub_surface(self.map_items2, left, top, w, h)        
        for surf in self.objects:
            self.codes.append((i, surf, f"collide {i}"))
            i += 1

        # objects that not collide - background
        left = [136,152,136,151,456,455,664,680,696,257,272,1568,1584,272,287]        
        top = [16,16,32,32,16,32,160,160,160,160,160,160,160,145,160]
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.back, self.back_mask = self.cut_sub_surface(self.map_items2, left, top, w, h)
        for surf in self.back:
            self.codes.append((i, surf, f"background {i}"))
            i += 1

        # objects that not collide - background2
        left = [208,208,208,208]        
        top = [160,176,192,200]
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.back2, self.back2_mask = self.cut_sub_surface(self.map_items3, left, top, w, h)
        for surf in self.back2:
            self.codes.append((i, surf, f"background {i}"))
            i += 1
        

        # items        
        left = [0,0]
        top = [64,81]
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.items, self.items_mask = self.cut_sub_surface(self.map_items_objects1, left, top, w, h)
        for surf in self.items:
            self.codes.append((i, surf, f"items {i}"))
            i += 1
          
        # fire pit
        left = [96]
        top = [144]
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.pit_fire, self.pit_fire_masks = self.cut_sub_surface(self.map_items_objects1, left, top, w, h)  
        for surf in self.pit_fire:
            self.codes.append((i, surf, f"items {i}"))
            i += 1
          
        #boss fire
        left = [100,100]
        top = [128,137]
        w = [24] * len(left)
        h = [7] * len(left)
        self.boss_fire, self.boss_fire_masks = self.cut_sub_surface(self.map_items_objects1, left, top, w, h)
        self.boss_fire_flip, self.boss_fire_flip_masks = self.get_flipped(self.boss_fire)

                
        # items - coins        
        left = [0,16,32,48]
        top = [81] * len(left)
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.coin, self.coin_mask = self.cut_sub_surface(self.map_items_objects1, left, top, w, h)
        
        
        # items - star        
        left = [0,16,32,48]
        top = [48] * len(left)
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.star, self.star_mask = self.cut_sub_surface(self.map_items_objects1, left, top, w, h)
        
        
        # items - coin out of box
        left = [0,16,32,48]
        top = [96] * len(left)
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.coin_box, self.coin_box_mask = self.cut_sub_surface(self.map_items_objects1, left, top, w, h)
        
        # items - box ?        
        left = [0,16,32,48]
        top = [64,64,64,64]
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.box, self.box_mask = self.cut_sub_surface(self.map_items_objects1, left, top, w, h)
        
        
        # items - dead brick        
        left = [64,64,64]
        top = [0,16,32]
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.ex_brick, self.ex_brick_mask = self.cut_sub_surface(self.map_items_objects1, left, top, w, h)
        
        # items - dead box        
        left = [128]
        top = [112]
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.box_empty, self.box_empty_mask = self.cut_sub_surface(self.map_items_objects2, left, top, w, h)
                       
        # get light dance        
        left = [1609]
        top = [1704]
        w = [74]
        h = [223] 
        self.dance, self.dance_mask = self.cut_sub_surface(self.map_items_objects3, left, top, w, h)
        
        # dead jackson and hit
        left = [419,152,298]
        top = [799,792,792]
        w = [61,33,33]
        h = [43,48,48] 
        self.dead, self.dead_mask = self.cut_sub_surface(self.map_items_objects3, left, top, w, h)
        self.dead_flip, self.dead_flip_masks = self.get_flipped(self.dead)
        
        # attack - fire
        left = [262,297,358]
        top = [1105] * len(left)
        w = [30,56,56]
        h = [32] * len(w) 
        self.fire, self.fire_masks = self.cut_sub_surface(self.map_items_objects3, left, top, w, h)
        self.fire_flip, self.fire_flip_masks = self.get_flipped(self.fire)
        
        # orb                                   # old with all - creating orb
        left = [1081,1126,1167]                 #left = [983,1001,1027,1053,1081,1126,1167]
        top = [509,507,506]                     #top = [513,509,509,509,509,507,506]
        w = [41,37,41]                          #w = [13,22,22,24,41,37,41]
        h = [23,28,28]                          #h = [16,22,23,24,23,28,28] 
        self.orb, self.orb_masks = self.cut_sub_surface(self.map_items_objects3, left, top, w, h)
         
        #enemies - pallete        
        left = [238]
        top = [186] * len(left)
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.enemies, self.enemies_masks = self.cut_sub_surface(self.map_mobs1, left, top, w, h)
        for surf in self.enemies:
            self.codes.append((i, surf, f"enemy {i}"))
            i += 1
        
        #enemies - 1        
        left = [238,257]
        top = [186] * len(left)
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.enemy1, self.enemy1_masks = self.cut_sub_surface(self.map_mobs1, left, top, w, h)
        
        
        #enemy1 dead
        left = [219]
        top = [186] * len(left)
        w = [TILE_CROP] * len(left)
        h = [TILE_CROP] * len(left)
        self.enemy1_dead, self.enemy1_dead_masks = self.cut_sub_surface(self.map_mobs1, left, top, w, h)
        
        # boss
        left = [257,292,327,362]
        top = [367] * len(left)
        w = [TILE_CROP*2] * len(left)
        h = [TILE_CROP*2] * len(left)
        self.boss_flip, self.boss_flip_masks = self.cut_sub_surface(self.map_mobs1, left, top, w, h)
        self.boss, self.boss_masks = self.get_flipped(self.boss_flip)
        for surf in self.boss:
            self.codes.append((i, surf, f"boss {i}"))
            i += 1
            break   # just first




    def create_tile_matrix(self, cols):
        self.tiles:list[list[Tile]] = []
        i = 1
        for lin in range(TILE_MAP_PALLET):
            line = []           
            for col in range(cols):                 
                if i < len(self.codes):
                    obj = Tile(*self.codes[i])
                    x, y = col, lin # 2d position
                    obj.rect.topleft = (x*TILE_SIZE, y*TILE_SIZE)
                    line.append(obj)                
                else: line.append(None) 
                i += 1 
            self.tiles.append(line)


    def get_flipped(self, surfaces:list):
        list = []
        mask_list = []
        for image in surfaces:
            surf = pygame.transform.flip(image, True, False)
            list.append(surf)
            mask = pygame.mask.from_surface(surf)
            mask_list.append(mask)
        return list, mask_list

    
    def cut_sub_surface(self, surface:pygame.Surface, left, top, w, h):        
        list = []
        mask_list = []
        if not (len(left) == len(top) == len(w) == len(h)):
            print('Subsurface empty list!!!')
            return list, mask_list      
        for i in range(len(left)):
            surf = surface.subsurface((left[i],top[i]),(w[i],h[i]))                        
            list.append(surf)
            mask = pygame.mask.from_surface(surf)
            mask_list.append(mask)
        return list, mask_list
    
#tile_map = TileMap()