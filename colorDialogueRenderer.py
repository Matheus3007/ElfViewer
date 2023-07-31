import pygame
import sys

def display_color_dialogue_test(theme):
    pygame.init()
    EXAMPLE_SIDE = 50

    keys = list(theme.keys())
    colors = [theme[key] for key in keys if key != "background"]
    descriptions = [key for key in keys if key != "background"]
    num_colors = len(colors)

    screen = pygame.display.set_mode((300, num_colors*EXAMPLE_SIDE))
    pygame.display.set_caption("Color Dialogue")
    
    font = pygame.font.SysFont(None, 20)
      
    while True:
        ## Fills background with gray
        screen.fill(theme["background"])
        pygame.draw.rect(screen, theme["background"],(0, 0, EXAMPLE_SIDE * 10, num_colors*EXAMPLE_SIDE))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        
        for i in range(num_colors):
            pygame.draw.rect(screen, colors[i], (0, i*EXAMPLE_SIDE, EXAMPLE_SIDE, EXAMPLE_SIDE))
            # writes description of color
            text = font.render(descriptions[i], True, (0, 0, 0))
            screen.blit(text, (EXAMPLE_SIDE+10, (i*(EXAMPLE_SIDE))+20))
        
        pygame.display.update()

def display_color_dialogue(theme, screen):
    EXAMPLE_SIDE = 50
    keys = list(theme.keys())
    colors = [theme[key] for key in keys if key != "background"]
    descriptions = [key for key in keys if key != "background"]
    num_colors = len(colors)

    pygame.display.set_caption("Color Dialogue")
    
    font = pygame.font.SysFont(None, 20)      
    pygame.draw.rect(screen, theme["background"],(5, 5, (EXAMPLE_SIDE * 5)+10, (num_colors*EXAMPLE_SIDE)+10))  
    for i in range(num_colors):
        pygame.draw.rect(screen, colors[i], (10, (i*EXAMPLE_SIDE)+10, EXAMPLE_SIDE, EXAMPLE_SIDE))
        # writes description of color
        text = font.render(descriptions[i], True, (255, 255, 255))
        screen.blit(text, (EXAMPLE_SIDE+15, (i*(EXAMPLE_SIDE))+30))
