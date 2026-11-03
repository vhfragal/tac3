import pygame
from ..constants import *
from ..utils import utils
from ..ui.levels import Level

class Cenario():
    def __init__(self, level:Level):
        self.level = level
        w = TILE_MAP_LEVELS[level.idx][0] * TILE_SIZE
        h = TILE_MAP_LEVELS[level.idx][1] * TILE_SIZE
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)        
        
        self.rect = self.image.get_rect()

        for line in level.tiles:
            for tile in line:
                if tile: self.image.blit(tile.image, tile.rect)

        #pygame.image.save(self.image, "test.png")

        # Converte e guarda o ID da GPU
        self.texture_id = utils.surface_to_texture(self.image) 

      