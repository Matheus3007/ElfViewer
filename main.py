import pygame, sys
from typeChooser import typeChooser
from objDumpParser import parse_objdump
from pygame.locals import *
from pygame import gfxdraw
from tqdm import tqdm
from tabulate import tabulate
import sys
import importlib
import drawPixels as dp

############### Imports render parameters from renderParams/average.py ###############
default_params = "average"
params_arg = sys.argv[1] if len(sys.argv) > 1 else default_params
try:
    # Load the selected theme module dynamically
    global virtPixelSize, screenX, screenY, fillColor, borderColor
    param_module = importlib.import_module(f"renderParams.{params_arg}")
    virtPixelSize = param_module.renderParams["virtPixelSize"]
    screenX = param_module.renderParams["screenX"]
    screenY = param_module.renderParams["screenY"]
    fillColor = param_module.renderParams["fillColor"]
    borderColor = param_module.renderParams["borderColor"]
except ImportError:
    print("Invalid render parameter selection.")
    sys.exit(1)
#######################################################################################

############### Selects between linear render or relative render #####################
default_render = "relative"
render_arg = sys.argv[2] if len(sys.argv) > 2 else default_render
if render_arg == "relative":
    renderStyle = 'memory_index'
elif render_arg == "linear":
    renderStyle = 'index'
#######################################################################################

############### Imports theme information from themes/DebuggersDream.py ###############
default_theme = "DebuggersDream"
theme_arg = sys.argv[3] if len(sys.argv) > 3 else default_theme
try:
    # Load the selected theme module dynamically
    theme_module = importlib.import_module(f"themes.{theme_arg}")
    groupColor = theme_module.theme
    theme_name = theme_module.name
except ImportError:
    print("Invalid theme selection.")
    sys.exit(1)
#######################################################################################

group_types = list(theme_module.theme)
group_types = group_types[:8]
group_types.append("Total")
group_ammounts = [0,0,0,0,0,0,0,0,0]
#print(group_types)
line = '''--------------------------------------------------------------------------------------------------------------'''
app_title = '''
Welcome to your favourite brand new and improved, elf file visualizer:
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
                      "Y8P'                                                                             *<|:^) 
--------------------------------------------------------------------------------------------------------------
'''
print(app_title)
input_file = input("Please enter the name of the file you want to visualize: ")
instructions = parse_objdump(input_file)


##### Initializes PyGame surface and sets up the window #####

icon = pygame.image.load("bruninho.jpg")
pygame.init()
pygame.display.set_caption("ElfoViewer")
pygame.display.set_icon(icon)
DISPLAYSURF = pygame.display.set_mode((screenX, screenY))


#### Draws elf layout
count = 0
for instruction in tqdm(instructions, desc="Rendering and creating table",unit="instructions"):
    count += 1
    color = groupColor[instruction['group']]
    group_ammounts[group_types.index(instruction['group'])] += 1
    dp.drawPixelRelative(DISPLAYSURF, instruction[renderStyle], color, screenX, screenY, virtPixelSize)
print("\n")
group_ammounts[-1] = count
#print("Group ammounts:", group_ammounts)
print(tabulate([group_ammounts], headers=group_types, tablefmt="fancy_grid"))
#### Setups variables to organize dialogue box life
dialogue_box_active = False

#### Main loop

while True: # main game loop
    for event in pygame.event.get():
        ## Quits when esc is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print(line)
                print("\nBye!")
                pygame.quit()
                sys.exit()
        if event.type == QUIT:
            
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()

            #print("Mouse clicked at coordinates:", mouse_pos)
            # prints mouse x and y coords to shell
            x = mouse_pos[0]
            y = mouse_pos[1]
            # finds which pixel was clicked on
            pixelX = (x//(virtPixelSize))
            pixelY = (y//(virtPixelSize)) 
            clickIndex = (screenX//virtPixelSize * (pixelY)) + pixelX
            #print("Pixel clicked at coordinates:", pixelX, pixelY)
            #print("Index:", clickIndex)
            if renderStyle == 'memory_index':
              try:
                clickedInstruction = dp.get_instructio_by_memory_index(instructions, clickIndex)
              except Exception as e:
                #print("No instruction found")
                continue
            elif renderStyle == 'index':
              try:
                clickedInstruction = instructions[clickIndex]    
              except Exception as e:
                #print("No instruction found")
                continue
                
            try:
              print("Instruction:", clickedInstruction)
              if clickedInstruction['group'] == 'BRANCH':
                 target = dp.get_instruction_by_address(instructions, clickedInstruction['content'].split()[0])
                 print("Branch target:", target)
              mnemonic = clickedInstruction['instruction']
              address = clickedInstruction['address']
            except Exception as e:
              #print("No instruction found, address "+ str(clickedInstruction) + " is not an instruction")
              continue
                
            
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
        dp.drawPixelRelative(DISPLAYSURF, instruction[renderStyle], color, screenX, screenY, virtPixelSize)
    if dialogue_box_active:
        
        dp.display_dialogue_box(dialogue_content, dialogue_box_position, DISPLAYSURF)


    pygame.display.update()