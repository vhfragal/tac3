import pygame
from ..constants import *
from ..utils import utils
from ..config.sounds import sounds
from ..display import display
from ..ui.cenario import Cenario


class Player():
    """Classe que gerencia o personagem, suas físicas básicas e inputs."""
    def __init__(self, map_w:int, map_h:int, pos:tuple[int,int]):
        self.MAP_WIDTH = map_w
        self.MAP_HEIGHT = map_h
       
        self.frame_index = 0
        self.frame_speed = 16
        self.current_frame = 0.0
        
        self.textures_walk_right = []        
        self.textures_walk_left = []        
        self.textures_jump_right = []
        self.textures_jump_left = []
        
        for i in range(14):
            img = pygame.image.load(f"assets/image/walk/frame{i:04d}.png").convert_alpha()
            img = pygame.transform.smoothscale(img, SIZE_PLAYER)    
            img_mirror = pygame.transform.flip(img, True, False)            
            self.textures_walk_right.append(utils.surface_to_texture(img))            
            self.textures_walk_left.append(utils.surface_to_texture(img_mirror))

        # jump 
        for i in range(1,4):
            img = pygame.image.load(f"assets/image/walk/jump{i}.png").convert_alpha()
            img = pygame.transform.smoothscale(img, SIZE_PLAYER)    
            img_mirror = pygame.transform.flip(img, True, False)            
            self.textures_jump_right.append(utils.surface_to_texture(img))
            self.textures_jump_left.append(utils.surface_to_texture(img_mirror))


        self.image = img
        self.rect = pygame.Rect(0, 0, SIZE_PLAYER[0], SIZE_PLAYER[1])
        self.rect.topleft = pos
        
        #self.texture_stand_right = self.textures_walk_right[0]
        #self.texture_stand_left = self.textures_walk_left[0]

        img = pygame.image.load(f"assets/image/walk/stand.png").convert_alpha()
        img = pygame.transform.smoothscale(img, SIZE_PLAYER) 
        pygame.draw.rect(img, "blue", (0, 0, self.rect.w, self.rect.h), 2)
        self.texture_stand = utils.surface_to_texture(img)
        

        # collision rect
        self.rect_colli = img.get_rect()        
        self.rect_colli.midbottom = self.rect.midbottom        
        self.img_colli = pygame.Surface(SIZE_PLAYER, pygame.SRCALPHA)
        #self.img_colli.fill("black")
        self.img_colli = pygame.transform.smoothscale(self.img_colli, SIZE_PLAYER)
        pygame.draw.rect(self.img_colli, "red", (0, 0, self.rect.w, self.rect.h), 2)
        diff_x = (self.rect_colli.x - self.rect.x) // 2
        diff_y = (self.rect_colli.y - self.rect.y) // 2
        pygame.draw.rect(self.img_colli, "green", (diff_x, diff_y, self.rect_colli.w, self.rect_colli.h), 2)
        self.texture_img_colli = utils.surface_to_texture(self.img_colli)


        img = pygame.image.load(f"assets/image/walk/jump_stand.png").convert_alpha()
        img = pygame.transform.smoothscale(img, SIZE_PLAYER) 
        self.texture_jump_stand = utils.surface_to_texture(img)
         
        # Vetores de movimento e física
        self.direction = pygame.math.Vector2(0, 0)
        # Use floats for exact sub-pixel positions
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.vel = pygame.math.Vector2(0, 0)
        
        # movement
        self.speed_boost = 1.5        
        self.speed_walk = 300
        self.speed_jump = -900        
        self.on_ground = False
        self.gravity = 1400

        # change jump 
        self.jump_max_sprite = (display.size[1]*TILE_SIZE) + TILE_SIZE # chao        
        self.jump_min_sprite = self.jump_max_sprite + (0.1* self.speed_jump)
        
        self.prev_key = pygame.key.get_pressed()     

        # limits of player movement - change camera
        self.rect_limit_up = pygame.Rect((0,display.h*0.9), (display.w,1))
        self.rect_limit_down = pygame.Rect((0,display.h*0.3), (display.w,1))
        self.rect_limit_left = pygame.Rect((display.w*0.5,0), (1,display.h))
        self.rect_limit_right = pygame.Rect((display.w*0.3,0), (1,display.h))

        # score
        self.score = 0
        self.life = 100
        self.max_life = 100
        self.hit = False
        self.hit_counter = 0
        self.hit_delay = 50
        self.text_count = 0
        self.message = ""
        
        # speak
        self.speak_delay = 100
        self.speak_count = 0
  

   
    def handle_input(self):
        key = pygame.key.get_pressed()
        self.vel.x = 0

        # Movimentação Horizontal
        if key[pygame.K_LEFT] or key[pygame.K_a]: self.direction.x = -1        
        elif key[pygame.K_RIGHT] or key[pygame.K_d]: self.direction.x = 1
        else: self.direction.x = 0

        # walk 
        self.vel.x = self.direction.x * self.speed_walk
        # run
        if key[pygame.K_LCTRL]:            
            self.vel.x *= self.speed_boost            


    def physics_step(self, dt:float, colliders:list[pygame.Rect]):
        # gravity           
        if self.vel.y > 0: 
            self.direction.y = 1           
        elif self.vel.y < 0: 
            self.direction.y = -1
        else: self.direction.y = 0
        self.vel.y += self.gravity * dt 

        # movement X     
        if self.rect.x < 0: 
            self.pos.x = 0 
        elif self.rect.x > self.MAP_WIDTH - self.rect.w: 
            self.pos.x = self.MAP_WIDTH - self.rect.w  
        else: 
            self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)
        self.check_collision_x(colliders)

        # movement Y
        if self.rect.y != round(self.pos.y):            
            self.on_ground = False
        if self.rect.y > self.MAP_HEIGHT - self.rect.h:
            self.pos.y = self.MAP_HEIGHT - self.rect.h           
            self.vel.y = 0
            self.on_ground = True
        else:
            self.pos.y += self.vel.y * dt
        
        self.rect.y = round(self.pos.y)
        self.check_collision_y(colliders)
        
        self.rect_colli.midbottom = self.rect.midbottom


    def check_collision_x(self, colliders:list[pygame.Rect]):
        for platform in colliders:
            if self.rect.colliderect(platform):
                #if self.rect.bottom - platform.top <= 2 and self.vel.y >= 0:
                #    print(self.rect, self.rect_colli)
                #    continue
                if self.vel.x > 0:  # Moving right; hit left side of platform
                    self.rect.right = platform.left
                    self.vel.x = 0
                elif self.vel.x < 0:  # Moving left; hit right side of platform
                    self.rect.left = platform.right
                    self.vel.x = 0

                # Sync float position with corrected Rect position
                self.pos.x = self.rect.x

    def check_collision_y(self, colliders:list[pygame.Rect]):
        for platform in colliders:
            if self.rect.colliderect(platform):                
                if self.vel.y > 0:  # Falling down; hit top of platform
                    self.rect.bottom = platform.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:  # Jumping up; hit bottom of platform
                    self.rect.top = platform.bottom
                    self.vel.y = 0

                # Sync float position with corrected Rect position
                self.pos.y = self.rect.y


    def update(self, dt):        
        self.update_frame(dt)
       

       

    def update_frame(self, dt):
        current_frame = self.current_frame
        # atualizar indice animação
        current_frame += self.frame_speed * dt
        if current_frame >= len(self.textures_walk_right):
            current_frame = 0
        self.frame_index = int(current_frame)

        self.current_frame = current_frame

        

    def draw(self):
        #x,y,w,h = self.rect.x, self.rect.y, self.rect.w, self.rect.h 
       
        texture = self.texture_stand 
        if not self.on_ground:    # pulando
            texture = self.texture_jump_stand
            if self.direction.x == 1:   # direita
                if self.direction.y > 0: # descendo
                    if self.jump_min_sprite <= self.rect.bottom <= self.jump_max_sprite:
                        texture = self.textures_jump_right[2]
                    else: texture = self.textures_jump_right[1]
                else: # subindo
                    if self.jump_min_sprite <= self.rect.bottom <= self.jump_max_sprite:
                        texture = self.textures_jump_right[0]
                    else: texture = self.textures_jump_right[1]
            elif self.direction.x == -1:    # esquerda
                if self.direction.y > 0: # descendo
                    if self.jump_min_sprite <= self.rect.bottom <= self.jump_max_sprite:
                        texture = self.textures_jump_left[2]
                    else: texture = self.textures_jump_left[1]
                else: # subindo
                    if self.jump_min_sprite <= self.rect.bottom <= self.jump_max_sprite:
                        texture = self.textures_jump_left[0]
                    else: texture = self.textures_jump_left[1] 
        else:   # chao
            if self.direction.x == 1:
                texture = self.textures_walk_right[self.frame_index]
            elif self.direction.x == -1:
                texture = self.textures_walk_left[self.frame_index]        
        utils.draw_textured_quad(texture, *self.rect)

        #if debug:
        utils.draw_textured_quad(self.texture_img_colli, *self.rect_colli)