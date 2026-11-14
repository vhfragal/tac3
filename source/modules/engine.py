import pygame
from .display import display
from .game import game
from .events.input import inputs
from OpenGL.GL import *
from .config.sounds import sounds
from .ui.menu import *
#from .constants import *
import threading
from .maker.main_loop import level_maker
from .events.collision import check_collision

class GameEngine:
    """A Engine Pura: Controla o ciclo de vida, janelas, eventos e loops."""
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 32, 512)
        pygame.init() # load all modules     
        #pygame.mixer.set_num_channels(32)  
        #pygame.joystick.init()        
        pass
             

    def run(self):
        display.create_display()   
        sounds.load_assets()
        game.init_assets()
        #menu.create()        
        #options.create()  

        # main menu - editor or game         
        #game.start()
        """O Game Loop Principal"""
        #self.main_loop()
                
        while not game.running:
            game.camera.reset_camera()            
            self.menu_selector()


    def menu_selector(self):
        menu = Basic_menu_all(MENU_MAIN)
        select = menu.run()
        #print(select)
        
        if select != 0:
            #game.multiplayer = False
            if select == 1:    
                game.start()                    
                self.new_game()
            elif select == 2:
                #game.multiplayer = True
                menu2 = Basic_menu_all(MENU_MULTIPLAYER)
                select = menu2.run()
                if select == 3:
                    select = menu.run()
                elif select == 1:
                    pass
                    # server
                    #game.server = True
                    #threading.Thread(target=self.server_thread).start()self.new_game()       
                elif select == 2:
                    pass
                    # cliente     
                    #game.client = True
                    #threading.Thread(target=self.client_thread).start()self.new_game()
            elif select == 3:            
                select = menu.run()
            elif select == 4:
                pygame.mouse.set_visible(True)
                #editor = Editor()
                #editor.run()
                level_maker()
                #select = menu.run()
            elif select == 5:
                #self.exit()
                game.stop()
    
    '''def server_thread(self):
        game.server_socket = AppServer("0.0.0.0", 5041)
        game.server_socket.server_listen()
        
    def client_thread(self): 
        with open("Jackson/host.txt", "r") as arq:
            ip = arq.read() 
        game.client_socket = AppClient(ip,  5041, 20)       
        game.client_socket.connect_server()  
        game.client_socket.receive_messages()'''


    def new_game (self):
        # Ocultando o cursor 
        pygame.mouse.set_visible(False)

        #while True:    # laço externo do game over
        # Configurando o começo do jogo.             
        
        
        #self.player = Player(game.WIDTH*0.1, (game.map_lin-3)*game.tile) 
        '''self.player2 = None           
        #self.player2 = None
        if game.multiplayer:
            self.life_counter2 = 0
            self.life_delay2 = 20
            self.life_show2 = True
            self.player2 = Player2(game.WIDTH*0.1, (game.map_lin-3)*game.tile)'''
                                
        self.main_loop()
        
        # Parando o jogo e mostrando a tela final.            
        '''if len(self.enemies) == 0: 
            boom = NiceEffect()
            boom.fireworks(self.cenario, self.cenario_rect)                
            self.__menu_win__()
        else: self.__menu_last__()'''



    def main_loop(self):        
        #try:           
        while game.running:
            # guards
            #if not self.cenario_rect: return    # dead
            #if len(self.enemies) == 0: return   # WIN
            #print("232")
            dt = display.game_tick()                
            self.handle_events()
            self.update(dt)
            self.draw()


            # Draw loop      
            #game.screen.blit(self.cenario, self.cenario_rect) 
            
            '''if game.multiplayer:
                if game.server:                    
                    if game.client_connected:
                        self.player2.update(self.ground, self.hazard, self.cenario_rect, self.loot)  
                        self.draw_panel2()                  
                if game.client:
                    # update cenario, players, items, etc.                   
                    self.player2.update(self.ground, self.hazard, self.cenario_rect, self.loot)
                    self.draw_panel2()'''
                       
            #update game elements 
            #self.update_game()
                                        
            # Panel      
            #self.draw_panel()          
                                              
            #update screen
            #pygame.display.update()
                       
            
            
        #except Exception as e:
        #    print(e)            # log here
        #    game.stop()


    def handle_events(self):
        """Loop de Eventos: Inputs globais do sistema e interrupções"""
        #net_thread = threading.Thread(
        #    target=inputs, args=()
        #)
        #net_thread.daemon = True
        #net_thread.start()
        inputs()


    def update(self, dt):
        """Loop de Atualização: Onde a lógica matemática acontece"""
        # new thread!       
        game.update(dt)
        #check_collision()
        
            
    def draw(self):
        """Loop de Renderização: Onde desenhamos na tela"""   
        # ordem importa - cada layer por vez - pode organizar
        game.draw()

        pygame.display.flip()
        # forçar sincronização de hardware CPU e GPU - chamadas assincronas
        #glFinish()
        
engine = GameEngine() # singleton 