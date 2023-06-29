import pygame, sys
from pygame.locals import *
from pygame import gfxdraw
# Parameters
virtPixelSize = 10
screenX=virtPixelSize*100
screenY=screenX
fillColor=Color(255,255,255)
borderColor=Color(0,0,0)
# Methods
def drawVirtPixel(surface, xOrigin, yOrigin, color, newSize):
    for x in range(newSize):
        for y in range(newSize):
            if (x==0 or y==0 or x==newSize-1 or y ==newSize-1):
                gfxdraw.pixel(surface, (newSize*xOrigin)+x, (newSize*yOrigin)+y, borderColor)
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
   
pygame.init()
DISPLAYSURF = pygame.display.set_mode((screenX, screenY))

DISPLAYSURF.fill((128,128,128))

drawVirtPixel(DISPLAYSURF, 0,0,fillColor ,virtPixelSize)
drawVirtPixel(DISPLAYSURF, 1,1,fillColor,virtPixelSize)
fillRegion(DISPLAYSURF, 0, 123, fillColor)
fillRegion(DISPLAYSURF, 124, 130, (0,255,0))
fillRegion(DISPLAYSURF, 140, 2000, (0,0,255))
pygame.display.set_caption('Hello World!')
while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()