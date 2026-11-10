import pygame
import cv2
import pygame.freetype

# Initialize Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Glowing OBJ")


def apply_shadow(surface: pygame.Surface,
                  color:tuple[int,int,int],
                  ksize: tuple[int,int],
                  sigmaX: float) -> pygame.Surface:
    """Applies a bloom effect to a pygame Surface using OpenCV."""
    # Convert Pygame Surface to NumPy array (BGR format for OpenCV)
    obj_array = pygame.surfarray.array3d(surface) 
    
    # Apply Gaussian Blur for initial glow
    obj_array = cv2.cvtColor(obj_array, cv2.COLOR_RGB2BGR)
    blurred_obj = cv2.GaussianBlur(obj_array, ksize, sigmaX)
            
    # Convert back to Pygame Surface
    bloomed_surface = pygame.surfarray.make_surface(cv2.cvtColor(blurred_obj, cv2.COLOR_BGR2RGB))     
    #bloomed_surface.set_colorkey((255,255,255))
    bloomed_surface = bloomed_surface.convert_alpha()

    # change alpha
    pixels = pygame.surfarray.pixels3d(bloomed_surface)
    alphas = pygame.surfarray.pixels_alpha(bloomed_surface)

    for y in range(bloomed_surface.get_height()):
        for x in range(bloomed_surface.get_width()):            
            white_percent = (int(pixels[x,y,0]) + int(pixels[x,y,1]) + int(pixels[x,y,2]))          
            alpha = int(255 * ((white_percent)/(765)))
            alphas[x, y] = alpha
            pixels[x,y,0] = color[0]
            pixels[x,y,1] = color[1]
            pixels[x,y,2] = color[2]

    '''# min point
    min_point = 765
    for y in range(bloomed_surface.get_height()):
        for x in range(bloomed_surface.get_width()):
            sum = int(pixels[x,y,0]) + int(pixels[x,y,1]) + int(pixels[x,y,2])
            if sum < min_point:
                min_point = sum

    # white border alpha
    for y in range(bloomed_surface.get_height()):
        for x in range(bloomed_surface.get_width()):            
            soma = (int(pixels[x,y,0]) + int(pixels[x,y,1]) + int(pixels[x,y,2])) - min_point            
            alpha = int(255 * (1-((soma)/(765-min_point))))
            alphas[x, y] = alpha
            pixels[x,y,0] = color[0]
            pixels[x,y,1] = color[1]
            pixels[x,y,2] = color[2]'''      

    return bloomed_surface


def create_shadow(obj_surf:pygame.Surface,
                   obj_rect:pygame.Rect,
                   shadow_color:tuple[int,int,int],
                   ksize: tuple[int,int],
                   sigmaX: float,
                   shadow_scale:float=1.0):       
    fog = 2     # factor size of fog for shadow        
    # create shadow before loop 
    shadow_size = (obj_rect.width*fog, obj_rect.height*fog)
    shadow_surf = pygame.Surface(shadow_size, pygame.SRCALPHA).convert_alpha()
    #shadow_surf.fill((255,255,255))
    shadow_rect = shadow_surf.get_rect()

    # create mask for shadow
    greater_surf = pygame.transform.rotozoom(obj_surf,0,shadow_scale)
    greater_rect = greater_surf.get_rect()
    greater_rect.center = (shadow_size[0] // 2, shadow_size[1] // 2)
    shadow_mask = pygame.mask.from_surface(greater_surf)
    mask_surf = shadow_mask.to_surface().convert_alpha() #unsetcolor=(255,255,255,0)setcolor=shadow_color

    # create blur img
    obj_rect.center = (shadow_size[0] // 2, shadow_size[1] // 2)
    shadow_surf.blit(mask_surf, greater_rect)
    shadow_surf = apply_shadow(shadow_surf, shadow_color, ksize, sigmaX)

    # debug limit
    #pygame.draw.rect(shadow_surf, (255,255,255), (0,0,shadow_size[0],shadow_size[1]), 1)

    return shadow_surf, shadow_rect 


def load_img_asset(file_img:str,
                    anchor:tuple[int,int],
                    shadow_color:tuple[int,int,int]):
    """Returns tuple for obj and shadow"""
    obj_surf = pygame.image.load(file_img).convert_alpha()
    obj_surf = pygame.transform.smoothscale(obj_surf, (60,100))
    obj_rect = obj_surf.get_rect()

    # param cv2.GaussianBlur()
    ksize = (41,41)
    sigmaX = 11
    shadow_scale = 1.2

    # create shadow
    shadow_surf, shadow_rect = create_shadow(obj_surf, obj_rect, shadow_color,
                                              ksize, sigmaX, shadow_scale)

    # position
    shadow_rect.center = anchor
    obj_rect.center = anchor

    return obj_surf, obj_rect, shadow_surf, shadow_rect 


def load_text_asset(text:str,                    
                    text_color:tuple[int,int,int],
                    anchor:tuple[int,int],
                    shadow_color:tuple[int,int,int]):
    """Returns tuple for obj and shadow"""    
    font = pygame.freetype.Font(None, size=100)
    text_surf, text_rect = font.render(text, text_color)

    # param cv2.GaussianBlur()
    ksize = (21,21)
    sigmaX = 15

    # create shadow
    shadow_surf, shadow_rect = create_shadow(text_surf, text_rect, shadow_color,
                                              ksize, sigmaX)

    # position
    shadow_rect.center = anchor
    text_rect.center = anchor

    return text_surf, text_rect, shadow_surf, shadow_rect 


def load_moon_asset(radius_size:int,                    
                    color:tuple[int,int,int],
                    anchor:tuple[int,int],
                    shadow_color:tuple[int,int,int]):
    """Returns tuple for obj and shadow"""    
    #font = pygame.freetype.Font(None, size=100)
    #text_surf, text_rect = font.render(text, text_color)
    surf = pygame.Surface((radius_size, radius_size), pygame.SRCALPHA)
    rect = pygame.draw.circle(surf, color, ((radius_size//2, radius_size//2)), radius_size//2)
    #rect = surf.get_rect()

    # param cv2.GaussianBlur()
    ksize = (51,51)
    sigmaX = 15

    # create shadow
    shadow_surf, shadow_rect = create_shadow(surf, rect, shadow_color,
                                              ksize, sigmaX)

    # position
    shadow_rect.center = anchor
    rect.center = anchor

    return surf, rect, shadow_surf, shadow_rect 


def apply_shader_color(obj_surf:pygame.Surface,
                            RGBA: tuple[int,int,int,int]):    
    pixels = pygame.surfarray.pixels3d(obj_surf)
    for y in range(obj_surf.get_height()):
        for x in range(obj_surf.get_width()): 
            pixels[x,y,0] = min(RGBA[0],pixels[x,y,0])
            pixels[x,y,1] = min(RGBA[1],pixels[x,y,1])
            pixels[x,y,2] = min(RGBA[2],pixels[x,y,2])


def apply_shader_gradient(obj_surf:pygame.Surface,
                            RGBA1: tuple[int,int,int,int],
                            RGBA2: tuple[int,int,int,int],
                            direction1:str='left',
                            direction2:str='right'):        
    pixels = pygame.surfarray.pixels3d(obj_surf)
    for y in range(obj_surf.get_height()):
        for x in range(obj_surf.get_width()):   
            percent = (x/obj_surf.get_width())          
            pixels[x,y,0] = RGBA1[0]*(1-percent) + RGBA2[0]*(percent)
            pixels[x,y,1] = RGBA1[1]*(1-percent) + RGBA2[1]*(percent)
            pixels[x,y,2] = RGBA1[2]*(1-percent) + RGBA2[2]*(percent)


def apply_shader_alpha(obj_surf:pygame.Surface):        
    alphas = pygame.surfarray.pixels_alpha(obj_surf)
    for y in range(obj_surf.get_height()):
        for x in range(obj_surf.get_width()): 
            alpha = int(255 * (x/(obj_surf.get_width())))
            alphas[x, y] = alpha


def blink_img(surf:pygame.Surface,
              alpha:int,
              switch:bool):
    #print(alpha, switch)
    surf.set_alpha(alpha)
    if switch: alpha += 1
    else: alpha -= 1
    if alpha >= 255: switch = False
    if alpha <= 0: switch = True
    return alpha, switch


# load assets
background_color = (0,0,0)

# file with shadows
file_img = 'assets/image/player.png'
anchor = (screen_width // 2, screen_height // 2)
shadow_color = (225,225,225,255)
obj_surf, obj_rect, shadow_surf, shadow_rect = load_img_asset(file_img, anchor, shadow_color)

# Load font
text = "TAC3"
color = (255,0,0)
anchor = (screen_width // 2, screen_height // 4)
shadow_color = (0,255,0,255)
obj_surf2, obj_rect2, shadow_surf2, shadow_rect2 = load_text_asset(text, color, anchor, shadow_color)

# Load Moon 1
radius = 70
color = (0,0,0)
anchor = (screen_width // 2, screen_height // 1.3)
shadow_color = (220,220,220,255)
obj_surf3, obj_rect3, shadow_surf3, shadow_rect3 = load_moon_asset(radius, color, anchor, shadow_color)

# file with shadows
#file_img = 'example.png'
anchor = (screen_width // 5, screen_height // 2)
shadow_color = (225,225,225,255)
obj_surf4, obj_rect4, shadow_surf4, shadow_rect4 = load_img_asset(file_img, anchor, shadow_color)

# static changes
#apply_shader_color(obj_surf4, (255,0,0,255))
#apply_shader_gradient(obj_surf4, (255,0,0,255), (0,0,255,255))
apply_shader_gradient(obj_surf4, (0,255,0,255), (255,0,255,255))
#apply_shader_alpha(obj_surf4)


# Main game loop
running = True
alpha = 0
switch = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color) # color background    
            
    screen.blit(shadow_surf, shadow_rect) 
    screen.blit(obj_surf, obj_rect)

    screen.blit(shadow_surf2, shadow_rect2) 
    screen.blit(obj_surf2, obj_rect2)

    screen.blit(shadow_surf3, shadow_rect3) 
    screen.blit(obj_surf3, obj_rect3)

    #screen.blit(shadow_surf4, shadow_rect4) 
    screen.blit(obj_surf4, obj_rect4)    

    #dynamic changes
    #alpha, switch = blink_img(obj_surf4, alpha, switch)
    

    pygame.display.flip()

pygame.quit()