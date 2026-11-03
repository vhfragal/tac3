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
uniform vec2 u_c; // Constante C do conjunto de Julia

void main() {
    // Mapeia o pixel para a coordenada Z inicial
    vec2 z = uvs * vec2(u_resolution.x / u_resolution.y, 1.0);
    z = z * u_zoom + u_offset;

    vec2 c = u_c; // C fixo para toda a tela nesta iteração
    float iter = 0.0;
    float max_iter = 200.0; // Aumentado para melhor definição das bordas de Julia

    // Equação de Julia: Z_next = Z^2 + C
    for (float i = 0.0; i < 200.0; i++) {
        if (dot(z, z) > 4.0) break;
        z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
        iter = i;
    }

    if (iter == max_iter - 1.0) {
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    } else {
        float t = iter / max_iter;
        // Paleta de cores elétrica e vibrante
        vec3 color = vec3(0.5 + 0.5 * sin(6.28 * t + 0.0),
                          0.5 + 0.5 * sin(6.28 * t + 1.0),
                          0.5 + 0.5 * sin(6.28 * t + 2.0));
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

# Configurações iniciais
zoom = 1.5
offset_x, offset_y = 0.0, 0.0
c_real, c_imag = -0.7, 0.27015 # Valores padrão iniciais interessantes
lock_c = False # Controla se o mouse altera a forma de Julia ou não

program['u_resolution'].value = (WIDTH, HEIGHT)

def screen_to_complex(mx, my, zoom, offset_x, offset_y, width, height):
    nx = (mx / width) * 2.0 - 1.0
    ny = 1.0 - (my / height) * 2.0
    cx = nx * (width / height) * zoom + offset_x
    cy = ny * zoom + offset_y
    return cx, cy

dragging = False
last_mouse_pos = (0, 0)

running = True
while running:
    # Coleta a posição atual do mouse a cada frame
    mx, my = pygame.mouse.get_pos()

    # Se NÃO estiver travado, transforma a posição do mouse em coordenadas complexas para gerar o C
    if not lock_c:
        # Escala o movimento do mouse para um intervalo suave do plano complexo (-1.5 a 1.5)
        c_real = ((mx / WIDTH) * 3.0) - 1.5
        c_imag = (((HEIGHT - my) / HEIGHT) * 3.0) - 1.5

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Barra de espaço trava/destrava a mutação do fractal pelo mouse
            lock_c = not lock_c
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5): # Scroll zoom
                cx_before, cy_before = screen_to_complex(mx, my, zoom, offset_x, offset_y, WIDTH, HEIGHT)
                if event.button == 4:
                    zoom *= 0.85
                else:
                    zoom *= 1.15
                cx_after, cy_after = screen_to_complex(mx, my, zoom, 0, 0, WIDTH, HEIGHT)
                offset_x = cx_before - cx_after
                offset_y = cy_before - cy_after
                
            elif event.button == 1: # Clique esquerdo arrasta (melhor usar quando lock_c estiver ativo)
                dragging = True
                last_mouse_pos = event.pos
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                
        elif event.type == pygame.MOUSEMOTION and dragging:
            dx = mx - last_mouse_pos[0]
            dy = my - last_mouse_pos[1]
            offset_x -= (dx / WIDTH) * 2.0 * (WIDTH / HEIGHT) * zoom
            offset_y += (dy / HEIGHT) * 2.0 * zoom
            last_mouse_pos = (mx, my)

    # Envia as variáveis atualizadas para o fragment shader
    program['u_zoom'].value = zoom
    program['u_offset'].value = (offset_x, offset_y)
    program['u_c'].value = (c_real, c_imag)

    ctx.clear(0.0, 0.0, 0.0, 1.0)
    vao.render()

    pygame.display.flip()
    clock.tick(60)

vbo.release()
vao.release()
program.release()
pygame.quit()
sys.exit()
