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

        self.ground:list[FixObj] = []
        #self.ground = pygame.sprite.Group() 
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
                        self.ground.append(FixObj(tile))
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


        
        raw_tiles:list[pygame.Rect] = []
        for ground in self.ground:
            raw_tiles.append(ground.rect)

        # Merge adjacent static tiles ONCE at level load
        self.colliders = self.build_merged_colliders(raw_tiles)


    def build_merged_colliders(self, tile_rects:list[pygame.Rect]):
        """Merges adjacent static tiles horizontally, then vertically,
        eliminating all internal floor, wall, and ceiling seams.
        """
        #if not tile_rects:
        #    return []

        # 1. Merge horizontally
        sorted_x = sorted(tile_rects, key=lambda r: (r.y, r.x))
        horiz_merged = [sorted_x[0].copy()]
        for current in sorted_x[1:]:
            last = horiz_merged[-1]
            if (
                last.right == current.left
                and last.y == current.y
                and last.height == current.height
            ):
                last.width += current.width
            else:
                horiz_merged.append(current.copy())

        # 2. Merge vertically (creates larger solid wall/platform blocks)
        sorted_y = sorted(horiz_merged, key=lambda r: (r.x, r.width, r.y))
        final_merged = [sorted_y[0].copy()]
        for current in sorted_y[1:]:
            last = final_merged[-1]
            if (
                last.bottom == current.top
                and last.x == current.x
                and last.width == current.width
            ):
                last.height += current.height
            else:
                final_merged.append(current.copy())

        return final_merged



    def update(self, dt:float):
        pass
        for ground in self.ground:
            pass


    def draw(self):        
        x,y,w,h = 0,0, self.rect.w, self.rect.h              
        utils.draw_textured_quad(self.texture_id, x,y,w,h)

        
        #for ground in self.ground:
        #    ground.draw()