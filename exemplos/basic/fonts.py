import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Initialize a font (system default or custom font file)
#font = pygame.font.SysFont("arial", 50)
font = pygame.font.Font("assets/fonts/Call of Ops Duty II.otf", 50)
#font = pygame.font.Font("assets/fonts/FreeSans.ttf", 50)


while running:    
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    #desenhe algo
    fps_text = f"FPS:{str(int(clock.get_fps()))}"
    fps_surface = font.render(fps_text, True, pygame.Color("green")) 
    screen.blit(fps_surface, (10, 10))
   

    pygame.display.flip()
    clock.tick(60)

pygame.quit()