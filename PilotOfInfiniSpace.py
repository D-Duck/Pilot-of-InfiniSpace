import EGraphics as eg
import random
import time
import math
from keyboard import is_pressed

# world settings                                                                                                        World settings
blockSize = 50
planetRarity = 0.05
worldSeed = random.random()

# window settings                                                                                                       Window settings
width, height = 750, 500
window = eg.create_window((width, height), "Space")

# window data                                                                                                           window data
drawScene = 0

# mouse data                                                                                                            mouse data
leftClick = False
leftClickPoz = [0, 0]
leftClickBackup = [0, 0]
mouseLast = [False, False, False]

# camera data                                                                                                           Camera data
globalX, globalY = 0, 0

#player data                                                                                                            player data
rot = 0
poz = [0, 0]
drawSolarSystem = False
location_data = [0, 0]

# local seeder                                                                                                          f()   =   local seeder
def local_seed(x, y):
    global blockSize, worldSeed

    x = int(round(x / blockSize, 0))
    y = int(round(y / blockSize, 0))

    random.seed(complex(complex(x, y), worldSeed))
    return random.random()
# float to rgb                                                                                                          f()   =   float to rgb
def float_to_rgb(local_value, star = True):
    if star:
        random.seed(local_value)
        r = random.randint(150, 255)

        random.seed(local_value + 1)
        g = random.randint(0, 255)

        random.seed(local_value - 1)
        b = random.randint(0, 50)

        if g > r:
            g = int(g / 2)

        if r + g + b / 3 < 150:
            r += r
            g += g
            b += b

        if str(local_value)[5] == "4" or str(local_value)[5] == "5":
            color = random.randint(150, 255)
            r, g, b = color, color, color
    else:
        random.seed(local_value)
        r = random.randint(25, 230)

        random.seed(local_value + 1)
        g = random.randint(25, 230)

        random.seed(local_value - 1)
        b = random.randint(25, 230)

    return (r, g, b)

# drawing scene                                                                                                         f()   =   drawing scene
drawBlocks = False
quickSettingsD = [drawBlocks, planetRarity]
background = []
def draw_background(win):
    eg.fill(win, eg.color.black)
    if background == []:
        for n in range(250):
            background.append((random.randint(0, width), random.randint(0, height)))
    for star in background:
        eg.draw_pixel(win, eg.color.white, star[0], star[1])
def draw_frame(win):
    global quickSettingsD, poz, target, rot, cicle, drawScene

    if drawScene == 0: # draw space
        draw_background(win)
        for localY in range(-blockSize - int(round(globalY, 0)) % blockSize, height + blockSize - int(round(globalY, 0)) % blockSize, blockSize):
            for localX in range(-blockSize - int(round(globalX, 0)) % blockSize, width + blockSize - int(round(globalX, 0)) % blockSize, blockSize):
                local_value = local_seed(globalX + localX, globalY + localY)
                if local_value > 1 - quickSettingsD[1]:
                    eg.draw_circle(win, float_to_rgb(local_value), localX, localY, int(round(local_value ** 25 * 25, 0)))
                    if poz == [None, None]:
                        poz = [globalX + localX, globalY + localY]
                if quickSettingsD[0]:
                    eg.draw_rectangle(win, eg.color.white, int(round(localX, 0)) - int(round(blockSize / 2, 0)), int(round(localY, 0)) - int(round(blockSize / 2, 0)), blockSize, blockSize, draw_offset=(0, 0), border_width=1)
        # draw player
        rot += 0.005
        if rot >= math.pi * 2:
            rot -= math.pi * 2
        if rot <= 0:
            rot += math.pi * 2
        length = int(round(local_seed(poz[0], poz[1]) ** 25 * 25, 0)) + 10
        eg.draw_circle(win, eg.color.sky_blue, int(round(math.cos(rot) * length + poz[0] - globalX, 0)), int(round(math.sin(rot) * length + poz[1] - globalY, 0)), 5)
    elif drawScene == 1:
        draw_background(win)
        eg.draw_rectangle(win, eg.color.black, 50, 50, width - 100, height - 100, draw_offset=(0, 0))
        eg.draw_rectangle(win, eg.color.blue, 50, 50, width - 100, height - 100, 4, draw_offset=(0, 0))
        x, y = 230, int(round(height /2, 0))
        local_value = local_seed(globalX + location_data[0], globalY + location_data[1])
        eg.draw_circle(win, float_to_rgb(local_value), 130, y, int(round(local_value ** 25 * 75, 0)))
        for n in range(int(str(local_value)[4])):
            eg.draw_circle(win, float_to_rgb(int(str(local_value)[n + 4]), False), x, y, int(str(local_value)[n + 4]) * 2, 0)
            x += 55
    else:
        print(f"Scene number {drawScene} does not exist. Changing it to 0")
        drawScene = 50
        
    # draw left click menu
    if leftClick: # adding menu buttons
        x, y = leftClickPoz
        if int(round(poz[0] / blockSize, 0)) != int(round((globalX + leftClickPoz[0]) / blockSize, 0)) or int(round(poz[1] / blockSize, 0)) != int(round((globalY + leftClickPoz[1]) / blockSize, 0)):
            if local_seed(globalX + x, globalY + y) > 1 - quickSettingsD[1]:
                mx, my = eg.get_mouse_poz()
                if x < mx < x + 75 and y < my < y + 25 :
                    eg.draw_rectangle(win, eg.color.white, x, y, 75, 25, draw_offset=(0, 0))
                    eg.draw_text(win, eg.color.black, x + 3, y + 5, "LAUNCH", 20, font="consolas")
                else:
                    eg.draw_rectangle(win, eg.color.black, x, y, 75, 25, draw_offset=(0, 0))
                    eg.draw_text(win, eg.color.white, x + 3, y + 5, "LAUNCH", 20, font="consolas")
                eg.draw_rectangle(win, eg.color.blue, x, y, 75, 25, draw_offset=(0, 0), border_width=1)
                y += 25
        if int(round(poz[0] / blockSize, 0)) == int(round((globalX + leftClickPoz[0]) / blockSize, 0)) and int(round(poz[1] / blockSize, 0)) == int(round((globalY + leftClickPoz[1]) / blockSize, 0)):
            mx, my = eg.get_mouse_poz()
            if x < mx < x + 75 and y < my < y + 25 :
                eg.draw_rectangle(win, eg.color.white, x, y, 75, 25, draw_offset=(0, 0))
                eg.draw_text(win, eg.color.black, x + 3, y + 5, "SOLAR", 20, font="consolas")
            else:
                eg.draw_rectangle(win, eg.color.black, x, y, 75, 25, draw_offset=(0, 0))
                eg.draw_text(win, eg.color.white, x + 3, y + 5, "SOLAR", 20, font="consolas")
            eg.draw_rectangle(win, eg.color.blue, x, y, 75, 25, draw_offset=(0, 0), border_width=1)

    # draw text
    eg.draw_text(win, (255, 255, 255), 0, 0, f"{globalX} X {globalY}", 15)
    eg.draw_text(win, (255, 255, 255), width - 30, height - 15, f"{cicle[2]}", 15)

    eg.update()

# key press event handler                                                                                               f()   =   Key press handler
speed = 10
multiplayer = 4
quickSettingsK = [speed, multiplayer]
def key_press_handler():
    global quickSettingsK

    if is_pressed("esc"):
        print("game was closed with esc")
        quit()

    x, y = 0, 0
    if is_pressed("w"):
        if is_pressed("shift"):
            y -= quickSettingsK[0] * quickSettingsK[1]
        else:
            y -= quickSettingsK[0]
    elif is_pressed("s"):
        if is_pressed("shift"):
            y += quickSettingsK[0] * quickSettingsK[1]
        else:
            y += quickSettingsK[0]

    if is_pressed("a"):
        if is_pressed("shift"):
            x -= quickSettingsK[0] * quickSettingsK[1]
        else:
            x -= quickSettingsK[0]
    elif is_pressed("d"):
        if is_pressed("shift"):
            x += quickSettingsK[0] * quickSettingsK[1]
        else:
            x += quickSettingsK[0]

    return x, y

# MAIN LOOP                                                                                                             > Main loop
fpsTarget =  1 / (60 + 10)
fpsTiming = time.time()
cicle = [0, time.time(), 0]
while True:
    if time.time() - fpsTiming > fpsTarget:
        fpsTiming = time.time()

        # KEY PRESS HANDLER                                                                                            > Key press handler
        if drawScene == 0:
            metaX, metaY = key_press_handler()
            globalX += metaX
            globalY += metaY

        if drawScene == 0: # MOUSE PRESS HANDLER scene 0
            if leftClickBackup != [globalX, globalY]:
                leftClick = False

            if eg.get_mouse_click()[0]: # adding menu buttons
                if leftClick:
                    x, y = leftClickPoz
                    if int(round(poz[0] / blockSize, 0)) != int(round((globalX + leftClickPoz[0]) / blockSize, 0)) or int(round(poz[1] / blockSize, 0)) != int(round((globalY + leftClickPoz[1]) / blockSize, 0)):
                        if local_seed(globalX + x, globalY + y) > 1 - quickSettingsD[1]:
                            mx, my = eg.get_mouse_poz()
                            if x < mx < x + 75 and y < my < y + 25:
                                poz = [int(round((globalX + leftClickPoz[0]) / blockSize, 0)) * blockSize, int(round((globalY + leftClickPoz[1]) / blockSize, 0)) * blockSize]
                                leftClick = False
                            y += 25
                    if int(round(poz[0] / blockSize, 0)) == int(round((globalX + leftClickPoz[0]) / blockSize, 0)) and int(round(poz[1] / blockSize, 0)) == int(round((globalY + leftClickPoz[1]) / blockSize, 0)):
                        mx, my = eg.get_mouse_poz()
                        if x < mx < x + 75 and y < my < y + 25:
                            drawScene = 1
                            leftClick = False
                    if not leftClick:
                        location_data = leftClickPoz
                        leftClickPoz = [0, 0]

            if eg.get_mouse_click()[2]:
                mx, my = eg.get_mouse_poz()
                if local_seed(globalX + mx, globalY + my) > 1 - quickSettingsD[1]:
                    if int(round(globalX + mx / blockSize, 0)) != int(round(globalX + leftClickPoz[0] / blockSize, 0)) or int(round(globalY + my / blockSize, 0)) != int(round(globalY + leftClickPoz[1] / blockSize, 0)):
                        leftClick = True
                        leftClickPoz = [mx, my]
                        leftClickBackup = [globalX, globalY]
        if drawScene == 1:
            if eg.get_mouse_click()[0]:
                mx, my = eg.get_mouse_poz()
                if 50 < mx < width - 50 and 50 < my < height - 50:
                    pass
                else:
                    if not mouseLast[0]:
                        drawScene = 0
            mouseLast = eg.get_mouse_click()

    cicle[0] += 1
    if time.time() - cicle[1] >= 1:
        cicle[2] = cicle[0]
        cicle[0] = 0
        cicle[1] = time.time()

    # DRAWING                                                                                                           > Drawing
    draw_frame(window)