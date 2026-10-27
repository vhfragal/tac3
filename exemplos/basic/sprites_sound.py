import pygame
import logging
import os

SCALE = 3
WIDTH, HEIGHT = (640*SCALE, 360*SCALE)
FPS = 60
BG_COLOR = pygame.Color("#74777481")
RED_ALPHA = (255, 75, 75, 120)    # 120 / 255 opacity
GREEN = (75, 255, 150)
PLAYER_SIZE = (25*SCALE,50*SCALE)


pygame.init()
flags = pygame.FULLSCREEN | pygame.SCALED
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, vsync=1)
clock = pygame.time.Clock()
running = True

# log type(prio) debug(10), info(20), warning(30), error(40), critical(50)     
logging.basicConfig(
    filename="game.log",
    filemode="w",  # 'a' appends to existing logs; 'w' overwrites the file every run
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


nr_channels = pygame.mixer.get_num_channels() 
g_channel = 1  # reserving channel 0 for prioritized sounds

sound_wow = pygame.mixer.Sound(os.path.abspath('assets/sounds/Wow.wav'))
sound_wow.set_volume(0.3)

pygame.mixer.music.load(os.path.abspath('assets/sounds/Smooth Criminal.wav'))
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.3)

def play_sound(sound:pygame.mixer.Sound,
               channel:int=-1):
        # plays a game sound on the next channel (all channels used in order).
        # if channel not specified, sounds will be missed as sometimes all channels are busy 
        # - rotates through channels.
        global g_channel
        if channel == -1:
            ch = pygame.mixer.Channel(g_channel)
            g_channel += 1  # move to next channel
            if g_channel == nr_channels:
                g_channel = 1
        else:
            ch = pygame.mixer.Channel(channel)        
        ch.play(sound)


surface = pygame.Surface(PLAYER_SIZE, flags=pygame.SRCALPHA)
rect = surface.get_frect()
rect.center = (WIDTH//2, HEIGHT//2)
try:
    frames = []
    for i in range(1,21):
        img = pygame.image.load(f"assets/image/sprites/batch_{i}.png").convert_alpha()
        #img = pygame.transform.smoothscale(img, PLAYER_SIZE)
        img = pygame.transform.smoothscale_by(img, SCALE)
        frames.append(img)
    #img = pygame.image.load("assets/image/player.png")
    #img = pygame.transform.smoothscale(img, PLAYER_SIZE)
    #surface.blit(img)
    #assert len(frames)==19, "Faltando imagens..."
    assert len(frames)==20, "Faltando imagens..."
    logger.info("Player loaded!")
except Exception as e:
    # log error
    logger.exception(e)

pygame.draw.rect(surface, (0,0,0), rect, 3)

frame_index = 0
frame_speed = 0.16
current_frame = 0.0


while running:  
    delta_time = clock.tick(FPS) / 1000.0 

    # tratamento de eventos 
    for event in pygame.event.get():
        # fechar a janela
        if event.type == pygame.QUIT:
            running = False
        # esc para sair...
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # atualizar indice 
    current_frame += frame_speed
    if current_frame >= len(frames):
        current_frame = 0
        play_sound(sound_wow)
    frame_index = int(current_frame)
            
    screen.fill(BG_COLOR)        
    #screen.blit(surface, rect)
    screen.blit(frames[frame_index], rect)
    

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()