import pygame
from .editor import editor
from .input import inputs
from ..display import display
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT


def level_maker():
    pygame.display.init()
    pygame.font.init()
    
    editor.create()

    """O Game Loop Principal"""
    #try:           
    while editor.running:
        dt = display.game_tick()   
        inputs()
        update(dt)
        draw()
    '''except Exception as e:
        print(e)            # log here
        editor.running = False
        pygame.quit()
        sys.exit()'''


def update(dt):
    editor.update(dt)

        
def draw():
    """Loop de Renderização: Onde desenhamos na tela"""                 
    # Render Phase
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # ordem importa - cada layer por vez - pode organizar
    editor.draw()
    
    pygame.display.flip()
    # forçar sincronização de hardware CPU e GPU - chamadas assincronas
    #glFinish()