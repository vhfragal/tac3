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
        self.w, self.h = self.size
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
        flags = FULLSCREEN | DOUBLEBUF | OPENGL   #| pygame.HWSURFACE   
        # ligar vsync no final com fps limitado ex. 60
        pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
        self.screen = pygame.display.set_mode(self.size, 
                                              flags, 
                                              display=self.selected_display, 
                                              vsync=0)
       
        # Setup 2D orthogonal projection
        #glViewport(0, 0, self.w, self.h)        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.w, self.h, 0, -1, 1)  # (0,0) at top-left
        #gluOrtho2D(0.0, float(self.w), float(self.h), 0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Enable Blending for Alpha/Transparency
        glShadeModel(GL_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        #glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        #glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


        
    def reload(self):
        pass


    def game_tick(self):
        # Captura o tempo decorrido desde o último quadro em segundos (Delta Time)
        # Limita o FPS máximo para não estressar o processador desnecessariamente
        #self.delta_time = min(self.clock.tick_busy_loop(FPS) / 1000.0, 0.033)
        self.delta_time = self.clock.tick(FPS) / 1000.0
        #print(self.delta_time)
        return self.delta_time       

       


display = Display()