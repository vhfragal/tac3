#import pygame
import json
from ..constants import *
#from ..utils import utils
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


'''
class Level1(Level):
    def __init__(self):
        super().__init__(1)

    def create_first_map(self):
        try:
            map1 = {            
                "height": TILE_MAP_LEVEL1[1],
                "width": TILE_MAP_LEVEL1[0],
                "tilewidth": TILE_SIZE,
                "tileheight": TILE_SIZE,  
                "layers": [
                    {                        
                        "map": FILE_LV1,
                        "height": TILE_MAP_LEVEL1[1],
                        "width": TILE_MAP_LEVEL1[0],
                        "name": "Blocks",
                        "opacity": 1,            
                        "visible": True,
                        "x": 0,
                        "y": 0
                    }
                ],  
                "orientation": "orthogonal",
                "renderorder": "right-down",  
                "type": "map",
                "version": "0.01"
            }
 
            resource = utils.get_full_path(FILE_LV1_JSON)            
            with open(resource, 'w', encoding='utf-8') as file:
                json.dump(map1, file, indent=4)

            self.create_matrix_tile()

        except Exception as e:
            # log
            print(e)


    def create_matrix_tile(self):
        # 1. Create a matrix with mostly zeros
        # (Using sparse array syntax - standard in SciPy)
        dense_matrix = np.zeros((TILE_MAP_LEVEL1[1], TILE_MAP_LEVEL1[0]), dtype=int)
              
        # 2. Convert to a sparse representation (CSR format)
        sparse_matrix = sp.csr_array(dense_matrix)
        # 3. Save to a compressed .npz file
        sp.save_npz(FILE_LV1, sparse_matrix, compressed=False)
        #np.savetxt('matrix.csv', dense_matrix, delimiter=',')


    def load_level(self):
        pass
        # save and load precisa ser refatorado! menu para escolha de arquivo de nivel   
        # salvar arquivo de configuração para guardar posicao de nivel e ancora
        # info tbm adaptar
        # novo botao de create level
        

    def save_level(self):
        dense_matrix = np.zeros((TILE_MAP_LEVEL1[1], TILE_MAP_LEVEL1[0]), dtype=int)
        for lin in range(TILE_MAP_LEVEL1[1]):                     
            for col in range(TILE_MAP_LEVEL1[0]):
                if self.tiles[lin][col]:
                    dense_matrix[lin,col] = self.tiles[lin][col].id
                else:
                    dense_matrix[lin,col] = 0
        sparse_matrix = sp.csr_array(dense_matrix)
        sp.save_npz(FILE_LV1, sparse_matrix, compressed=False)



    def load(self, tile_map):        
        # debug
        #self.create_first_map()
                
        self.tiles:list[list[Tile]] = []
        try:
            resource = utils.get_full_path(FILE_LV1_JSON)            
            with open(resource, 'r', encoding='utf-8') as file:
                self.data = json.load(file)

            # Load it back instantly
            dense_matrix = sp.load_npz(FILE_LV1)
            for lin in range(TILE_MAP_LEVEL1[1]):
                line = []           
                for col in range(TILE_MAP_LEVEL1[0]):                    
                    if dense_matrix[lin,col] != 0:
                        self.obj_call(dense_matrix, lin, col, line, tile_map)
                    else: line.append(None)  
                self.tiles.append(line)  

        except FileNotFoundError:
            print(f"Error: The file '{resource}' was not found.")
            # create first map
            self.create_first_map()
            return False
        except json.JSONDecodeError:
            print("Error: The file is not a valid JSON format.")
        return True


    def obj_call(self, dense_matrix, lin, col, line, tile_map:TileMap):
        for k, call in enumerate(tile_map.codes):
            if dense_matrix[lin,col] == k:
                id = call[0]
                surf = call[1]
                desc = call[2]
                obj:Tile = Tile(id, surf, desc)
                x, y = col, lin # 2d position
                obj.rect.topleft = (x*TILE_SIZE, y*TILE_SIZE)
                line.append(obj)

'''
#level1 = Level1()
