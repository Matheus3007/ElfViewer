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

# Reads input with objdump file name and parses it
objdumpFileName = input("Enter objdump file name: ")
instructions = parse_objdump(objdumpFileName)

pygame.init()
pygame.display.set_caption("ElfoViewer")
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

    pygame.display.update()