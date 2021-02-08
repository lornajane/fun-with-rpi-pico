import time
import pyb

import picokeypad as keypad

keypad.init()
keypad.set_brightness(1.0)

# 16 keys:
#   0   1   2   3
#   4   5   6   7
#   8   9   a   b
#   c   d   e   f


########### LEVELS ########
# Level 1
red = [0x80, 0x00, 0x00]
blue = [0x00, 0x00, 0x80]
pattern = {
            0: red,
            2: blue,
            7: blue,
            4: red,
            }

###### FUNCTIONS ####

def draw_pattern(pattern):
    for i in range(0,16):
        if i in pattern:
            button = pattern[i]
            keypad.illuminate(i, button[0], button[1], button[2])

    keypad.update()


##### MAIN PROGRAM ###

# draw pattern and wait a few seconds before the next step

draw_pattern(pattern)
time.sleep(3)

# shuffle and draw shuffled
# we don't seem to have much random
print(pyb.rng() * 30)

# handle swapping


# have we won?
