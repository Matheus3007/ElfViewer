import pygame, sys
from typeChooser import typeChooser
from objDumpParser import parse_objdump
from pygame.locals import *
from pygame import gfxdraw
# Parameters
virtPixelSize = 5
screenX=virtPixelSize*200
screenY=screenX
fillColor=Color(255,255,255)
borderColor=Color(0,0,0)

# Methods
def drawVirtPixel(surface, xOrigin, yOrigin, color, newSize):
    for x in range(newSize):
        for y in range(newSize):
            if (x==0 or y==0 or x==newSize-1 or y ==newSize-1):
                #gfxdraw.pixel(surface, (newSize*xOrigin)+x, (newSize*yOrigin)+y, borderColor)
                gfxdraw.pixel(surface, (newSize*xOrigin)+x, (newSize*yOrigin)+y, color)
            else:
                gfxdraw.pixel(surface, (newSize*xOrigin)+x, (newSize*yOrigin)+y, color)

def coord(pos):
    y=pos//(screenY//virtPixelSize)
    x=pos%(screenY//virtPixelSize)
    return (x,y)

def fillRegion(surface, start, end, color):
    size = end - start
    lineCount = size//(screenY//virtPixelSize)
    for pos in range(start, end):     
        x, y = coord(pos)
        drawVirtPixel(surface, x, y, color, virtPixelSize)

def drawPixelRelative(surface, spot, color):
    fillRegion(surface, spot, spot+1, color)

def display_dialogue_box(text, position, screen):
    font = pygame.font.Font(None, 24)
    dialogue_text = font.render(text, True, (0, 0, 0))
    dialogue_box = dialogue_text.get_rect(topleft=position)
    
    # Draw the box background
    box_width = dialogue_text.get_width() + 10
    box_height = dialogue_text.get_height() + 10
    dialogue_box_background = pygame.Rect(position, (box_width, box_height))
    pygame.draw.rect(screen, (255,255,255), dialogue_box_background)
    
    # Draw the text
    screen.blit(dialogue_text, dialogue_box.move(5, 5))
    pygame.display.flip()



# Reads input with objdump file name and parses it
objdumpFileName = input("Enter objdump file name: ")
instructions = parse_objdump(objdumpFileName)
icon = pygame.image.load("bruninho.jpg")
pygame.init()
pygame.display.set_caption("ElfoViewer")
pygame.display.set_icon(icon)
DISPLAYSURF = pygame.display.set_mode((screenX, screenY))

DISPLAYSURF.fill((128,128,128))

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
groupColor = {
    "LOAD STORE": (0,255,0), # COLOR = GREEN
    "BRANCH": (0,0,255), # COLOR = BLUE
    "ALU": (255,0,0), # COLOR = RED
    "COPROCESSOR": (255,255,0), # COLOR = YELLOW
    "LOAD STORE MULTIPLE": (255,0,255),     # COLOR = MAGENTA
    "LOAD STORE INDEXED": (0,255,255),     # COLOR = CYAN
    "UNDEFINED": (0,0,0) # COLOR = GRAY
}
# Draws each instruction in the screen
for instruction in instructions:
    color = groupColor[instruction['group']]
    drawPixelRelative(DISPLAYSURF, instruction['index'], color)

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
            print("Instruction:", instructions[clickIndex])
            mnemonic = instructions[clickIndex]['instruction']
            address = instructions[clickIndex]['address']
            dialogue_content = "Address: " +"0x"+ address + " | " + "Instruction: " + mnemonic
            if not dialogue_box_active:
                dialogue_box_text = "This is a sample dialogue."
                dialogue_box_position = event.pos
                dialogue_box_active = True
                dialogue_box_timer = pygame.time.get_ticks()
                
            elif dialogue_box_active:
                dialogue_box_active = False


    for instruction in instructions:
        color = groupColor[instruction['group']]
        drawPixelRelative(DISPLAYSURF, instruction['index'], color)
    if dialogue_box_active:
        display_dialogue_box(dialogue_content, dialogue_box_position, DISPLAYSURF)

    pygame.display.update()