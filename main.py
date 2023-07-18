import pygame, sys
from typeChooser import typeChooser
from objDumpParser import parse_objdump
from pygame.locals import *
from pygame import gfxdraw
from tqdm import tqdm
#import drawPixels as dp

app_title = '''
Welcome your favourite brand new and improved, elf file visualizer:
--------------------------------------------------------------------------------------------------------------              
   ,ggggggg,                          ,ggg,         ,gg                                                  
 ,dP""""""Y8b ,dPYb, ,dPYb,          dP""Y8a       ,8P                                                   
 d8'    a  Y8 IP'`Yb IP'`Yb          Yb, `88       d8'                                                   
 88     "Y8P' I8  8I I8  8I           `"  88       88  gg                                                
 `8baaaa      I8  8' I8  8'               88       88  ""                                                
,d8P""""      I8 dP  I8 dP     ,ggggg,    I8       8I  gg    ,ggg,   gg    gg    gg    ,ggg,    ,gggggg, 
d8"           I8dP   I8dP     dP"  "Y8ggg `8,     ,8'  88   i8" "8i  I8    I8    88bg i8" "8i   dP""""8I 
Y8,           I8P    I8P     i8'    ,8I    Y8,   ,8P   88   I8, ,8I  I8    I8    8I   I8, ,8I  ,8'    8I 
`Yba,,_____, ,d8b,_ ,d8b,_  ,d8,   ,d8'     Yb,_,dP  _,88,_ `YbadP' ,d8,  ,d8,  ,8I   `YbadP' ,dP     Y8,
  `"Y8888888 8P'"Y88PI8"8888P"Y8888P"        "Y8P"   8P""Y8888P"Y888P""Y88P""Y88P"   888P"Y8888P      `Y8
                     I8 `8,                                                                              
                     I8  `8,                                                                             
                     I8   8I                                                                             
                     I8   8I                                                                             
                     I8, ,8'                                                                             
                      "Y8P'                                                                              
--------------------------------------------------------------------------------------------------------------
'''
print(app_title)
input_file = input("Please enter the name of the file you want to visualize: ")
instructions = parse_objdump(input_file)
