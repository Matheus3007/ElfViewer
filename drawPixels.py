import pygame, sys
from typeChooser import typeChooser
from objDumpParser import parse_objdump
from pygame.locals import *
from pygame import gfxdraw
import sys
import importlib



# Parameters
# For small dumps


# Methods
def drawVirtPixel(surface, xOrigin, yOrigin, color, newSize):
    for x in range(newSize):
        for y in range(newSize):
            if (x==0 or y==0 or x==newSize-1 or y ==newSize-1):
                #gfxdraw.pixel(surface, (newSize*xOrigin)+x, (newSize*yOrigin)+y, (0,0,0))
                gfxdraw.pixel(surface, (newSize*xOrigin)+x, (newSize*yOrigin)+y, color)
            else:
                gfxdraw.pixel(surface, (newSize*xOrigin)+x, (newSize*yOrigin)+y, color)

def get_instructio_by_memory_index(lst, index):
    for item in lst:
        if 'memory_index' in item and item['memory_index'] == index:
            return item
    return "No relative Index"  # Return None if the item with the specified index is not found

def get_instruction_by_address(lst, address):
    for item in lst:
        if 'address' in item and item['address'] == address:
            return item
    return "No address"  # Return None if the item with the specified index is not found

def coord(pos, screenX, screenY, virtPixelSize):
    y=pos//(screenY//virtPixelSize)
    x=pos%(screenY//virtPixelSize)
    return (x,y)

def fillRegion(surface, start, end, color, screenX, screenY, virtPixelSize):
    size = end - start
    lineCount = size//(screenY//virtPixelSize)
    for pos in range(start, end):     
        x, y = coord(pos, screenX, screenY, virtPixelSize)
        drawVirtPixel(surface, x, y, color, virtPixelSize)

def drawPixelRelative(surface, spot, color, screenX, screenY, virtPixelSize):
    fillRegion(surface, spot, spot+1, color, screenX, screenY, virtPixelSize)

def display_dialogue_box(text, position, screen):
    font = pygame.font.Font(None, 24)
    dialogue_text = font.render(text, True, (0, 0, 0))
    screen.set_at(position, (255, 255, 255))
    ## Draws the box to the left of the cursor if beyond middle of screen
    if position[0] > screen.get_width() / 2:
        dialogue_box = dialogue_text.get_rect(topright=position)
    else:
        dialogue_box = dialogue_text.get_rect(topleft=position)
    
    
    # Draws the box background
    box_width = dialogue_text.get_width() + 10
    box_height = dialogue_text.get_height() + 10
    if position[0] > screen.get_width() / 2:
        dialogue_box_background = pygame.Rect((position[0]-box_width+10, position[1]+2), (box_width, box_height))
    else:
        dialogue_box_background = pygame.Rect(position, (box_width, box_height))
    pygame.draw.rect(screen, (255,255,255), dialogue_box_background)
    
    # Draws the text
    screen.blit(dialogue_text, dialogue_box.move(5, 5))
    pygame.display.flip()

'''
default_theme = "DebuggersDream"
theme_arg = sys.argv[1] if len(sys.argv) > 1 else default_theme
try:
    # Load the selected theme module dynamically
    theme_module = importlib.import_module(f"themes.{theme_arg}")
    groupColor = theme_module.theme
    theme_name = theme_module.name
except ImportError:
    print("Invalid theme selection.")
    sys.exit(1)

default_params = "average"
params_arg = sys.argv[2] if len(sys.argv) > 2 else default_params
try:
    # Load the selected theme module dynamically
    param_module = importlib.import_module(f"renderParams.{params_arg}")
    virtPixelSize = param_module.renderParams["virtPixelSize"]
    screenX = param_module.renderParams["screenX"]
    screenY = param_module.renderParams["screenY"]
    fillColor = param_module.renderParams["fillColor"]
    borderColor = param_module.renderParams["borderColor"]
except ImportError:
    print("Invalid render parameter selection.")
    sys.exit(1)

# Reads input with objdump file name and parses it
objdumpFileName = input("Enter objdump file name: ")
instructions = parse_objdump(objdumpFileName)
icon = pygame.image.load("bruninho.jpg")
pygame.init()
pygame.display.set_caption("ElfoViewer")
pygame.display.set_icon(icon)
DISPLAYSURF = pygame.display.set_mode((screenX, screenY))



drawVirtPixel(DISPLAYSURF, 0,0,fillColor ,virtPixelSize)
drawVirtPixel(DISPLAYSURF, 1,1,fillColor,virtPixelSize)
fillRegion(DISPLAYSURF, 0, 123, fillColor)
fillRegion(DISPLAYSURF, 124, 130, (0,255,0))
fillRegion(DISPLAYSURF, 140, 2000, (0,0,255))
fillRegion(DISPLAYSURF, 2500, 3000, (0,255,255))

fillRegion(DISPLAYSURF, 3200, 3201, (0,255,255))
fillRegion(DISPLAYSURF, 3201, 3202, ((0,0,255)))
drawPixelRelative(DISPLAYSURF, 3202, (0,255,0))


# Relates each group to a color

# Draws each instruction in the screen
for instruction in instructions:
    color = groupColor[instruction['group']]
    drawPixelRelative(DISPLAYSURF, instruction['memory_index'], color)

dialogue_box_active = False
dialogue_box_text = ""
dialogue_box_position = (0, 0)
dialogue_box_timer = 0


while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()

            print("Mouse clicked at coordinates:", mouse_pos)
            # prints mouse x and y coords to shell
            x = mouse_pos[0]
            y = mouse_pos[1]
            # finds which pixel was clicked on
            pixelX = (x//(virtPixelSize))
            pixelY = (y//(virtPixelSize)) 
            clickIndex = (screenX//virtPixelSize * (pixelY)) + pixelX
            print("Pixel clicked at coordinates:", pixelX, pixelY)
            print("Index:", clickIndex)
            clickedInstruction = get_instructio_by_memory_index(instructions, clickIndex)
            print("Instruction:", clickedInstruction)
            mnemonic = clickedInstruction['instruction']
            address = clickedInstruction['address']
            dialogue_content = "Address: " +"0x"+ address + " | " + "Instruction: " + mnemonic
            if not dialogue_box_active:
                dialogue_box_text = "This is a sample dialogue."
                dialogue_box_position = event.pos
                dialogue_box_active = True
                dialogue_box_timer = pygame.time.get_ticks()
                
            elif dialogue_box_active:
                dialogue_box_active = False
                
    DISPLAYSURF.fill(groupColor['background'])
    for instruction in instructions:
        color = groupColor[instruction['group']]
        drawPixelRelative(DISPLAYSURF, instruction['memory_index'], color)
    if dialogue_box_active:
        
        display_dialogue_box(dialogue_content, dialogue_box_position, DISPLAYSURF)


    pygame.display.update()
'''