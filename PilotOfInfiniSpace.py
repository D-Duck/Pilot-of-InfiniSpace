import EGraphics as eg
import random
import time
import math
from keyboard import is_pressed, get_hotkey_name

# global data                                                                                                           Global data
command = None
commandTimeout = 0
commandBlock = False
rockLoot = ["ironore", "copperore"]
rockWeight = [3, 1]

# world settings                                                                                                        World settings
spaceStationRot = 0
blockSize = 50
planetRarity = 0.05
worldSeed = random.random()

# window settings                                                                                                       Window settings
width, height = 750, 500
window = eg.create_window((width, height), "Space")

# window data                                                                                                           window data
drawScene = 0

# mouse data                                                                                                            mouse data
leftHold = False
leftClick = False
leftClickPoz0 = [0, 0]
leftClickPoz1 = [0, 0]
leftClickPoz2 = [0, 0]
leftClickBackup = [0, 0]
mouseLast = [False, False, False]
lastPoz = [0, 0]
nowPoz = [0, 0]

# camera data                                                                                                           Camera data
globalX, globalY = random.randint(0, 2_000_000) - 1_000_000, random.randint(0, 2_000_000) - 1_000_000

#player data                                                                                                            player data
rot = 0
poz = [globalX, globalY]
fuel = 10
showRange = False
showRangeTiming = time.time()
hyperCharge = True
hyperRange = 10000
hyperChargeTiming = 0
drawSolarSystem = False
inventoryPressed = 0
inventoryOpen = False
inventory = []
laungAnim = False
target = [0, 0]
step = 0

inventorySpace = 15
hyperRecovery = 300
launchRange = 300

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
    global quickSettingsD, poz, target, rot, cicle, drawScene, hyperChargeTiming, hyperCharge, hyperRecovery, launchRange, showRange, laungAnim, step, target, spaceStationRot

    if drawScene == 0: # draw space
        draw_background(win)
        for localY in range(-blockSize - int(round(globalY, 0)) % blockSize, height + blockSize - int(round(globalY, 0)) % blockSize, blockSize):
            for localX in range(-blockSize - int(round(globalX, 0)) % blockSize, width + blockSize - int(round(globalX, 0)) % blockSize, blockSize):
                local_value = local_seed(globalX + localX, globalY + localY)
                if local_value > 1 - quickSettingsD[1]:
                    eg.draw_circle(win, float_to_rgb(local_value), localX, localY, int(round(local_value ** 25 * 25, 0)))
                    if str(local_value)[10] == "0":
                        length, rot_ = int(round(local_seed(localX + globalX, localY + globalY) ** 25 * 25, 0)) + 20, spaceStationRot + eg.rad_to_deg(local_value)
                        eg.draw_image(win, "graphics\\sprites\\spaceStation.png", int(round(math.cos(rot_) * length + localX, 0)), int(round(math.sin(rot_) * length + localY, 0)), scale_to=10, rotate_deg=eg.rad_to_deg(-rot_))
                    if poz == [None, None]:
                        poz = [globalX + localX, globalY + localY]
                if quickSettingsD[0]:
                    eg.draw_rectangle(win, eg.color.white, int(round(localX, 0)) - int(round(blockSize / 2, 0)), int(round(localY, 0)) - int(round(blockSize / 2, 0)), blockSize, blockSize, draw_offset=(0, 0), border_width=1)
        # draw player
        spaceStationRot += 0.005
        if not laungAnim:
            rot += 0.005
        else:
            rot = math.atan2(target[1] - poz[1], target[0] - poz[0])
        if rot >= math.pi * 2:
            rot -= math.pi * 2
        if rot <= 0:
            rot += math.pi * 2

            if is_pressed("f"):
                laungAnim = False
        if laungAnim:
            length = int(round(local_seed(poz[0], poz[1]) ** 25 * 25, 0)) + 10 + math.sqrt((((poz[0] - target[0]) / 250) * step) ** 2 +  (((poz[1] - target[1]) / 250) * step) ** 2)
            eg.draw_image(win, "graphics\\sprites\\player.png",int(round(math.cos(rot) * length + poz[0] - globalX, 0)),int(round(math.sin(rot) * length + poz[1] - globalY, 0)), rotate_deg=eg.rad_to_deg(-rot) + 90)
            step += 1
            if step == 250:
                laungAnim = False
                poz = target
        else:
            length = int(round(local_seed(poz[0], poz[1]) ** 25 * 25, 0)) + 10
            eg.draw_image(win, "graphics\\sprites\\player.png", int(round(math.cos(rot) * length + poz[0] - globalX, 0)), int(round(math.sin(rot) * length + poz[1] - globalY, 0)), rotate_deg=eg.rad_to_deg(-rot))
        x, y, color = width - 25, height - 60, [255, 0, 0]
        if showRange:
            eg.draw_circle(window, eg.color.green, poz[0] - globalX, poz[1] - globalY, launchRange, 2)
        for n in range(fuel + 1):
            if n < fuel:
                eg.draw_rectangle(win, color, x, y, 10, 20, draw_offset=(0, 0))
                x -= 12
                color[0] -= 25.5
                color[1] += 25.55
            else:
                if hyperCharge:
                    eg.draw_rectangle(win, eg.color.light_blue, width - 133, height - 35, 118, 20,draw_offset=(0, 0))
                    eg.draw_rectangle(win, eg.color.white, width - 133, height - 35, 118, 20, 2,draw_offset=(0, 0))
                else:
                    eg.draw_rectangle(win, eg.color.light_blue, width - 132, height - 35,int(round((time.time() - hyperChargeTiming) * 118 / hyperRecovery, 0)), 20,draw_offset=(0, 0))
                    eg.draw_rectangle(win, eg.color.gray, width - 133, height - 35, 118, 20, 2, draw_offset=(0, 0))
        if inventoryOpen:
            x, y = 10, height - 10
            for n in range(1, inventorySpace + 1):
                eg.draw_rectangle(win, eg.color.black, x, y, 50, 50, draw_offset=(0, 50))
                try:
                    path = "graphics\\inventory\\" + inventory[n - 1] + ".png"
                    eg.draw_image(win, path, x, y, draw_offset=(0, 50))
                except:
                    pass
                eg.draw_rectangle(win, eg.color.blue, x, y, 50, 50, 2, draw_offset=(0, 50))
                y -= 60
                if n % 5 == 0 and n != 0:
                    x += 60
                    y = height - 10
            x, y = 10, height - 60
            mx, my = eg.get_mouse_poz()
            for n in range(1, inventorySpace + 1):
                if x + 50 > mx > x and y + 50 > my > y:
                    eg.draw_rectangle(win, eg.color.black, mx + 10, my, 100, 25, draw_offset=(0, 0))
                    try:
                        eg.draw_text(win, eg.color.white, mx + 12, my, inventory[n - 1], 20)
                    except:
                        eg.draw_text(win, eg.color.white, mx + 12, my, "EMPTY", 20)
                    eg.draw_rectangle(win, eg.color.blue, mx + 10, my, 100, 25, draw_offset=(0, 0), border_width=1)
                y -= 60
                if n % 5 == 0 and n != 0:
                    x += 60
                    y = height - 60
    elif drawScene == 1:
        draw_background(win)
        eg.draw_rectangle(win, eg.color.black, 50, 50, width - 100, height - 100, draw_offset=(0, 0))
        eg.draw_rectangle(win, eg.color.blue, 50, 50, width - 100, height - 100, 4, draw_offset=(0, 0))
        x, y = 230, int(round(height /2, 0))
        local_value = local_seed(poz[0], poz[1])
        eg.draw_circle(win, float_to_rgb(local_value), 130, y, 50)
        eg.draw_circle(win, float_to_rgb(local_value), 130, y, int(round(local_value ** 25 * 75, 0)))
        if str(local_value)[10] == "0":
            for n in range(int(str(local_value)[4]) - 1):
                eg.draw_circle(win, float_to_rgb(int(str(local_value)[n + 5]) + int(str(local_value)[n + 6]) + int(str(local_value)[n + 7]), False), x, y,int(str(local_value)[n + 4]) * 2, 0)
                path = "graphics\\mask\\planets\\mask" + str(local_value)[n + 4] + ".png"
                eg.draw_image(win, path, x, y)
                x += 55
            eg.draw_image(win, "graphics\\sprites\\spaceStation.png", x, y)
        else:
            for n in range(int(str(local_value)[4])):
                eg.draw_circle(win, float_to_rgb(int(str(local_value)[n + 5]) + int(str(local_value)[n + 6]) + int(str(local_value)[n + 7]), False), x, y,int(str(local_value)[n + 4]) * 2, 0)
                path = "graphics\\mask\\planets\\mask" + str(local_value)[n + 4] + ".png"
                eg.draw_image(win, path, x, y, scale_to=30)
                x += 55
        x, y, color = width - 25, height - 30, [255, 0, 0]
        for n in range(fuel):
            if n < fuel:
                eg.draw_rectangle(win, color, x, y, 10, 20, draw_offset=(0, 0))
                x -= 12
                color[0] -= 25.5
                color[1] += 25.55
    elif drawScene == 2:
        local_value = local_seed(poz[0], poz[1])
        n = int(round((leftClickPoz1[0] - 230) / 55, 0))
        eg.fill(win, float_to_rgb(int(str(local_value)[n + 5]) + int(str(local_value)[n + 6]) + int(str(local_value)[n + 7]), False))
        path = "graphics\\mask\\planetary\\mask" + str(local_value)[n + 4] + ".png"
        eg.draw_image(win, path, 0, 0, draw_offset=(0, 0))
        if str(local_value)[n + 6] == "5" or str(local_value)[n + 6] == "6" or str(local_value)[n + 6] == "7":
            eg.draw_image(win, "graphics\\sprites\\rock.png", int(str(local_value)[n + 6]) * 83, int(str(local_value)[n + 5]) * 83, draw_offset=(0, 0))
        mx, my = eg.get_mouse_poz()
        if width - 10 > mx > width - 60 and height - 10 > my > height - 60:
            eg.draw_rectangle(win, eg.color.white, width - 60, height - 60, 50, 50, draw_offset=(0, 0))
            eg.draw_line(win, eg.color.black, width - 35, height - 15, width - 35, height - 55, 2)
            eg.draw_line(win, eg.color.black, width - 25, height - 40, width - 35, height - 55, 2)
            eg.draw_line(win, eg.color.black, width - 45, height - 40, width - 35, height - 55, 2)
        else:
            eg.draw_rectangle(win, eg.color.black, width - 60, height - 60, 50, 50, draw_offset=(0, 0))
            eg.draw_line(win, eg.color.white, width - 35, height - 15, width - 35, height - 55, 2)
            eg.draw_line(win, eg.color.white, width - 25, height - 40, width - 35, height - 55, 2)
            eg.draw_line(win, eg.color.white, width - 45, height - 40, width - 35, height - 55, 2)
        eg.draw_rectangle(win, eg.color.blue, width - 60, height - 60, 50, 50, 2, draw_offset=(0, 0))

    else:
        print(f">>> Scene number {drawScene} does not exist. Changing it to 0\n")
        drawScene = 50
        
    # draw left click menu
    if leftClick: # adding menu buttons
        if drawScene == 0:
            x, y = leftClickPoz0
            if int(round(poz[0] / blockSize, 0)) != int(round((globalX + leftClickPoz0[0]) / blockSize, 0)) or int(round(poz[1] / blockSize, 0)) != int(round((globalY + leftClickPoz0[1]) / blockSize, 0)):
                if launchRange > math.sqrt((abs(globalX + leftClickPoz0[0] - poz[0]) ** 2) + (abs(globalY + leftClickPoz0[1] - poz[1]) ** 2)):
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
            if int(round(poz[0] / blockSize, 0)) == int(round((globalX + leftClickPoz0[0]) / blockSize, 0)) and int(round(poz[1] / blockSize, 0)) == int(round((globalY + leftClickPoz0[1]) / blockSize, 0)):
                mx, my = eg.get_mouse_poz()
                if x < mx < x + 75 and y < my < y + 25 :
                    eg.draw_rectangle(win, eg.color.white, x, y, 75, 25, draw_offset=(0, 0))
                    eg.draw_text(win, eg.color.black, x + 3, y + 5, "SOLAR", 20, font="consolas")
                else:
                    eg.draw_rectangle(win, eg.color.black, x, y, 75, 25, draw_offset=(0, 0))
                    eg.draw_text(win, eg.color.white, x + 3, y + 5, "SOLAR", 20, font="consolas")
                eg.draw_rectangle(win, eg.color.blue, x, y, 75, 25, draw_offset=(0, 0), border_width=1)
                y += 25
            if hyperRange > math.sqrt((abs(globalX + leftClickPoz0[0] - poz[0]) ** 2) + (abs(globalY + leftClickPoz0[1] - poz[1]) ** 2)) > launchRange + 1:
                mx, my = eg.get_mouse_poz()
                if x < mx < x + 75 and y < my < y + 25 :
                    eg.draw_rectangle(win, eg.color.white, x, y, 75, 25, draw_offset=(0, 0))
                    eg.draw_text(win, eg.color.black, x + 3, y + 5, "HYPER", 20, font="consolas")
                else:
                    eg.draw_rectangle(win, eg.color.black, x, y, 75, 25, draw_offset=(0, 0))
                    eg.draw_text(win, eg.color.white, x + 3, y + 5, "HYPER", 20, font="consolas")
                eg.draw_rectangle(win, eg.color.blue, x, y, 75, 25, draw_offset=(0, 0), border_width=1)
                y += 25
            if int(round(poz[0] / blockSize, 0)) == int(round((globalX + leftClickPoz0[0]) / blockSize, 0)) and int(round(poz[1] / blockSize, 0)) == int(round((globalY + leftClickPoz0[1]) / blockSize, 0)):
                mx, my = eg.get_mouse_poz()
                if x < mx < x + 75 and y < my < y + 25 :
                    eg.draw_rectangle(win, eg.color.white, x, y, 75, 25, draw_offset=(0, 0))
                    eg.draw_text(win, eg.color.black, x + 3, y + 5, "RANGE", 20, font="consolas")
                else:
                    eg.draw_rectangle(win, eg.color.black, x, y, 75, 25, draw_offset=(0, 0))
                    eg.draw_text(win, eg.color.white, x + 3, y + 5, "RANGE", 20, font="consolas")
                eg.draw_rectangle(win, eg.color.blue, x, y, 75, 25, draw_offset=(0, 0), border_width=1)
                y += 25
        elif drawScene == 1:
            x, y = leftClickPoz1
            mx, my = eg.get_mouse_poz()
            if (int(str(local_value)[4])) * 55 + 205 > leftClickPoz1[0] > 205 and int(round(height / 2, 0)) + 25 > leftClickPoz1[1] > int(round(height / 2, 0)) - 25:
                if (int(str(local_value)[4]) - 1) * 55 + 205 > leftClickPoz1[0] > 205 and int(round(height / 2, 0)) + 25 > leftClickPoz1[1] > int(round(height / 2, 0)) - 25:
                    if x < mx < x + 75 and y < my < y + 25:
                        eg.draw_rectangle(win, eg.color.white, x, y, 75, 25, draw_offset=(0, 0))
                        eg.draw_text(win, eg.color.black, x + 3, y + 5, "LAND", 20, font="consolas")
                    else:
                        eg.draw_rectangle(win, eg.color.black, x, y, 75, 25, draw_offset=(0, 0))
                        eg.draw_text(win, eg.color.white, x + 3, y + 5, "LAND", 20, font="consolas")
                    eg.draw_rectangle(win, eg.color.blue, x, y, 75, 25, draw_offset=(0, 0), border_width=1)
                else:
                    if str(local_value)[10] == "0":
                        if x < mx < x + 75 and y < my < y + 25:
                            eg.draw_rectangle(win, eg.color.white, x, y, 75, 25, draw_offset=(0, 0))
                            eg.draw_text(win, eg.color.black, x + 3, y + 5, "DOCK", 20, font="consolas")
                        else:
                            eg.draw_rectangle(win, eg.color.black, x, y, 75, 25, draw_offset=(0, 0))
                            eg.draw_text(win, eg.color.white, x + 3, y + 5, "DOCK", 20, font="consolas")
                        eg.draw_rectangle(win, eg.color.blue, x, y, 75, 25, draw_offset=(0, 0), border_width=1)
                    else:
                        if x < mx < x + 75 and y < my < y + 25:
                            eg.draw_rectangle(win, eg.color.white, x, y, 75, 25, draw_offset=(0, 0))
                            eg.draw_text(win, eg.color.black, x + 3, y + 5, "LAND", 20, font="consolas")
                        else:
                            eg.draw_rectangle(win, eg.color.black, x, y, 75, 25, draw_offset=(0, 0))
                            eg.draw_text(win, eg.color.white, x + 3, y + 5, "LAND", 20, font="consolas")
                        eg.draw_rectangle(win, eg.color.blue, x, y, 75, 25, draw_offset=(0, 0), border_width=1)
                y += 25
        elif drawScene == 2:
            x, y = leftClickPoz2
            mx, my = eg.get_mouse_poz()
            if str(local_value)[n + 6] == "5" or str(local_value)[n + 6] == "6" or str(local_value)[n + 6] == "7":
                rx, ry = int(str(local_value)[n + 6]) * 83, int(str(local_value)[n + 5]) * 83
                if rx + 50 > mx > rx and ry + 50 > my > ry:
                    if x < mx < x + 75 and y < my < y + 25:
                        eg.draw_rectangle(win, eg.color.white, x, y, 75, 25, draw_offset=(0, 0))
                        eg.draw_text(win, eg.color.black, x + 3, y + 5, "MINE", 20, font="consolas")
                    else:
                        eg.draw_rectangle(win, eg.color.black, x, y, 75, 25, draw_offset=(0, 0))
                        eg.draw_text(win, eg.color.white, x + 3, y + 5, "MINE", 20, font="consolas")
                    eg.draw_rectangle(win, eg.color.blue, x, y, 75, 25, draw_offset=(0, 0), border_width=1)



    # draw text
    eg.draw_text(win, (255, 255, 255), 0, 0, f"{globalX} X {globalY}", 15)
    eg.draw_text(win, (255, 255, 255), width - 30, 0, f"{cicle[2]}", 15)
    if command != None:
        eg.draw_text(win, (255, 255, 255), 0, height - 40, f"<<< {command}")

    eg.update()

# key press event handler                                                                                               f()   =   Key press handler
speed = 10
multiplayer = 4
quickSettingsK = [speed, multiplayer]
def command_comparing(str1, str2):
    same = True
    try:
        for n in range(len(str2)):
            if str1[n].lower() != str2[n].lower():
                same = False
                break
    except:
        same = False
    return same
def command_parsing(str):
    meta = []
    meta_ = ""
    if str[-1] != " ":
        str = str + " "
    for char in str:
        if char == " ":
            meta.append(meta_)
            meta_ = ""
        else:
            meta_ += char
    return meta
def key_press_handler():
    global quickSettingsK, command, commandTimeout, commandBlock, globalY, globalX, fuel, hyperCharge, inventoryOpen, inventoryPressed

    if is_pressed("`"):
        if time.time() - commandTimeout > 0.5:
            if command == None:
                command = ""
                commandTimeout = time.time()
            else:
                command = None
                commandTimeout = time.time()
            commandBlock = True
    if command != None:
        try:
            key = get_hotkey_name()[0]
            if not commandBlock:
                if get_hotkey_name() == "backspace":
                    command_ = ""
                    for n in range(len(command) - 1):
                        command_ += command[n]
                    command = command_
                elif get_hotkey_name() == "space":
                    command += " "
                    commandBlock = True
                elif get_hotkey_name() == "enter": # commands here
                    if command_comparing(command, "tp to"):
                        backup = [globalX, globalY]
                        try:
                            globalX = int(command_parsing(command)[2])
                            globalY = int(command_parsing(command)[3])
                        except:
                            globalX = backup[0]
                            globalY = backup[1]
                            print(f'Wierd coordinates for "tp to" ({command_parsing(command)[2]} X {command_parsing(command)[3]})')
                    elif command_comparing(command, "tp player"):
                        globalX = poz[0] - int(width / 2)
                        globalY = poz[1] - int(height / 2)
                    elif command_comparing(command, "set fuel"):
                        ammount = int(command_parsing(command)[2])
                        if ammount > 10:
                            ammount = 10
                        if ammount < 0:
                            ammount = 0
                        fuel = ammount
                    elif command_comparing(command, "help"):
                        print(">>> hyper full = fully recharge hyper jump")
                        print(">>> set fuel N = set fuel to max N(0 - 10)")
                        print(">>> tp to X Y = tp to exact coordinates given by player (X, Y)")
                        print(">>> tp player = tp to player coordinates")
                        print(">>> help = list all commands\n")
                    elif command_comparing(command, "hyper full"):
                        hyperCharge = True
                    else:
                        print(f'>>> Unknown command "{command}"\n')
                    command = None
                else:
                    command += key
                commandBlock = True
        except:
            commandBlock = False

    if is_pressed("esc"):
        print(">>> game was closed with esc")
        quit()

    if is_pressed("i"):
        if not inventoryPressed:
            if inventoryOpen:
                inventoryOpen = False
            else:
                inventoryOpen = True
            inventoryPressed = True
    else:
        inventoryPressed = False

    x, y = 0, 0
    if command == None:
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

        if not hyperCharge:
            if time.time() - hyperChargeTiming >= hyperRecovery:
                hyperCharge = True
                hyperChargeTiming = 0
        # KEY PRESS HANDLER                                                                                            > Key press handler
        if drawScene == 0:
            metaX, metaY = key_press_handler()
            globalX += metaX
            globalY += metaY
        else:
            key_press_handler()

        lock1 = False
        if drawScene == 2:
            if eg.get_mouse_click()[0]:
                if not leftHold:
                    mx, my = eg.get_mouse_poz()
                    if width - 10 > mx > width - 60 and height - 10 > my > height - 60:
                        drawScene = 1
                        leftHold = True
                        lock1 = True
        leftHold = eg.get_mouse_click()[0]

        if leftClickBackup != [globalX, globalY]:
            leftClick = False

        if eg.get_mouse_click()[0]:  # adding menu buttons
            if leftClick:
                if drawScene == 0:
                    leftClick = True
                    x, y = leftClickPoz0
                    if int(round(poz[0] / blockSize, 0)) != int(round((globalX + leftClickPoz0[0]) / blockSize, 0)) or int(round(poz[1] / blockSize, 0)) != int(round((globalY + leftClickPoz0[1]) / blockSize, 0)):
                        if launchRange > math.sqrt((abs(globalX + leftClickPoz0[0] - poz[0]) ** 2) + (abs(globalY + leftClickPoz0[1] - poz[1]) ** 2)):
                            if local_seed(globalX + x, globalY + y) > 1 - quickSettingsD[1]:
                                if fuel > 0:
                                    mx, my = eg.get_mouse_poz()
                                    if x < mx < x + 75 and y < my < y + 25:
                                        target = [int(round((globalX + leftClickPoz0[0]) / blockSize, 0)) * blockSize,int(round((globalY + leftClickPoz0[1]) / blockSize, 0)) * blockSize]
                                        step = 0
                                        laungAnim = True
                                        leftClick = False
                                        fuel -= 1
                                    y += 25
                    if int(round(poz[0] / blockSize, 0)) == int(round((globalX + leftClickPoz0[0]) / blockSize, 0)) and int(
                            round(poz[1] / blockSize, 0)) == int(round((globalY + leftClickPoz0[1]) / blockSize, 0)):
                        mx, my = eg.get_mouse_poz()
                        if x < mx < x + 75 and y < my < y + 25:
                            drawScene = 1
                            leftClick = False
                        y += 25
                    if hyperRange > math.sqrt((abs(globalX + leftClickPoz0[0] - poz[0]) ** 2) + (
                            abs(globalY + leftClickPoz0[1] - poz[1]) ** 2)) > launchRange + 1:
                        mx, my = eg.get_mouse_poz()
                        if x < mx < x + 75 and y < my < y + 25:
                            if int(round(poz[0] / blockSize, 0)) != int(
                                    round((globalX + leftClickPoz0[0]) / blockSize, 0)) or int(
                                    round(poz[1] / blockSize, 0)) != int(round((globalY + leftClickPoz0[1]) / blockSize, 0)):
                                if local_seed(globalX + leftClickPoz0[0], globalY + leftClickPoz0[1]) > 1 - quickSettingsD[1]:
                                    if hyperCharge:
                                        if x < mx < x + 75 and y < my < y + 25:
                                            poz = [int(round((globalX + leftClickPoz0[0]) / blockSize, 0)) * blockSize,
                                                   int(round((globalY + leftClickPoz0[1]) / blockSize, 0)) * blockSize]
                                            leftClick = False
                                            hyperCharge = False
                                            hyperChargeTiming = time.time()
                            leftClick = False
                        y += 25
                    if int(round(poz[0] / blockSize, 0)) == int(round((globalX + leftClickPoz0[0]) / blockSize, 0)) and int(
                            round(poz[1] / blockSize, 0)) == int(round((globalY + leftClickPoz0[1]) / blockSize, 0)):
                        mx, my = eg.get_mouse_poz()
                        if x < mx < x + 75 and y < my < y + 25:
                            if showRange:
                                showRange = False
                            else:
                                showRange = True
                            showRangeTiming = time.time()
                            leftClick = False
                        y += 25
                elif drawScene == 1:
                    x, y = leftClickPoz1
                    mx, my = eg.get_mouse_poz()
                    local_value = local_seed(poz[0], poz[1])
                    if (int(str(local_value)[4])) * 55 + 205 > leftClickPoz1[0] > 205 and int(round(height / 2, 0)) + 25 > leftClickPoz1[1] > int(round(height / 2, 0)) - 25:
                        if (int(str(local_value)[4]) - 1) * 55 + 205 > leftClickPoz1[0] > 205 and int(round(height / 2, 0)) + 25 > leftClickPoz1[1] > int(round(height / 2, 0)) - 25:
                            if x < mx < x + 75 and y < my < y + 25:
                                if fuel > 0:
                                    drawScene = 2
                                    fuel -= 1
                                    leftClick = False
                        else:
                            if str(local_value)[10] == "0":
                                if x < mx < x + 75 and y < my < y + 25:
                                    print("DOCKING")
                                    leftClick = False
                            else:
                                if x < mx < x + 75 and y < my < y + 25:
                                    if fuel > 0:
                                        drawScene = 2
                                        fuel -= 1
                                        leftClick = False
                        y += 25
                elif drawScene == 2:
                    n = int(round((leftClickPoz1[0] - 230) / 55, 0))
                    x, y = leftClickPoz2
                    mx, my = eg.get_mouse_poz()
                    if str(local_value)[n + 6] == "5" or str(local_value)[n + 6] == "6" or str(local_value)[n + 6] == "7":
                        rx, ry = int(str(local_value)[n + 6]) * 83, int(str(local_value)[n + 5]) * 83
                        if rx + 50 > mx > rx and ry + 50 > my > ry:
                            if x < mx < x + 75 and y < my < y + 25:
                                random.seed(time.time())
                                if len(inventory) < inventorySpace:
                                    inventory.append(random.choices(rockLoot, rockWeight, k=1)[0])
                                else:
                                    print("Not enough space")

                if leftClick:
                    if drawScene == 0:
                        leftClickPoz0 = [0, -100]
                    elif drawScene == 1:
                        leftClickPoz1 = [0, -100]
                    elif drawScene == 2:
                        leftClickPoz2 = [0, -100]

        if not laungAnim:
            if eg.get_mouse_click()[2]:
                mx, my = eg.get_mouse_poz()
                if drawScene == 0:
                    if local_seed(globalX + mx, globalY + my) > 1 - quickSettingsD[1]:
                            leftClick = True
                            leftClickPoz0 = [mx, my]
                            leftClickBackup = [globalX, globalY]
                elif drawScene == 1:
                    leftClick = True
                    leftClickPoz1 = [mx, my]
                    leftClickBackup = [globalX, globalY]
                elif drawScene == 2:
                    leftClick = True
                    leftClickPoz2 = [mx, my]

        if drawScene == 1:
            if eg.get_mouse_click()[0]:
                if not lock1:
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