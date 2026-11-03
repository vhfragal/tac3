import pygame
import sys
import moderngl
import numpy as np

# Inicializa o Pygame com contexto OpenGL
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

ctx = moderngl.create_context()

VERTEX_SHADER = """
#version 330 core
in vec2 in_vert;
out vec2 uvs;
void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    uvs = in_vert;
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec2 uvs;
out vec4 fragColor;

uniform vec2 u_resolution;
uniform float u_zoom;
uniform vec2 u_offset;

void main() {
    vec2 c = uvs * vec2(u_resolution.x / u_resolution.y, 1.0);
    c = c * u_zoom + u_offset;

    vec2 z = vec2(0.0);
    float iter = 0.0;
    float max_iter = 150.0; // Aumentado para manter detalhes no zoom profundo

    for (float i = 0.0; i < 150.0; i++) {
        if (dot(z, z) > 4.0) break;
        z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
        iter = i;
    }

    if (iter == max_iter - 1.0) {
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    } else {
        float t = iter / max_iter;
        vec3 color = vec3(0.5 + 0.5 * cos(6.28 * t + 0.0),
                          0.5 + 0.5 * cos(6.28 * t + 0.4),
                          0.5 + 0.5 * cos(6.28 * t + 0.2));
        fragColor = vec4(color, 1.0);
    }
}
"""

program = ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)

vertices = np.array([
    -1.0, -1.0,
     1.0, -1.0,
    -1.0,  1.0,
    -1.0,  1.0,
     1.0, -1.0,
     1.0,  1.0,
], dtype='f4')

vbo = ctx.buffer(vertices.tobytes())
vao = ctx.vertex_array(program, [(vbo, '2f', 'in_vert')])

# Configurações iniciais de visualização
zoom = 1.2
offset_x, offset_y = -0.5, 0.0
program['u_resolution'].value = (WIDTH, HEIGHT)

def screen_to_complex(mx, my, zoom, offset_x, offset_y, width, height):
    """Converte coordenadas de pixel da tela para o plano complexo do fractal"""
    # Transforma pixels (0 a Width) para coordenadas normalizadas OpenGL (-1 a 1)
    nx = (mx / width) * 2.0 - 1.0
    ny = 1.0 - (my / height) * 2.0 # Inverte o eixo Y do Pygame para alinhar com o OpenGL
    
    # Aplica o aspecto, zoom e offset idênticos ao Fragment Shader
    cx = nx * (width / height) * zoom + offset_x
    cy = ny * zoom + offset_y
    return cx, cy

# Controle de arrastar com o mouse
dragging = False
last_mouse_pos = (0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            
        # Zoom com a roda do mouse (Scroll) no ponto do cursor
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5): # 4 é Scroll Up, 5 é Scroll Down
                mx, my = event.pos
                # Ponto complexo antes do zoom
                cx_before, cy_before = screen_to_complex(mx, my, zoom, offset_x, offset_y, WIDTH, HEIGHT)
                
                # Aplica o fator de zoom
                if event.button == 4:
                    zoom *= 0.85
                else:
                    zoom *= 1.15
                    
                # Ponto complexo após o zoom (com offset zerado para achar a diferença)
                cx_after, cy_after = screen_to_complex(mx, my, zoom, 0, 0, WIDTH, HEIGHT)
                
                # Ajusta o offset para manter o ponto fixo sob o mouse
                offset_x = cx_before - cx_after
                offset_y = cy_before - cy_after
                
            elif event.button == 1: # Botão esquerdo para arrastar
                dragging = True
                last_mouse_pos = event.pos
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                
        elif event.type == pygame.MOUSEMOTION and dragging:
            # Arrasta o plano proporcionalmente ao zoom atual
            mx, my = event.pos
            dx = mx - last_mouse_pos[0]
            dy = my - last_mouse_pos[1]
            
            offset_x -= (dx / WIDTH) * 2.0 * (WIDTH / HEIGHT) * zoom
            offset_y += (dy / HEIGHT) * 2.0 * zoom # Invertido pois Y do OpenGL cresce para cima
            last_mouse_pos = event.pos

    # Atualiza uniforms e renderiza
    program['u_zoom'].value = zoom
    program['u_offset'].value = (offset_x, offset_y)

    ctx.clear(0.0, 0.0, 0.0, 1.0)
    vao.render()

    pygame.display.flip()
    clock.tick(60)

vbo.release()
vao.release()
program.release()
pygame.quit()
sys.exit()
