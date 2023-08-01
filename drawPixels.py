import pygame, sys
from typeChooser import typeChooser
from objDumpParser import parse_objdump
from pygame.locals import *
from pygame import gfxdraw
import sys

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

def highlight_virtpixel_border(surface, virtPixelSize, color, index, screenX):
    line = (index//(screenX//virtPixelSize))
    column = (index%(screenX//virtPixelSize))
    xCorner = column * virtPixelSize
    yCorner = line * virtPixelSize
    # Draws a border around the pixel starting in xCorner, yCorner with virtPixelSize as a side and using pygame rect
    pygame.draw.rect(surface, color, (xCorner, yCorner, virtPixelSize, virtPixelSize), 2)
    return xCorner, yCorner, xCorner+virtPixelSize, yCorner+virtPixelSize
