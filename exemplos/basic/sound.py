import pygame, os

pygame.init()
#pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


nr_channels = pygame.mixer.get_num_channels() 
g_channel = 1  # reserving channel 0 for prioritized sounds

sound_hi = pygame.mixer.Sound(os.path.abspath('assets/sounds/Uh.wav'))
sound_hi.set_volume(0.5)

pygame.mixer.music.load(os.path.abspath('assets/sounds/Bad.wav'))
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


while running:    
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                play_sound(sound_hi)

    screen.fill("gray")

    #desenhe algo

    pygame.display.flip()
    clock.tick(60)

pygame.quit()