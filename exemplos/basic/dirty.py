import pygame
import random

# Initialize pygame-ce
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5
GRAVITY = 0.8
JUMP_FORCE = -16

# Layer constants for performance rendering
BACKGROUND_LAYER = 0
BLOCK_LAYER = 1
PLAYER_LAYER = 2

class Background(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill((30, 30, 40)) # Dark blue-gray
        # Draw some static stars
        for _ in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            pygame.draw.circle(self.image, (100, 100, 150), (x, y), 2)
        self.rect = self.image.get_rect()
        self.dirty = 1 # Draw once initially
        self._layer = BACKGROUND_LAYER

class Block(pygame.sprite.DirtySprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((70, 140, 70)) # Green platforms
        pygame.draw.rect(self.image, (100, 200, 100), (0, 0, w, h), 3) # Border
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dirty = 1 # Static block, render once
        self._layer = BLOCK_LAYER

class Player(pygame.sprite.DirtySprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (230, 80, 80), (0, 0, 40, 60)) # Red player
        pygame.draw.rect(self.image, (255, 255, 255), (8, 12, 8, 8)) # Left eye
        pygame.draw.rect(self.image, (255, 255, 255), (24, 12, 8, 8)) # Right eye
        
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.platforms = platforms
        
        # Physics variables
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        
        # Track previous rect to erase accurately via LayeredDirty
        self.old_rect = self.rect.copy()
        self._layer = PLAYER_LAYER
        self.dirty = 2 # Always dirty (moves every frame)

    def update(self):
        self.old_rect = self.rect.copy()
        
        # Apply gravity
        self.vy += GRAVITY
        if self.vy > 15:
            self.vy = 15

        # Horizontal movement
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = PLAYER_SPEED

        # Move horizontally
        self.rect.x += self.vx
        self.handle_collision(0)

        # Move vertically
        self.rect.y += self.vy
        self.handle_collision(1)
        
        # Keep inside window bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def handle_collision(self, direction):
        # direction 0 = horizontal, 1 = vertical
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in hits:
            if direction == 0: # Horizontal
                if self.vx > 0:
                    self.rect.right = block.rect.left
                elif self.vx < 0:
                    self.rect.left = block.rect.right
            elif direction == 1: # Vertical
                if self.vy > 0:
                    self.rect.bottom = block.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = block.rect.bottom
                    self.vy = 0

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False

def main():
    # Setup high-performance display mode
    # SCALED automatically scales window size smoothly
    # RESIZABLE allows switching window sizes without flickering
    flags = pygame.SCALED | pygame.RESIZABLE
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, vsync=1)
    pygame.display.set_caption("pygame-ce Smooth 2D Platformer (DirtySprites)")
    
    clock = pygame.time.Clock()
    fullscreen = False

    # Create Group Managed via LayeredDirty for automated optimization
    all_sprites = pygame.sprite.LayeredDirty()
    platforms = pygame.sprite.Group()

    # Add background
    bg = Background()
    all_sprites.add(bg)

    # Build Map Platforms
    level_layout = [
        Block(0, HEIGHT - 40, WIDTH, 40), # Floor
        Block(100, 450, 200, 20),
        Block(450, 380, 250, 20),
        Block(250, 250, 200, 20),
        Block(50, 150, 150, 20),
    ]
    for block in level_layout:
        platforms.add(block)
        all_sprites.add(block)

    # Add Player
    player = Player(platforms)
    all_sprites.add(player)

    # Main Game Loop
    running = True
    while running:
        # Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
                # Seamless toggle without tearing/flickering using pygame.display.toggle_fullscreen()
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    pygame.display.toggle_fullscreen()

        # Update Phase
        all_sprites.update()

        # Render Phase - DirtyRect updating saves CPU/GPU time by partial clearing
        rects = all_sprites.draw(screen)
        pygame.display.update(rects)

        # Enforce Framerate (60 FPS synced with VSync)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()