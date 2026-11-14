import pygame
from ..constants import *
from ..game import game
from ..events.notify import notify
from ..config.sounds import sounds


def inputs():
    x,y = pygame.mouse.get_pos()    
    
    """Loop de Eventos: Inputs globais do sistema e interrupções"""
    for event in pygame.event.get():
        exit(event)        
        click_buttons(x, y, event)
        check_keys(event)
        
        
    mouse_pressed = pygame.mouse.get_pressed()    
    if mouse_pressed[0]: 
        pass    
    elif mouse_pressed[2]:
        pass
    else: check_over_buttons(x, y)

    check_working_buttons()

   
def check_keys(event:pygame.Event):
    if event.type == pygame.KEYDOWN:        
        if event.key == pygame.K_UP and game.player.on_ground:
            game.player.vel.y = game.player.speed_jump
            game.player.on_ground = False
            sounds.play_sound(sounds.sound_jump, 2)
        
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            if game.player.vel.y < 0: 
                game.player.vel.y *= 0.35

  

def click_buttons(x, y, event:pygame.Event):
    # guards
    if event.type == pygame.MOUSEBUTTONUP: 
        #editor.grid.button_left.unset_clicked()        
        return 
    if event.type != pygame.MOUSEBUTTONDOWN: return 

    #if editor.button_save.rect.collidepoint(x,y):     
    #    editor.button_save.set_clicked()
    
    #if editor.grid.button_left.working:
    #    if editor.grid.button_left.rect.collidepoint(x,y):     
    #        editor.grid.button_left.set_clicked()
    


def hold_buttons(x:int, y:int):
    pass
    #if editor.grid.button_left.working and editor.grid.button_left.clicked:
    #    if editor.grid.button_left.rect.collidepoint(x,y):        
    #        editor.grid.anchor.x -= 1
    #        notify.add_event(EVENT_ANCHOR_HORIZONTAL, editor.grid)
    


def check_over_buttons(x:int, y:int):   
    pass 
    #if editor.button_save.rect.collidepoint(x,y): 
    #    notify.add_event(EVENT_BUTTON_OVER, editor.button_save)
    

def check_working_buttons():
    pass
    #if editor.grid.anchor.x == 0: editor.grid.button_left.set_working(False)
    #else: editor.grid.button_left.set_working(True)

    
def exit(event:pygame.Event):
    if event.type == pygame.QUIT:
        game.running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game.running = False


           