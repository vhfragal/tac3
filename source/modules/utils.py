import pygame
import os
import sys
from OpenGL.GL import *
from OpenGL.GLU import *

class Utils():
    def __init__(self):                   
        if getattr(sys, 'frozen', False):
            # Executável compilado com cx_Freeze
            self.path = os.path.dirname(sys.executable)
            # ou no main.py
            #os.path.split(os.path.abspath(__file__))[0]
        else:
            # Modo desenvolvimento (.py)
            self.path = os.path.abspath(".")       
  
    def get_full_path(self, resource):
        return os.path.join(self.path, resource)

    def load_font(self, file, size):
        return pygame.font.Font(os.path.join(self.path, file), size)
    
    def load_image(self, file):
        return pygame.image.load(os.path.join(self.path, file)).convert_alpha()


    def cut_sprite(self, map:pygame.Surface, x,y,w,h, to_size:tuple[int,int],
                   frame_list:list[pygame.Surface], texture_list:list[any]):
        img = map.subsurface((x,y,w,h))
        img = pygame.transform.smoothscale(img, to_size)            
        frame_list.append(img)
        texture_list.append(self.surface_to_texture(img))


    def surface_to_texture(self, pygame_surface:pygame.Surface):
        """
        Converte um Pygame Surface em uma textura OpenGL e retorna o ID da textura.
        """
        # 1. Inverte a imagem verticalmente para alinhar o sistema de coordenadas (Pygame vs OpenGL)
        flipped_surface = pygame.transform.flip(pygame_surface, False, True)
        
        # 2. Converte a superfície para uma string/bytes de pixels no formato RGBA
        # Usamos RGBA para garantir suporte a transparências (PNGs, etc.)
        texture_data = pygame.image.tobytes(flipped_surface, "RGBA", True)
        width, height = flipped_surface.get_size()
        
        # 3. Gera um ID único para a textura no OpenGL
        texture_id = glGenTextures(1)
        
        # Vincula (ativa) a textura criada para configurá-la
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        # Define os filtros de renderização (GL_NEAREST preserva o estilo Pixel Art sem borrar)
        # GL_LINEAR - anti aliasing
        # Mipmaps (GL_NEAREST_MIPMAP_NEAREST, GL_LINEAR_MIPMAP_LINEAR, ...)
        # para objetos distantes, evitando ruído visual e melhorando a performance
        # Filtro Anisotrópico (GL_TEXTURE_MAX_ANISOTROPY_EXT)
        # Melhora drasticamente a nitidez de texturas vistas em ângulos inclinados 

        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        # A GPU só usará os mipmaps entre os tamanhos dos níveis 1 e 4
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 1);
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 4);
        #glGenerateMipmap(GL_TEXTURE_2D);

        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # Carrega os bytes da imagem diretamente para a memória da GPU
        glTexImage2D(
            GL_TEXTURE_2D,    # Tipo da textura
            0,                # Nível de Mipmap (0 = padrão)
            GL_RGBA,          # Formato interno do OpenGL
            width,            # Largura da imagem
            height,           # Altura da imagem
            0,                # Borda (deve ser 0)
            GL_RGBA,          # Formato dos pixels de entrada
            GL_UNSIGNED_BYTE, # Tipo de dado dos pixels
            texture_data      # Os bytes reais da imagem
        )

        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)

        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        # Desvincula a textura para evitar modificações acidentais posteriores
        glBindTexture(GL_TEXTURE_2D, 0)
        
        return texture_id


    def update_texture(self, texture_id, pygame_surface:pygame.Surface):
            """
            Converte um Pygame Surface em uma textura OpenGL e retorna o ID da textura.
            """
            # 1. Inverte a imagem verticalmente para alinhar o sistema de coordenadas (Pygame vs OpenGL)
            flipped_surface = pygame.transform.flip(pygame_surface, False, True)
            
            # 2. Converte a superfície para uma string/bytes de pixels no formato RGBA
            # Usamos RGBA para garantir suporte a transparências (PNGs, etc.)
            texture_data = pygame.image.tobytes(flipped_surface, "RGBA", True)
            width, height = flipped_surface.get_size()
                                  
            # Vincula (ativa) a textura criada para configurá-la
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            # Define os filtros de renderização (GL_NEAREST preserva o estilo Pixel Art sem borrar)
            # GL_LINEAR - anti aliasing
            # Mipmaps (GL_NEAREST_MIPMAP_NEAREST, GL_LINEAR_MIPMAP_LINEAR, ...)
            # para objetos distantes, evitando ruído visual e melhorando a performance
            # Filtro Anisotrópico (GL_TEXTURE_MAX_ANISOTROPY_EXT)
            # Melhora drasticamente a nitidez de texturas vistas em ângulos inclinados 

            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            # A GPU só usará os mipmaps entre os tamanhos dos níveis 1 e 4
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 1);
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 4);
            #glGenerateMipmap(GL_TEXTURE_2D);
            
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            # Carrega os bytes da imagem diretamente para a memória da GPU
            glTexImage2D(
                GL_TEXTURE_2D,    # Tipo da textura
                0,                # Nível de Mipmap (0 = padrão)
                GL_RGBA,          # Formato interno do OpenGL
                width,            # Largura da imagem
                height,           # Altura da imagem
                0,                # Borda (deve ser 0)
                GL_RGBA,          # Formato dos pixels de entrada
                GL_UNSIGNED_BYTE, # Tipo de dado dos pixels
                texture_data      # Os bytes reais da imagem
            )

            #glGenerateMipmap(GL_TEXTURE_2D)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glGenerateMipmap(GL_TEXTURE_2D)

            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            
            # Desvincula a textura para evitar modificações acidentais posteriores
            glBindTexture(GL_TEXTURE_2D, 0)
            
            return texture_id


    def draw_textured_quad(self, texture_id, x, y, w, h):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        glColor4f(1, 1, 1, 1) # Reseta a cor global para não aplicar filtros cromáticos na imagem

        '''glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        rx = round(x)
        ry = round(y)
        rw = round(w)
        rh = round(h)'''
        
        glBegin(GL_QUADS)
        # Mapeamento: (Coordenada_Textura, Coordenada_Tela)
        glTexCoord2f(0, 0); glVertex2f(x, y)         # Superior Esquerdo
        glTexCoord2f(1, 0); glVertex2f(x + w, y)     # Superior Direito
        glTexCoord2f(1, 1); glVertex2f(x + w, y + h) # Inferior Direito
        glTexCoord2f(0, 1); glVertex2f(x, y + h)     # Inferior Esquerdo
        glEnd()
        
        glDisable(GL_TEXTURE_2D)


    def draw_rect(self, x, y, w, h, color):
        """Draws a solid colored rectangle at screen coordinates."""
        glColor4f(color[0]/255.0, color[1]/255.0, color[2]/255.0, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(x, y)          # Top-Left
        glVertex2f(x + w, y)      # Top-Right
        glVertex2f(x + w, y + h)  # Bottom-Right
        glVertex2f(x, y + h)      # Bottom-Left
        glEnd()
              

utils = Utils()