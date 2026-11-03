import pygame
from ..constants import *
from ..utils import utils
from ..config.sounds import sounds
from ..display import display
import math


class Player():
    """Classe que gerencia o personagem, suas físicas básicas e inputs."""
    def __init__(self, x, y):
        self.w, self.h = SIZE_PLAYER
        self.image = pygame.Surface(SIZE_PLAYER, pygame.SRCALPHA)
        self.image.fill("green")
        self.rect = self.image.get_frect(topleft=(x, y))

        self.texture_id = utils.surface_to_texture(self.image)


        '''self.platforms = [
            pygame.FRect(0, 500, 1200, 50),     # Floor
            pygame.FRect(300, 400, 200, 30),    # Floating platform 1
            pygame.FRect(600, 300, 200, 30),    # Floating platform 2
        ]'''

        #speed_x, speed_y = 200, 0
        #self.pos = pygame.math.Vector2(x, y)
        #self.velocity = pygame.math.Vector2(speed_x, speed_y)


        # Physics & Input Variables
        self.velocity_y = 0
        self.velocity_x = 0
        self.GRAVITY = 0.5
        self.JUMP_STRENGTH = -12
        self.ACCELERATION = 0.8
        self.FRICTION = 0.85
        self.onground = False
        self.camera_x = 0
        ''''''

        
        
        '''self.pos = pygame.math.Vector2(x, y)
        self.speed = pygame.math.Vector2(0, 0)
        self.JUMP = -700
        self.WALK = 400
        self.onground = False
        self.look_direction = 1  # right 1 - left -1

        # --- CONFIGURAÇÕES DA CÂMERA ---
        self.offset_camera = pygame.math.Vector2(self.pos.x - display.w / 2, self.pos.y - display.h / 2)
        self.SMOOTH_X = 4.0           
        self.SMOOTH_Y = 8.0 

        # Configuração do Look Ahead
        # Distância máxima (em pixels) que a câmera vai avançar à frente do jogador
        self.LOOK_AHEAD = 150 '''




        '''self.LERP_FACTOR = 11
        self.pos_current = pygame.math.Vector2(x, y)
        self.pos_target = pygame.math.Vector2(x, y)
       
        # movement
        self.speed_boost = 1.5
        self.speed_h = 0  # pixel * delta time
        self.speed_v = 0
        self.speed_walk = 200
        self.speed_jump = 1000
        self.speed_jump_min = 300
        self.onground = False
        self.gravity = 9.8
        # Vetores de movimento e física
        self.direction = pygame.math.Vector2(0, 0)

        self.prev_key = pygame.key.get_pressed()'''


    def set_map_size(self, map_size:tuple[int,int]):
        self.map_w, self.map_h = map_size


    def update(self, dt): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x -= self.ACCELERATION
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x += self.ACCELERATION
    
        # --- Physics & Platformer Logic ---
        self.velocity_x *= self.FRICTION  # Apply horizontal drag
        self.velocity_y += self.GRAVITY    # Apply gravity
    
        # Horizontal Movement & Collisions
        self.rect.x += self.velocity_x
        '''for plat in self.platforms:
            if self.rect.colliderect(plat):
                if self.velocity_x > 0:
                    self.rect.right = plat.left
                    self.velocity_x = 0
                elif self.velocity_x < 0:
                    self.rect.left = plat.right
                    self.velocity_x = 0'''
    
        # Vertical Movement & Collisions
        self.rect.y += self.velocity_y
        self.onground = False
        '''for plat in self.platforms:
            if self.rect.colliderect(plat):
                if self.velocity_y > 0:  # Falling down
                    self.rect.bottom = plat.top
                    self.velocity_y = 0
                    self.onground = True
                elif self.velocity_y < 0:  # Hitting ceiling
                    self.rect.top = plat.bottom
                    self.velocity_y = 0'''

        # Simulação temporária de colisão com o "chão" da tela        
        floor = (display.size[1]) 
        if self.rect.bottom >= floor:
            self.rect.bottom = floor
            #self.direction.y = 0
            self.onground = True
    
        # --- Camera Scrolling System ---
        # Linear interpolation (lerp) camera tracking the player
        target_camera_x = self.rect.centerx - display.w // 2
        self.camera_x += (target_camera_x - self.camera_x) * 0.1


    def draw(self): 
        # Draw all level platforms (Green)
        #for plat in self.platforms:
        #    utils.draw_rect(plat.x, plat.y, plat.width, plat.height, (46, 204, 113))

        #x,y = (int(self.pos.x - self.offset_camera.x), int(self.pos.y - self.offset_camera.y))
        #w,h = self.rect.w, self.rect.h
        utils.draw_textured_quad(self.texture_id, *self.rect)



    def update3(self, dt): 

        # Captura de inputs contínuos para o pulo dinâmico
        keys = pygame.key.get_pressed()
        press_jump = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]

        # MOVIMENTAÇÃO HORIZONTAL
        self.speed.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed.x = -self.WALK
            self.look_direction = -1 
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed.x = self.WALK
            self.look_direction = 1

        # FÍSICA DO PULO VARIÁVEL (Modificação de Gravidade)
        # Se o jogador está subindo (self.speed.y < 0) mas SOLTOU o botão de pulo...
        if self.speed.y < 0 and not press_jump:
            # Aplicamos a gravidade rápida para cortar a subida imediatamente
            self.speed.y += GRAVITY_EXTRA * dt
        else:
            # Se ele continuar segurando ou já estiver caindo normalmente
            self.speed.y += GRAVITY * dt

        
        # Movimento 
        self.pos.x += self.speed.x * dt
        self.pos.x = max(self.w, min(self.pos.x, self.map_w - self.w))
        self.pos.y += self.speed.y * dt
        self.pos.y = max(self.h, min(self.pos.y, self.map_h - self.h))
        
        self.rect.topleft = self.pos.x - self.w, self.pos.y - self.h
        self.onground = False

        '''for plat in plataforms:
            if rect_jogador.colliderect(plat):
                if self.speed.x > 0: self.pos.x = plat.left - raio_jogador
                if self.speed.x < 0: self.pos.x = plat.right + raio_jogador'''
       
        '''for plat in plataforms:
            if rect_jogador.colliderect(plat):
                if self.speed.y > 0: # Caindo
                    self.pos.y = plat.top - raio_jogador
                    self.speed.y = 0
                    esta_no_chao = True
                if self.speed.y < 0: # Subindo / Batendo a cabeça
                    self.pos.y = plat.bottom + raio_jogador
                    self.speed.y = 0'''
        
        # Simulação temporária de colisão com o "chão" da tela        
        floor = (display.size[1]) 
        if self.rect.bottom >= floor:
            self.rect.bottom = floor
            #self.direction.y = 0
            self.onground = True
        


        # CÂMERA COM LOOK AHEAD
        shift_horizontal = self.look_direction * self.LOOK_AHEAD
        camera_target = pygame.math.Vector2(
            self.pos.x - display.w / 2 + shift_horizontal,
            self.pos.y - (display.h * 0.6)
        )

        factor_time_x = 1.0 - math.exp(-self.SMOOTH_X * dt)
        factor_time_y = 1.0 - math.exp(-self.SMOOTH_Y * dt)
        
        self.offset_camera.x = pygame.math.lerp(self.offset_camera.x, camera_target.x, factor_time_x)
        self.offset_camera.y = pygame.math.lerp(self.offset_camera.y, camera_target.y, factor_time_y)

        # Limites da câmera
        limit_max_x = self.map_w - display.w
        limit_max_y = self.map_h - display.h
        self.offset_camera.x = max(0, min(self.offset_camera.x, limit_max_x))
        self.offset_camera.y = max(0, min(self.offset_camera.y, limit_max_y))
        


        '''self.pos_target.x += self.speed_walk * dt
        time_dt = 1.0 - math.exp(-self.LERP_FACTOR * dt)            
        if self.pos_current.distance_to(self.pos_target) > 0.1:
            self.pos_current = self.pos_current.lerp(self.pos_target, time_dt)
        else:
            self.pos_current = pygame.math.Vector2(self.pos_target)


        #self.pos += self.velocity * dt
        self.rect.topleft = self.pos_current'''

        """self.speed_h = 0
        
        if self.onground: self.speed_v = 0
        else: self.speed_v += self.gravity
      

        key = pygame.key.get_pressed()                       
        
        # Movimentação horizontal
        if key[pygame.K_LEFT] or key[pygame.K_a]: self.direction.x = -1        
        elif key[pygame.K_RIGHT] or key[pygame.K_d]: self.direction.x = 1
        else: self.direction.x = 0
        # walk 
        #print(self.direction.x , self.speed_walk , dt)
        self.speed_h = self.direction.x * self.speed_walk * dt
        #run
        if key[pygame.K_LCTRL] and self.onground: self.speed_h = self.speed_h * 1.5
        # update x pos
        #self.rect.x += self.direction.x * self.speed_h * dt


        # Movimentação vertical
        # Pulo
        if (key[pygame.K_UP] or key[pygame.K_w]) and self.onground:
            #self.direction.y = -1
            self.speed_v = -self.speed_jump
            self.onground = False
            sounds.play_sound(sounds.sound_jump, 2)
                                        
        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.speed_v < -self.speed_jump_min:
                self.speed_v = -self.speed_jump_min
        self.prev_key = key


        '''if self.speed_v > 0 and not self.onground:
            self.speed_v += self.gravity 
        if self.onground and self.speed_v > 0:
            self.speed_v = 0'''


        if self.speed_v > 0: self.direction.y = 1
        elif self.speed_v == 0: self.direction.y = 0
        else: self.direction.y = -1
        # update y pos
        #self.rect.y += self.direction.y * self.speed_v * dt


        #self.speed_h = self.direction.x * self.speed_walk * dt
        self.rect.move_ip([self.speed_h, self.speed_v])


        # Atualiza posição baseada no tempo delta (dt)
        #self.rect.x += self.direction.x * self.speed_walk * dt
        #self.direction.y += self.gravity
        #self.rect.y += self.direction.y * dt

        # Simulação temporária de colisão com o "chão" da tela        
        floor = (display.size[1]) 
        if self.rect.bottom >= floor:
            self.rect.bottom = floor
            #self.direction.y = 0
            self.onground = True"""



    def draw3(self):
        x,y = (int(self.pos.x - self.offset_camera.x), int(self.pos.y - self.offset_camera.y))
        w,h = self.rect.w, self.rect.h
        utils.draw_textured_quad(self.texture_id, x,y,w,h)

        
        
        '''self.frame_index = 0
        self.frame_speed = PLAYER_FRAME_SPEED
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
        self.speak_count = 0'''
  

   
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


    def update2(self, dt): 
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

        


    def draw2(self):
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