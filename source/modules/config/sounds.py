import pygame
import os

class Sounds():
    def __init__(self):        
        # Pre-initialize mixer with a 512 or 1024 buffer to minimize CPU timing interruptions
        #pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()

    def load_assets(self): 
        self.nr_channels = pygame.mixer.get_num_channels() 
        self.g_channel = 1  # reserving channel 0 for prioritized sounds

        self.sound_wow = pygame.mixer.Sound(os.path.abspath('assets/sounds/Wow.wav'))
        self.sound_wow.set_volume(0.1)

        self.sound_jump = pygame.mixer.Sound(os.path.abspath('assets/sounds/jump.wav'))
        self.sound_jump.set_volume(0.3)

        self.sound_j1 = pygame.mixer.Sound(os.path.abspath('assets/sounds/j1.wav'))
        self.sound_j1.set_volume(0.3)

        self.sound_j2 = pygame.mixer.Sound(os.path.abspath('assets/sounds/j2.wav'))
        self.sound_j2.set_volume(0.3)

        self.sound_j3 = pygame.mixer.Sound(os.path.abspath('assets/sounds/j3.wav'))
        self.sound_j3.set_volume(0.3)

        self.sound_jump_list = [self.sound_j1, self.sound_j2, self.sound_j3]

        #pygame.mixer.music.load(os.path.abspath('assets/sounds/Smooth Criminal.wav'))
        pygame.mixer.music.load(os.path.abspath('assets/sounds/_LAmourToujours.mp3'))


    #def play_music(self):    
    #    pygame.mixer.music.load(os.path.abspath('assets/sounds/Smooth Criminal.wav'))    
    #    pygame.mixer.music.play(-1, 0.0)
    #    pygame.mixer.music.set_volume(0.2)



    def play_menu_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/sounds/Billie Jean.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.2)

    def play_new_game_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/sounds/Smooth Criminal.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.2)


    def play_sound(self,
                    sound:pygame.mixer.Sound,
                    channel:int=-1):
        # plays a game sound on the next channel (all channels used in order).
        # if channel not specified, sounds will be missed as sometimes all channels are busy 
        # - rotates through channels.
        g_channel = self.g_channel
        if channel == -1:
            ch = pygame.mixer.Channel(g_channel)
            g_channel += 1  # move to next channel
            if g_channel == self.nr_channels:
                g_channel = 1
        else:
            ch = pygame.mixer.Channel(channel)        
        ch.play(sound)
        self.g_channel = g_channel

sounds = Sounds()