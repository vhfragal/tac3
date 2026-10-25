import pygame
from ..constants import *
from ..entities.tiles import Tile
from .editor import editor
from .notify import notify
from .grid import Grid
from .pallet import Pallet

def inputs():
    x,y = pygame.mouse.get_pos()    
    
    """Loop de Eventos: Inputs globais do sistema e interrupções"""
    for event in pygame.event.get():
        exit(event)
        select_tile(x, y, event)  
        save_map(x, y, event)
        load_map(x, y, event)
        click_slider(x, y, event)
        click_buttons(x, y, event)
        click_grid(x, y, event)
        scroll_pallet(event)
        #print(pygame.mouse.get_just_pressed())
        
        
    mouse_pressed = pygame.mouse.get_pressed()
    # preencher tile na grade    
    if mouse_pressed[0]: 
        fill_tile(x, y)        
        hold_buttons(x, y)
        hold_slider(x, y)
    # apagar tile - botao direito
    elif mouse_pressed[2]:
        erase_tile(x, y)
    else: check_over_buttons(x, y)

    check_working_buttons()
    handle_keys()


def scroll_pallet(event:pygame.Event):
    if event.type == pygame.MOUSEWHEEL:
        if event.y == -1:    # down
            max = TILE_MAP_PALLET - editor.pallet.y_tiles
            if editor.pallet.anchor.y < max:
                editor.pallet.anchor.y += 1
                notify.add_event(EVENT_ANCHOR_VERTICAL, editor.pallet)
        if event.y == 1: # up
            if editor.pallet.anchor.y > 0:
                editor.pallet.anchor.y -= 1
                notify.add_event(EVENT_ANCHOR_VERTICAL, editor.pallet)
        

    


def click_grid(x, y, event:pygame.Event):
    # guards
    if event.type == pygame.MOUSEBUTTONUP: 
        editor.grid.unset_clicked()        
        return 
    if event.type != pygame.MOUSEBUTTONDOWN: return 

    if editor.grid.rect.collidepoint(x,y):     
        editor.grid.set_clicked()

  
def click_slider(x:int, y:int, event:pygame.Event):    
    # guards
    if event.type == pygame.MOUSEBUTTONUP: 
        editor.grid.horizontal_bar.unset_clicked()
        editor.grid.vertical_bar.unset_clicked()
        editor.pallet.vertical_bar.unset_clicked()
        return 
    if event.type != pygame.MOUSEBUTTONDOWN: return 
    if not pygame.mouse.get_pressed()[0]: return

    # horizontal bar - grid
    if editor.grid.horizontal_bar.rect.collidepoint(x,y):
        editor.grid.horizontal_bar.set_clicked()
        move_bar_horizontal(x, editor.grid, TILE_MAP_LEVELS[editor.level_idx][0])

    # vertical
    if editor.grid.vertical_bar.rect.collidepoint(x,y):
        editor.grid.vertical_bar.set_clicked()
        move_bar_vertical(y, editor.grid, TILE_MAP_LEVELS[editor.level_idx][1])

    # pallet
    if editor.pallet.vertical_bar.rect.collidepoint(x,y):
        editor.pallet.vertical_bar.set_clicked()
        move_bar_vertical(y, editor.pallet, TILE_MAP_PALLET)

   


def hold_slider(x:int, y:int):
    if editor.grid.horizontal_bar.clicked:        
        move_bar_horizontal(x, editor.grid, TILE_MAP_LEVELS[editor.level_idx][0])
    if editor.grid.vertical_bar.clicked:        
        move_bar_vertical(y, editor.grid, TILE_MAP_LEVELS[editor.level_idx][1])

    if editor.pallet.vertical_bar.clicked:        
        move_bar_vertical(y, editor.pallet, TILE_MAP_PALLET)


def move_bar_vertical(y, grid:Grid|Pallet, max_y):
    init_pos = grid.rect.top
    final_pos = grid.vertical_bar.rect.h + init_pos
        
    if (final_pos - y) < (SIZE_SCROLL//2): delta = (final_pos - y)
    elif (y - init_pos) < (SIZE_SCROLL//2): delta = -(y - init_pos)
    else: 
        delta = 0 
        init_pos += (SIZE_SCROLL//2)
        final_pos -= (SIZE_SCROLL//2)

    percentage = ((y+delta)-init_pos) / (final_pos-init_pos)
    grid.anchor.y = int((max_y - grid.y_tiles)*percentage)
    notify.add_event(EVENT_ANCHOR_VERTICAL, grid)
        

def move_bar_horizontal(x, grid:Grid|Pallet, max_x):
    init_pos = grid.rect.left
    final_pos = grid.horizontal_bar.rect.w + init_pos
        
    # ajuste fino slider no meio do clique
    if (final_pos - x) < (SIZE_SCROLL//2): delta = (final_pos - x)
    elif (x - init_pos) < (SIZE_SCROLL//2): delta = -(x - init_pos)
    else: 
        delta = 0 #pos = x
        init_pos += (SIZE_SCROLL//2)
        final_pos -= (SIZE_SCROLL//2)
        
    percentage = ((x+delta)-init_pos) / (final_pos-init_pos)
    grid.anchor.x = int((max_x - grid.x_tiles)*percentage)
    notify.add_event(EVENT_ANCHOR_HORIZONTAL, grid)



def click_buttons(x, y, event:pygame.Event):
    # guards
    if event.type == pygame.MOUSEBUTTONUP: 
        editor.grid.button_left.unset_clicked()
        editor.grid.button_right.unset_clicked()
        editor.grid.button_up.unset_clicked()
        editor.grid.button_down.unset_clicked()
        editor.button_save.unset_clicked()
        editor.button_load.unset_clicked()
        return 
    if event.type != pygame.MOUSEBUTTONDOWN: return 

    if editor.button_save.rect.collidepoint(x,y):     
        editor.button_save.set_clicked()
    if editor.button_load.rect.collidepoint(x,y):     
        editor.button_load.set_clicked()

    if editor.grid.button_left.working:
        if editor.grid.button_left.rect.collidepoint(x,y):     
            editor.grid.button_left.set_clicked()
    if editor.grid.button_right.working:
        if editor.grid.button_right.rect.collidepoint(x,y):     
            editor.grid.button_right.set_clicked()
    if editor.grid.button_up.working:
        if editor.grid.button_up.rect.collidepoint(x,y):     
            editor.grid.button_up.set_clicked()
    if editor.grid.button_down.working:
        if editor.grid.button_down.rect.collidepoint(x,y):     
            editor.grid.button_down.set_clicked()



def hold_buttons(x:int, y:int):
    if editor.grid.button_left.working and editor.grid.button_left.clicked:
        if editor.grid.button_left.rect.collidepoint(x,y):        
            editor.grid.anchor.x -= 1
            notify.add_event(EVENT_ANCHOR_HORIZONTAL, editor.grid)
    if editor.grid.button_up.working and editor.grid.button_up.clicked:
        if editor.grid.button_up.rect.collidepoint(x,y):        
            editor.grid.anchor.y -= 1
            notify.add_event(EVENT_ANCHOR_VERTICAL, editor.grid)
    if editor.grid.button_down.working and editor.grid.button_down.clicked:
        if editor.grid.button_down.rect.collidepoint(x,y):        
            editor.grid.anchor.y += 1
            notify.add_event(EVENT_ANCHOR_VERTICAL, editor.grid)
    if editor.grid.button_right.working and editor.grid.button_right.clicked:
        if editor.grid.button_right.rect.collidepoint(x,y):        
            editor.grid.anchor.x += 1
            notify.add_event(EVENT_ANCHOR_HORIZONTAL, editor.grid)



def check_over_buttons(x:int, y:int):    
    if editor.button_save.rect.collidepoint(x,y): 
        notify.add_event(EVENT_BUTTON_OVER, editor.button_save)
    if editor.button_load.rect.collidepoint(x,y): 
        notify.add_event(EVENT_BUTTON_OVER, editor.button_load)
        
    if editor.grid.button_left.rect.collidepoint(x,y): 
        notify.add_event(EVENT_BUTTON_OVER, editor.grid.button_left)
    if editor.grid.button_up.rect.collidepoint(x,y): 
        notify.add_event(EVENT_BUTTON_OVER, editor.grid.button_up)
    if editor.grid.button_down.rect.collidepoint(x,y): 
        notify.add_event(EVENT_BUTTON_OVER, editor.grid.button_down)
    if editor.grid.button_right.rect.collidepoint(x,y): 
        notify.add_event(EVENT_BUTTON_OVER, editor.grid.button_right)


def check_working_buttons():
    if editor.grid.anchor.x == 0: editor.grid.button_left.set_working(False)
    else: editor.grid.button_left.set_working(True)

    if editor.grid.anchor.y == 0: editor.grid.button_up.set_working(False)
    else: editor.grid.button_up.set_working(True)

    if editor.grid.anchor.y == (TILE_MAP_LEVELS[editor.level_idx][1]-editor.grid.y_tiles): 
        editor.grid.button_down.set_working(False)
    else: editor.grid.button_down.set_working(True)

    if editor.grid.anchor.x == (TILE_MAP_LEVELS[editor.level_idx][0]-editor.grid.x_tiles): 
        editor.grid.button_right.set_working(False)
    else: editor.grid.button_right.set_working(True)
    


def erase_tile(x:int, y:int):
    #if not editor.grid.clicked: return
    if not editor.grid.rect.collidepoint(x,y): return

    for tile in editor.grid.tiles:
        if tile.rect.collidepoint(x,y): 
            col, lin = tile.desc.split(",")            
            col = int(col) + int(editor.grid.anchor.x)
            lin = int(lin) + int(editor.grid.anchor.y)              
            if editor.grid.level.tiles[lin][col]: 
                editor.grid.level.tiles[lin][col] = None
                notify.add_event(EVENT_GRID_FILL, None)
                #editor.level1.save_level()                           
            break


def fill_tile(x:int, y:int):
    if not editor.grid.clicked: return
    fill = editor.pallet.select and editor.grid.rect.collidepoint(x,y)
    if not fill: return    

    for tile in editor.grid.tiles:
        if tile.rect.collidepoint(x,y):                                
            col, lin = tile.desc.split(",")
            col = int(col) + int(editor.grid.anchor.x)
            lin = int(lin) + int(editor.grid.anchor.y)
            tile = Tile(*editor.pallet.select.get())
            editor.grid.level.tiles[lin][col] = tile                            
            left = (col) * TILE_SIZE
            top = (lin) * TILE_SIZE
            editor.grid.level.tiles[lin][col].rect.topleft = (left, top)
            notify.add_event(EVENT_GRID_FILL, None) 
            #editor.level1.save_level()                        
            break


def save_map(x:int, y:int, event:pygame.Event):
    if event.type != pygame.MOUSEBUTTONDOWN: return  

    if editor.button_save.rect.collidepoint(x,y):
        editor.level.save_level()
        editor.save_config()
        notify.add_event(EVENT_BUTTON_MESSAGE, editor.button_save)


def load_map(x:int, y:int, event:pygame.Event):
    if event.type != pygame.MOUSEBUTTONDOWN: return  

    if editor.button_load.rect.collidepoint(x,y):        
        editor.change_level()        
        notify.add_event(EVENT_BUTTON_MESSAGE, editor.button_load)


def select_tile(x:int, y:int, event:pygame.Event):        
    if event.type != pygame.MOUSEBUTTONDOWN: return 
    if not pygame.mouse.get_pressed()[0]: return
    if not editor.pallet.rect.collidepoint(x,y): return
    
    for tile in editor.pallet.tiles:    
        if tile.rect.collidepoint(x,y):                                            
            col, lin = tile.desc.split(",")
            col = int(col) + int(editor.pallet.anchor.x)
            lin = int(lin) + int(editor.pallet.anchor.y)
            #editor.pallet.select = editor.pallet.tilemap.tiles[lin][col]  
            editor.pallet.select_pos = (lin,col)                        
            notify.add_event(EVENT_PALLET_SELECT, editor.pallet)              
            break
      


def exit(event:pygame.Event):
    if event.type == pygame.QUIT:
        editor.running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            editor.running = False


def handle_keys():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if editor.grid.anchor.x > 0:
            editor.grid.anchor.x -= 1
            notify.add_event(EVENT_ANCHOR_HORIZONTAL, editor.grid)           
    if keys[pygame.K_RIGHT]:
        max = TILE_MAP_LEVELS[editor.level_idx][0] - editor.grid.x_tiles
        if editor.grid.anchor.x < max:
            editor.grid.anchor.x += 1
            notify.add_event(EVENT_ANCHOR_HORIZONTAL, editor.grid)            
    if keys[pygame.K_UP]:
        if editor.grid.anchor.y > 0:
            editor.grid.anchor.y -= 1
            notify.add_event(EVENT_ANCHOR_VERTICAL, editor.grid)          
    if keys[pygame.K_DOWN]:
        max = TILE_MAP_LEVELS[editor.level_idx][1] - editor.grid.y_tiles
        if editor.grid.anchor.y < max:
            editor.grid.anchor.y += 1
            notify.add_event(EVENT_ANCHOR_VERTICAL, editor.grid)
           