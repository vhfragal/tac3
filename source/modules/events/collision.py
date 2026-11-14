import pygame
from ..constants import *
from ..game import game


def check_collision():
    #check_collision_x()
    #check_collision_y()
    pass


def check_collision_x():
    for platform in game.cenario.ground:
      if game.player.rect.colliderect(platform.rect):
        # Ignore blocks that are just barely grazing the very bottom of the feet
        if game.player.rect.bottom - platform.rect.top <= 2 and game.player.vel.y >= 0:
          continue
        if game.player.rect.top - platform.rect.bottom <= 2 and game.player.vel.y <= 0:
          continue
        print("go")
        if game.player.vel.x > 0:  # Moving right; hit left side of platform
          game.player.rect.right = platform.rect.left
          print("right")
        elif game.player.vel.x < 0:  # Moving left; hit right side of platform
          game.player.rect.left = platform.rect.right

        # Sync float position with corrected Rect position
        game.player.pos.x = game.player.rect.x

def check_collision_y():
    for platform in game.cenario.ground:
      if game.player.rect.colliderect(platform.rect):
        if game.player.vel.y > 0:  # Falling down; hit top of platform
          game.player.rect.bottom = platform.rect.top
          game.player.vel.y = 0
          game.player.on_ground = True
        elif game.player.vel.y < 0:  # Jumping up; hit bottom of platform
          game.player.rect.top = platform.rect.bottom
          game.player.vel.y = 0

        # Sync float position with corrected Rect position
        game.player.pos.y = game.player.rect.y



def collideXY():
    for g in game.cenario.ground:
        # check AABB - intersection collision
        ch1 = game.player.rect.x < g.rect.x + g.rect.w
        ch2 = game.player.rect.x + game.player.rect.w > g.rect.x 
        ch3 = game.player.rect.y < g.rect.y + g.rect.h
        ch4 = game.player.rect.y + game.player.rect.h > g.rect.y    
        if (ch1 and ch2 and ch3 and ch4):
            '''if game.player.speed_h > 0: 
                game.player.rect.x = g.rect.x - game.player.rect.w
            if game.player.speed_h < 0:
                game.player.rect.x = g.rect.x + g.rect.w'''

            if game.player.speed_v > 0:
                game.player.rect.y = g.rect.y - game.player.rect.h
                game.player.speed_v = 0
                game.player.onground = True
                print("plus")
            if game.player.speed_v < 0:
                game.player.rect.y = g.rect.y + g.rect.h
                game.player.speed_v = 0
                print("minus")

    