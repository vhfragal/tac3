import pygame
#import time
from pygame.locals import *
from .constants import TITLE, FPS
from OpenGL.GL import *
from OpenGL.GLU import *

class Display():
    def __init__(self):
        pass

    def create_display(self):                
        self.clock = pygame.time.Clock() 

        # display info and sizes
        num_displays = pygame.display.get_num_displays()    
        self.selected_display = 0  
        desktop_sizes = pygame.display.get_desktop_sizes()                
        self.size = desktop_sizes[self.selected_display]
        self.all_resolutions = pygame.display.list_modes(display=self.selected_display)
        print("displays ", num_displays, desktop_sizes)
        print(self.all_resolutions)
        print(self.size)
        
        #info = pygame.display.Info()    # vetorial dirty sprites        
        #self.size = (info.current_w, info.current_h)
               
        pygame.display.set_caption(TITLE)         
        #flags = 0  
        #flags = pygame.NOFRAME #| pygame.OPENGL | pygame.DOUBLEBUF    # vetorial
        #flags = pygame.SCALED | pygame.FULLSCREEN  # pixel art  
        flags = FULLSCREEN | DOUBLEBUF | OPENGL      
        # ligar vsync no final com fps limitado ex. 60
        self.screen = pygame.display.set_mode(self.size, 
                                              flags, 
                                              display=self.selected_display, 
                                              vsync=0)
       
        # Setup 2D orthogonal projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.size[0], self.size[1], 0, -1, 1)  # (0,0) at top-left
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Enable Blending for Alpha/Transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


        
    def reload(self):
        pass


    def game_tick(self):
        # Captura o tempo decorrido desde o último quadro em segundos (Delta Time)
        # Limita o FPS máximo para não estressar o processador desnecessariamente
        self.delta_time = min(self.clock.tick_busy_loop(FPS) / 1000.0, 0.033)
        #print(self.delta_time)
        return self.delta_time       

       


display = Display()