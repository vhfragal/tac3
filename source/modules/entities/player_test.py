import pygame
from ..constants import *
from ..utils import utils
from ..config.sounds import sounds
from ..display import display


class Player():
    """Classe que gerencia o personagem, suas físicas básicas e inputs."""
    def __init__(self, x, y):
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
        self.rect = self.image.get_frect(topleft=(x, y))
        #self.texture_stand_right = self.textures_walk_right[0]
        #self.texture_stand_left = self.textures_walk_left[0]

        img = pygame.image.load(f"assets/image/walk/stand.png").convert_alpha()
        img = pygame.transform.smoothscale(img, SIZE_PLAYER) 
        self.texture_stand = utils.surface_to_texture(img)

        img = pygame.image.load(f"assets/image/walk/jump_stand.png").convert_alpha()
        img = pygame.transform.smoothscale(img, SIZE_PLAYER) 
        self.texture_jump_stand = utils.surface_to_texture(img)
         
        # Vetores de movimento e física
        self.direction = pygame.math.Vector2(0, 0)
        
        # movement
        self.speed_boost = 1.5
        self.speed_h = 0  # pixel * delta time
        self.speed_v = 0
        self.speed_walk = 200
        self.speed_jump = 1000
        self.speed_jump_min = 300
        self.onground = False
        self.gravity = 9.8

        # change jump 
        self.jump_max = (display.size[1]*TILE_SIZE) + TILE_SIZE # chao        
        self.jump_min = self.jump_max + (0.08* self.speed_jump)
        
        self.prev_key = pygame.key.get_pressed()     

        # limits of player movement - change camera
        self.rect_up = pygame.Rect((0,display.h*0.9), (display.w,1))
        self.rect_down = pygame.Rect((0,display.h*0.3), (display.w,1))
        self.rect_left = pygame.Rect((display.w*0.5,0), (1,display.h))
        self.rect_right = pygame.Rect((display.w*0.3,0), (1,display.h))

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
  

   
    def get_input(self, dt:float):
        key = pygame.key.get_pressed()
               
        # Movimentação Horizontal
        if key[pygame.K_LEFT] or key[pygame.K_a]: self.direction.x = -1        
        elif key[pygame.K_RIGHT] or key[pygame.K_d]: self.direction.x = 1
        else: self.direction.x = 0

        # walk 
        self.speed_h = self.direction.x * self.speed_walk * dt

        #run
        if key[pygame.K_LCTRL] and self.onground:            
            self.speed_h = self.speed_h * 1.5

        # Pulo
        if (key[pygame.K_UP] or key[pygame.K_w]) and self.onground:
            self.direction.y = -1
            self.speed_v = -self.speed_jump
            self.onground = False
            sounds.play_sound(sounds.sound_jump, 2)
                                      
        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.speed_v < -self.speed_jump_min:
                self.speed_v = -self.speed_jump_min
        self.prev_key = key


    def check_gravity(self):
        # gravity
        '''if self.speed_v < 20 and not self.onground:             
            self.walk_count += 1
            if self.walk_count > self.walk_delay:
                self.v_speed += self.gravity
                self.walk_count = 0'''
        if self.speed_v > 0 and not self.onground:
            self.speed_v += self.gravity 
        if self.onground and self.speed_v > 0:
            self.speed_v = 0
        #if self.onceil:
        #    self.v_speed = self.gravity


    '''def apply_gravity(self, dt:float):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y * dt'''


    def update(self, dt): 
        self.speed_h = 0                
        #self.onground = self.check_collision(0, 1, boxes, "UP")
        #self.onceil = self.check_collision(0, -1, boxes, "DOWN")
        
        self.update_frame(dt)
        self.get_input(dt)
        self.check_gravity()

        #self.speed_h = self.direction.x * self.speed_walk * dt
        self.rect.move_ip([self.speed_h, self.speed_v])


        # Atualiza posição baseada no tempo delta (dt)
        #self.rect.x += self.direction.x * self.speed_walk * dt
        #self.direction.y += self.gravity
        #self.rect.y += self.direction.y * dt

        #all sides- dont go out of screen
        right = self.rect.right > display.w
        left = self.rect.left < 0
        up = self.rect.top < 0
        down = self.rect.bottom > display.h
        '''if right or left:
            self.rect.x -= self.direction.x * self.speed * dt
        if up or down:
            self.rect.y -= self.direction.y * dt'''
        
        # Simulação temporária de colisão com o "chão" da tela        
        floor = (display.size[1]) 
        if self.rect.bottom >= floor:
            self.rect.bottom = floor
            self.direction.y = 0
            self.onground = True


    '''def adjust_move(self, x, y, boxes):
        dx = x
        dy = y    
        while self.check_collision(dx, dy, boxes, "LEFT"):
            dx -= 1
        while self.check_collision(dx, dy, boxes, "RIGHT"):
            dx += 1
        while self.check_collision(dx, dy, boxes, "UP"):            
            dy -= 1
        while self.check_collision(dx, dy, boxes, "DOWN"):
            dy += 1
        self.rect.move_ip([dx, dy])
        return dx, dy'''
    

    def update_frame(self, dt):
        current_frame = self.current_frame
        # atualizar indice animação
        current_frame += self.frame_speed * dt
        if current_frame >= len(self.textures_walk_right):
            current_frame = 0
            #play_sound(sound_wow)
        self.frame_index = int(current_frame)

        self.current_frame = current_frame

        


    def draw(self):
        x,y,w,h = self.rect.x, self.rect.y, self.rect.w, self.rect.h 
        texture = self.texture_stand 
        if not self.onground:    # pulando
            texture = self.texture_jump_stand
            if self.direction.x == 1:   # direita
                if self.direction.y > 0: # descendo
                    if self.jump_min <= self.rect.bottom <= self.jump_max:
                        texture = self.textures_jump_right[2]
                    else: texture = self.textures_jump_right[1]
                else: # subindo
                    if self.jump_min <= self.rect.bottom <= self.jump_max:
                        texture = self.textures_jump_right[0]
                    else: texture = self.textures_jump_right[1]
            elif self.direction.x == -1:    # esquerda
                if self.direction.y > 0: # descendo
                    if self.jump_min <= self.rect.bottom <= self.jump_max:
                        texture = self.textures_jump_left[2]
                    else: texture = self.textures_jump_left[1]
                else: # subindo
                    if self.jump_min <= self.rect.bottom <= self.jump_max:
                        texture = self.textures_jump_left[0]
                    else: texture = self.textures_jump_left[1] 
        else:   # chao
            if self.direction.x == 1:
                texture = self.textures_walk_right[self.frame_index]
            elif self.direction.x == -1:
                texture = self.textures_walk_left[self.frame_index]        
        utils.draw_textured_quad(texture, x,y,w,h)