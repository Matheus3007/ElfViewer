### TODO:
# - Implement branch direction highlighting for relative mode

import pygame, sys
#from typeChooser import typeChooser
from objDumpParser import parse_objdump
from colorDialogueRenderer import display_color_dialogue
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
print(group_types)
print(len(group_types))
group_types = group_types[:13]
group_types.append("Total")
group_ammounts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#print(group_types)
line = '''--------------------------------------------------------------------------------------------------------------'''
app_title = '''
Welcome to your favourite brand new and improved, interactive elf file visualizer:
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

icon = pygame.image.load("icone.jpg")
pygame.init()
pygame.display.set_caption("ElfoViewer")
pygame.display.set_icon(icon)
DISPLAYSURF = pygame.display.set_mode((screenX, screenY))

#### Draws elf layout
count = 0
DISPLAYSURF.fill(groupColor['background'])
for instruction in tqdm(instructions, desc="Rendering and creating table",unit="instructions"):
    count += 1
    color = groupColor[instruction['group']]
    try:
        group_ammounts[group_types.index(instruction['group'])] += 1
    except Exception as e:
        pass
    dp.drawPixelRelative(DISPLAYSURF, instruction[renderStyle], color, screenX, screenY, virtPixelSize)
AUXSURF = DISPLAYSURF.copy()
print("\n")
group_ammounts[-1] = count
print("Group ammounts:", group_ammounts)
group_percentages = []
for i in group_ammounts[:13]:
    group_percentages.append(str("{:.4f}".format((i/group_ammounts[-1])*100)) + "%")
print(tabulate([group_ammounts, group_percentages], headers=group_types, tablefmt="fancy_grid"))
#### Setups variables to organize dialogue box life
dialogue_box_active = False
highlight_on = False
branch_highlight_on = False
display_color_description = False

#### Main loop
run = True
while run: # main game loop
    for event in pygame.event.get():
        ## Quits when esc is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print(line)
                print("\nBye!")
                pygame.image.save(DISPLAYSURF, "output.png")
                run = False
            if event.key == pygame.K_l:
                display_color_description = not (display_color_description)
        if event.type == QUIT:
            run = False
            print("\nBye!")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            if display_color_description:
                display_color_description = not (display_color_description)
            mouse_pos = pygame.mouse.get_pos()
        
            branch_highlight_on = False
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
              #print("Instruction:", clickedInstruction)
              if not highlight_on:
                if clickedInstruction['group'] == 'Desvios' and clickedInstruction['instruction'][:2] != 'bl':
                    target = dp.get_instruction_by_address(instructions, clickedInstruction['content'].split()[0])
                    if not branch_highlight_on:
                        branch_highlight_on = True
                    elif branch_highlight_on:
                        branch_highlight_on = False

                    #print("Branch target:", target)
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

            if not highlight_on:
                highlight_on = True
            elif highlight_on:
                highlight_on = False
           
                
    ## Fill the screen with background color
    
    DISPLAYSURF.blit(AUXSURF, (0,0))    
    if highlight_on:
        try:
            originTopX, originTopY, originBottomX, originBottomY = dp.highlight_virtpixel_border(DISPLAYSURF, virtPixelSize, (0,0,0),clickedInstruction[renderStyle],screenX)
        except Exception as e:
            #print("No instruction found, address "+ str(clickedInstruction) + " is not an instruction")
            continue
    if branch_highlight_on:
        try:
            destinyTopX, destinyTopY, destinyBottomX, destinyBottomY = dp.highlight_virtpixel_border(DISPLAYSURF, virtPixelSize, (0,0,0),target[renderStyle],screenX)
            pygame.draw.line(DISPLAYSURF, (0,0,0), (originBottomX, originBottomY), (destinyTopX, destinyTopY), 2)
        except Exception as e:
            continue
    if dialogue_box_active:       
        dp.display_dialogue_box(dialogue_content, dialogue_box_position, DISPLAYSURF)
    if display_color_description:
        display_color_dialogue(groupColor, DISPLAYSURF)
    pygame.display.update()

pygame.quit()