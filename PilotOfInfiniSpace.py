import EGraphics as eg
import random
import time
from keyboard import is_pressed

# world settings                                                                                                        World settings
blockSize = 50
planetRarity = 0.05

# window settings                                                                                                       Window settings
width, height = 750, 500
window = eg.create_window((width, height), "Space")

# camera data                                                                                                           Camera data
globalX, globalY = 0, 0

# local seeder                                                                                                          f()   =   local seeder
def local_seed(x, y):
    global blockSize

    x = int(round(x / blockSize, 0))
    y = int(round(y / blockSize, 0))

    random.seed(complex(x, y))
    return random.random()
# float to rgb                                                                                                          f()   =   float to rgb
def float_to_rgb(local_value):
    random.seed(local_value)
    r = random.randint(150, 255)

    random.seed(local_value + 1)
    g = random.randint(0, 255)

    random.seed(local_value + 1)
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

    return (r, g, b)

# drawing scene                                                                                                         f()   =   drawing scene
drawBlocks = False
quickSettingsD = [drawBlocks, planetRarity]
def draw_frame(win):
    global quickSettingsD

    eg.fill(win, eg.color.black)
    for localY in range(-blockSize - int(round(globalY, 0)) % blockSize, height + blockSize - int(round(globalY, 0)) % blockSize, blockSize):
        for localX in range(-blockSize - int(round(globalX, 0)) % blockSize, width + blockSize - int(round(globalX, 0)) % blockSize, blockSize):
            local_value = local_seed(globalX + localX, globalY + localY)
            if local_value > 1 - quickSettingsD[1]:
                eg.draw_circle(win, float_to_rgb(local_value), int(round(localX + blockSize / 2, 0)), int(round(localY + blockSize / 2, 0)), int(round(local_value ** 25 * 25, 0)))
            if quickSettingsD[0]:
                eg.draw_rectangle(win, eg.color.white, int(round(localX, 0)), int(round(localY, 0)), blockSize, blockSize, draw_offset=(0, 0), border_width=1)

    eg.update()

# key press event handler                                                                                               f()   =   Key press handler
speed = 10
multiplayer = 4
quickSettingsK = [speed, multiplayer]
def key_press_handler():
    global quickSettingsK

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
while True:
    if time.time() - fpsTiming > fpsTarget:
        fpsTiming = time.time()

        # KEY PRESS HANDLER                                                                                             > Key press handler
        metaX, metaY = key_press_handler()
        globalX += metaX
        globalY += metaY

    # DRAWING                                                                                                           > Drawing
    draw_frame(window)