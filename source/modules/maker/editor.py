from ..display import display
from .info import Info
from .grid import Grid
from ..entities.tiles import TileMap
from OpenGL.GL import *
from ..ui.background import Background
from ..ui.levels import Level
from .notify import notify
from .pallet import Pallet
from .button import Button
from ..constants import *
from ..utils import utils
import json

class Editor:
    def __init__(self):
        pass

    def create(self):
        self.running = True
        self.level_idx = 1         

        display.create_display()
        self.bg = Background(*display.size, "Black")

        # load tiles
        self.tile_map = TileMap()        
        self.tile_map.load_sprite_maps()
        self.level = Level(self.level_idx, self.tile_map)
        
        # assets        
        self.grid = Grid(self.level)        
        self.pallet = Pallet(self.tile_map)   
        self.info = Info(self.grid, self.pallet) 

        self.load_config()       
      
        text, message = "Save", "Map saved!!!"
        self.button_save = Button(text=text, message=message, icon=ICON_SAVE)
        self.button_save.rect.topleft = (0, display.size[1]-SIZE_ICON[1])

        text, message = "Load next", "Map loaded!!!"
        self.button_load = Button(text=text, message=message, icon=ICON_LOAD)
        self.button_load.rect.topleft = (self.button_save.rect.w, display.size[1]-SIZE_ICON[1])


    def load_config(self):
        self.config = {}
        try:
            resource = utils.get_full_path(FILE_CONFIG)            
            with open(resource, 'r', encoding='utf-8') as file:
                self.config = json.load(file)
                self.level_idx = self.config["level"]
                self.grid.anchor.xy = self.config["anchor_grid"]
                self.pallet.anchor.xy = self.config["anchor_pallet"]
                self.pallet.select_pos = self.config["select_pallet"]
                self.level.change_level(self.level_idx)
                self.info = Info(self.grid, self.pallet)                
                self.refresh()                            
        except FileNotFoundError:
            print(f"Warning: The file '{resource}' was not found. Creating...")
            # create first config            
            self.save_config()
            return False
        return True


    def refresh(self):        
        notify.add_event(EVENT_PALLET_SELECT, editor.pallet)
        notify.add_event(EVENT_ANCHOR_HORIZONTAL, editor.grid)
        notify.add_event(EVENT_ANCHOR_VERTICAL, editor.grid)
        notify.add_event(EVENT_ANCHOR_VERTICAL, editor.pallet)
        notify.add_event(EVENT_GRID_FILL, None) 


    def change_level(self):
        self.level_idx = ((self.level_idx) % (len(FILE_LEVELS)-1)) + 1
        
        self.level.change_level(self.level_idx)
        self.grid.anchor.xy = 0,0
        self.info = Info(self.grid, self.pallet) 
        #print(self.level_idx, self.grid.anchor, self.grid.level.idx)

        self.config["level"] = self.level_idx    
        self.config["anchor_grid"] = 0,0
        self.config["anchor_pallet"] = 0,0
        self.config["select_pallet"] = 0,0
        resource = utils.get_full_path(FILE_CONFIG)            
        with open(resource, 'w', encoding='utf-8') as file:
            json.dump(self.config, file, indent=4)

        self.refresh()



    def save_config(self):        
        self.config["level"] = self.level_idx    
        self.config["anchor_grid"] = self.grid.anchor.x, self.grid.anchor.y
        self.config["anchor_pallet"] = self.pallet.anchor.x, self.pallet.anchor.y
        self.config["select_pallet"] = self.pallet.select_pos
        resource = utils.get_full_path(FILE_CONFIG)            
        with open(resource, 'w', encoding='utf-8') as file:
            json.dump(self.config, file, indent=4)

        
        

    def update(self, dt:float):
        self.info.update(dt)
        self.grid.update(dt)
        self.pallet.update(dt)
        self.button_save.update(dt) 
        self.button_load.update(dt)  
        
        notify.clear()


    def draw(self):
        self.bg.draw()
        self.info.draw()
        self.grid.draw()
        self.pallet.draw()
        self.button_save.draw()
        self.button_load.draw()
        
        


editor = Editor()

