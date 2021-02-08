import time
import urandom

import picokeypad as keypad

keypad.init()
keypad.set_brightness(1.0)
game_in_progress = 0
level = 0;

# 16 keys:
#   0   1   2   3
#   4   5   6   7
#   8   9   a   b
#   c   d   e   f

######### COLOURS #######
red = [0x80, 0x00, 0x00]
blue = [0x00, 0x00, 0x80]
purple = [0x30, 0x00, 0xff]
pink = [0x50, 0x10, 0x8f]
yellow = [0x50, 0x50, 0x00]
green = [0x10, 0xff, 0x00]
teal = [0x00, 0x30, 0xff]

########### LEVELS ########
levels = {}

levels[1] = {
            9: red,
            6: yellow,
            }

levels[2] = {
            1: yellow,
            7: teal,
            8: green
            }

levels[3] = {
            0: pink,
            2: blue,
            7: blue,
            4: pink,
            12: purple
            }

###### FUNCTIONS ####

def draw_pattern(pattern):
    keypad.clear()

    for i in range(16):
        if i in pattern:
            button = pattern[i]
            keypad.illuminate(i, button[0], button[1], button[2])

    keypad.update()

def won():
    on = 1

    while True:
        # flash key 15
        if on:
            keypad.illuminate(15, 0x00, 0x80, 0x00)
            on = 0
        else:
            keypad.illuminate(15, 0x00, 0x00, 0x00)
            on = 1

        keypad.update()
        time.sleep(1)

        # return when key 15 is pressed
        if keypad.get_button_states() == 32768:
            return
    

##### MAIN PROGRAM ###

def init(pattern):
    # draw pattern and wait a few seconds before the next step
    draw_pattern(pattern)
    time.sleep(3)

    # shuffle and draw current_lights, kind of DIY solution
    current_lights = {}

    # represents the original pattern, this handles gaps
    options = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    for i in range(16):
        # pick an option
        pick = urandom.choice(options)

        # use that value from the original pattern, remove this from the options
        if pick in pattern:
            current_lights[i] = pattern[pick]
        
        options.remove(pick)

    draw_pattern(current_lights)
    return current_lights

######### EVENT LOOP #########
while True:
    # initialise if appropriate
    if game_in_progress == 0:
        level = level + 1
        if level not in levels:
            level = 1
        winning_pattern = levels[level]
        current_lights = init(winning_pattern)
        game_in_progress = 1

    pressed = []
    button_states = keypad.get_button_states()

    # figure out what's pressed
    for i in range(16):
        if (button_states >> i) & 0x01 != 0:
            pressed.append(i)

    # were two buttons pressed? Swap them and redraw
    if len(pressed) == 2:
        lights = {}
        indexes = {}
        place = "first"
        for p in pressed:
            indexes[place] = p
            if p in current_lights:
                lights[place] = current_lights[p]
            else:
                lights[place] = []
            place = "second"

        # does this index exist? and should it after this? (err... twice)
        if len(lights["second"]):
            current_lights[indexes["first"]] = lights["second"]
        else:
            if indexes["first"] in current_lights:
                del current_lights[indexes["first"]]

        if len(lights["first"]):
            current_lights[indexes["second"]] = lights["first"]
        else:
            if indexes["second"] in current_lights:
                del current_lights[indexes["second"]]

        draw_pattern(current_lights)

    time.sleep(0.5)

    # check if we won (suspense intentional)
    if current_lights == winning_pattern:
        game_in_progress = 0
        won()
