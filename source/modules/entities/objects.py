import pygame
from .tiles import Tile


class Sprite(pygame.sprite.Sprite):
    def __init__(self, tile:Tile):
        '''General sprite for all objects
            Starting image and position x,y
        '''
        super().__init__()
        self.tile = tile
        
        self.image:pygame.Surface = tile.image
        #self.mask:pygame.Mask = mask
        
        # return a width and height of an image
        self.size = self.image.get_size()  
        self.rect = tile.rect
      

    def update(self):
        pass

    def draw(self): 
        pass


class FixObj(Sprite):
    def __init__(self, tile:Tile):
        super().__init__(tile)
                
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0], 1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0], 1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1, self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1, self.rect.bottomright[1] - self.rect.topright[1]))

    def update(self):
        pass