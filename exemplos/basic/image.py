import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

surface = pygame.image.load("assets/image/player.png").convert_alpha()
surface = pygame.transform.smoothscale_by(surface, 5)

while running:    
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    #desenhe algo
    screen.blit(surface, (100,100))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()