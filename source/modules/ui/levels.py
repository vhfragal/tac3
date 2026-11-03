import json
from ..constants import *
import numpy as np
import scipy.sparse as sp
from ..entities.tiles import Tile, TileMap #tile_map


class Level():
    def __init__(self, idx:int, tile_map:TileMap):
        self.idx = idx
        self.tile_map = tile_map
        if not self.load(): self.load()
        

    def change_level(self, idx:int):
        self.idx = idx
        if not self.load(): self.load()
 

    def create_matrix_tile(self):
        x, y = TILE_MAP_LEVELS[self.idx][1], TILE_MAP_LEVELS[self.idx][0]
        dense_matrix = np.zeros((x,y), dtype=int)        
        sparse_matrix = sp.csr_array(dense_matrix)
        sp.save_npz(FILE_LEVELS[self.idx], sparse_matrix, compressed=False)

    def save_level(self):
        x, y = TILE_MAP_LEVELS[self.idx][1], TILE_MAP_LEVELS[self.idx][0]
        dense_matrix = np.zeros((x,y), dtype=int)
        for lin in range(TILE_MAP_LEVELS[self.idx][1]):                     
            for col in range(TILE_MAP_LEVELS[self.idx][0]):
                if self.tiles[lin][col]:
                    dense_matrix[lin,col] = self.tiles[lin][col].id
                else:
                    dense_matrix[lin,col] = 0
        sparse_matrix = sp.csr_array(dense_matrix)
        sp.save_npz(FILE_LEVELS[self.idx], sparse_matrix, compressed=False)


    def load(self):                       
        self.tiles:list[list[Tile]] = []
        try:
            dense_matrix = sp.load_npz(FILE_LEVELS[self.idx])
            #print(TILE_MAP_LEVELS[self.idx], dense_matrix, TILE_MAP_LEVELS[self.idx][0], TILE_MAP_LEVELS[self.idx][1])
            for lin in range(TILE_MAP_LEVELS[self.idx][1]):
                line = []           
                for col in range(TILE_MAP_LEVELS[self.idx][0]):  
                    #print(lin, col)                  
                    if dense_matrix[lin,col] != 0:
                        self.obj_call(dense_matrix, lin, col, line)
                    else: line.append(None)  
                self.tiles.append(line)  

        except FileNotFoundError:            
            self.create_matrix_tile()
            return False
        except json.JSONDecodeError:
            print("Error: The file is not a valid JSON format.")
        return True


    def obj_call(self, dense_matrix, lin:int, col:int, line:list):
        for k, call in enumerate(self.tile_map.codes):
            if dense_matrix[lin,col] == k:
                id = call[0]
                surf = call[1]
                desc = call[2]
                obj:Tile = Tile(id, surf, desc)
                x, y = col, lin # 2d position
                obj.rect.topleft = (x*TILE_SIZE, y*TILE_SIZE)
                line.append(obj)
