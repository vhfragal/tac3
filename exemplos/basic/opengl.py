import pygame
from pygame.locals import *
from OpenGL.GL import *
import sys

# 1. Initialize Pygame-ce and OpenGL window
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("2D OpenGL Platformer")
clock = pygame.time.Clock()

# 2. Configure OpenGL for 2D graphics
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
# Set up ortho matrix matching screen coordinates (0 to WIDTH, HEIGHT to 0)
glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Enable 2D transparency blending
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# 3. Helper function to draw colored rectangles in OpenGL
def draw_rect(x, y, w, h, color):
    """Draws a solid colored rectangle at screen coordinates."""
    glColor4f(color[0]/255.0, color[1]/255.0, color[2]/255.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(x, y)          # Top-Left
    glVertex2f(x + w, y)      # Top-Right
    glVertex2f(x + w, y + h)  # Bottom-Right
    glVertex2f(x, y + h)      # Bottom-Left
    glEnd()

# 4. Game Entities using standard pygame.FRect
player_rect = pygame.FRect(100, 100, 40, 60)
platforms = [
    pygame.FRect(0, 500, 1200, 50),     # Floor
    pygame.FRect(300, 400, 200, 30),    # Floating platform 1
    pygame.FRect(600, 300, 200, 30),    # Floating platform 2
]

# Physics & Input Variables
velocity_y = 0
velocity_x = 0
GRAVITY = 0.5
JUMP_STRENGTH = -12
ACCELERATION = 0.8
FRICTION = 0.85
on_ground = False

# Camera offset
camera_x = 0

# 5. Main Game Loop
running = True
while running:
    # --- Input Handling ---
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE and on_ground:
                velocity_y = JUMP_STRENGTH
                on_ground = False

    keys = pygame.key.get_pressed()
    if keys[K_LEFT] or keys[K_a]:
        velocity_x -= ACCELERATION
    if keys[K_RIGHT] or keys[K_d]:
        velocity_x += ACCELERATION

    # --- Physics & Platformer Logic ---
    velocity_x *= FRICTION  # Apply horizontal drag
    velocity_y += GRAVITY    # Apply gravity

    # Horizontal Movement & Collisions
    player_rect.x += velocity_x
    for plat in platforms:
        if player_rect.colliderect(plat):
            if velocity_x > 0:
                player_rect.right = plat.left
                velocity_x = 0
            elif velocity_x < 0:
                player_rect.left = plat.right
                velocity_x = 0

    # Vertical Movement & Collisions
    player_rect.y += velocity_y
    on_ground = False
    for plat in platforms:
        if player_rect.colliderect(plat):
            if velocity_y > 0:  # Falling down
                player_rect.bottom = plat.top
                velocity_y = 0
                on_ground = True
            elif velocity_y < 0:  # Hitting ceiling
                player_rect.top = plat.bottom
                velocity_y = 0

    # --- Camera Scrolling System ---
    # Linear interpolation (lerp) camera tracking the player
    target_camera_x = player_rect.centerx - WIDTH // 2
    camera_x += (target_camera_x - camera_x) * 0.1

    # --- Rendering with OpenGL ---
    # Clear screen with a dark blue sky background
    glClearColor(0.1, 0.14, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Save the base matrix state
    glPushMatrix()
    # Apply camera translations (moves the world relative to camera)
    glTranslatef(-camera_x, 0, 0)

    # Draw all level platforms (Green)
    for plat in platforms:
        draw_rect(plat.x, plat.y, plat.width, plat.height, (46, 204, 113))

    # Draw the Player block (Red)
    draw_rect(player_rect.x, player_rect.y, player_rect.width, player_rect.height, (231, 76, 60))

    # Restore matrix state to clear the translation for UI elements
    glPopMatrix()

    # --- Update Screen ---
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()