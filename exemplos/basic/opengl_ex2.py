import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# 1. SETUP & INITIALIZATION
pygame.init()
WIDTH, HEIGHT = 800, 600
pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN | SCALED | DOUBLEBUF | OPENGL | HWSURFACE, vsync=0)
pygame.display.set_caption("Pygame OpenGL 2D Platformer - Complete")

# Setup 2D orthogonal projection
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)  # (0,0) at top-left
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Enable Blending for Alpha/Transparency
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# 2. GENERATE PROCEDURAL TEXTURE
def create_dummy_texture():
    # Create a 64x64 RGBA surface for a retro character
    surf = pygame.Surface((64, 64), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0)) # Transparent background
    
    # Outer body (Cyan robot style)
    pygame.draw.rect(surf, (0, 200, 255, 255), (8, 8, 48, 48), border_radius=12)
    # Inner face / details
    pygame.draw.rect(surf, (255, 255, 255, 255), (16, 16, 32, 20), border_radius=4)
    # Eyes
    pygame.draw.circle(surf, (0, 0, 0, 255), (26, 26), 4)
    pygame.draw.circle(surf, (0, 0, 0, 255), (38, 26), 4)
    
    texture_data = pygame.image.tobytes(surf, "RGBA", True)
    width, height = surf.get_size()
    
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    return tex_id

player_texture = create_dummy_texture()

# 3. GAME OBJECTS & RAYCAST AABB PHYSICS
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 40
        self.h = 40
        self.vx = 0
        self.vy = 0
        # Speeds are now defined in PIXELS PER SECOND
        self.gravity = 1500  
        self.speed = 300     # Horizontal speed
        self.jump_force = -600
        self.is_grounded = False

    def update(self, dt, platforms):
        # 1. Apply Gravity scaled by delta time
        self.vy += self.gravity * dt
        if self.vy > 800:  # Terminal velocity
            self.vy = 800

        # --- X Movement and Collision ---
        # Move by velocity * time passed
        self.x += self.vx * dt
        for plat in platforms:
            if self.check_collision(plat):
                if self.vx > 0: 
                    self.x = plat['x'] - self.w
                elif self.vx < 0: 
                    self.x = plat['x'] + plat['w']
                self.vx = 0

        # --- Y Movement and Collision ---
        self.is_grounded = False
        self.y += self.vy * dt
        for plat in platforms:
            if self.check_collision(plat):
                if self.vy > 0: # Falling down
                    self.y = plat['y'] - self.h
                    self.vy = 0
                    self.is_grounded = True
                elif self.vy < 0: # Jumping up
                    self.y = plat['y'] + plat['h']
                    self.vy = 0

    def check_collision(self, rect):
        return (self.x < rect['x'] + rect['w'] and
                self.x + self.w > rect['x'] and
                self.y < rect['y'] + rect['h'] and
                self.y + self.h > rect['y'])

    def draw(self):
        # Draw Textured Player Quad
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, player_texture)
        glColor4f(1, 1, 1, 1) # Retain texture colors
        
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex2f(self.x, self.y)
        glTexCoord2f(1, 1); glVertex2f(self.x + self.w, self.y)
        glTexCoord2f(1, 0); glVertex2f(self.x + self.w, self.y + self.h)
        glTexCoord2f(0, 0); glVertex2f(self.x, self.y + self.h)
        glEnd()
        glDisable(GL_TEXTURE_2D)

def draw_platform(plat):
    glColor4f(*plat['color'])
    glBegin(GL_QUADS)
    glVertex2f(plat['x'], plat['y'])
    glVertex2f(plat['x'] + plat['w'], plat['y'])
    glVertex2f(plat['x'] + plat['w'], plat['y'] + plat['h'])
    glVertex2f(plat['x'], plat['y'] + plat['h'])
    glEnd()

# Define Stage Platforms
platforms = [
    {'x': 0,   'y': 520, 'w': 800, 'h': 80,  'color': (0.2, 0.5, 0.3, 1.0)}, # Floor
    {'x': 200, 'y': 400, 'w': 150, 'h': 20,  'color': (0.7, 0.4, 0.2, 1.0)}, # Plat 1
    {'x': 450, 'y': 300, 'w': 150, 'h': 20,  'color': (0.7, 0.4, 0.2, 1.0)}, # Plat 2
    {'x': 150, 'y': 220, 'w': 150, 'h': 20,  'color': (0.7, 0.4, 0.2, 1.0)}, # Plat 3
    {'x': 350, 'y': 450, 'w': 40,  'h': 70,  'color': (0.4, 0.4, 0.4, 1.0)}, # Solid Wall Box
]

player = Player(100, 300)
clock = pygame.time.Clock()
running = True

# 4. MAIN GAME LOOP
while running:
    dt = clock.tick_busy_loop() / 1000.0 
    # Cap dt to prevent massive physics skips if the window freezes or drags
    if dt > 0.1: 
        dt = 0.1

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE and player.is_grounded:
                player.vy = player.jump_force 

    # Continuous movement key scan
    keys = pygame.key.get_pressed()
    player.vx = (keys[K_RIGHT] - keys[K_LEFT]) * player.speed

    # Update Physics
    player.update(dt, platforms)

    # Render Phase
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    for plat in platforms:
        draw_platform(plat)
        
    player.draw()

    pygame.display.flip()
    glFinish()
    #clock.tick(60)

pygame.quit()
