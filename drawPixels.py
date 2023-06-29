import pygame, sys
from pygame.locals import *
from pygame import gfxdraw
# Parameters
virtPixelSize = 10
screenX=700
screenY=screenX
color=Color(255,255,255)
# Methods
def drawVirtPixel(surface, xOrigin, yOrigin, color, newSize):
    for x in range(newSize):
        for y in range(newSize):
            if (x==0 or y==0 or x==newSize-1 or y ==newSize-1):
                gfxdraw.pixel(surface, (newSize*xOrigin)+x, (newSize*yOrigin)+y, (0,0,0))
            else:
                gfxdraw.pixel(surface, (newSize*xOrigin)+x, (newSize*yOrigin)+y, color)


def drawRegion(start, end):
    


pygame.init()
DISPLAYSURF = pygame.display.set_mode((screenX, screenY))

DISPLAYSURF.fill((128,128,128))

drawVirtPixel(DISPLAYSURF, 0,0,color ,virtPixelSize)
drawVirtPixel(DISPLAYSURF, 1,1,color,virtPixelSize)

pygame.display.set_caption('Hello World!')
while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
