import random
import pygame

def pick_direction(old_x, old_y, cur_x, cur_y, step):
    pygame.time.delay(10)
    perc = random.random()
    x_diff = cur_x - old_x
    y_diff = cur_y - old_y
    x_ch = 0 if x_diff == 0 else (1 if x_diff > 0 else -1) # collapse change into zero, positive or negative
    y_ch = 0 if y_diff == 0 else (1 if y_diff > 0 else -1) # -"-
    if x_ch == 0 and y_ch == 0:
        if perc < 0.25:
            x_ch = 1
        if perc < 0.50:
            x_ch = -1
        if perc < 0.75:
            y_ch = 1
        if perc < 1.00:
            y_ch = -1

    if perc < 0.75: # continue on path
        print('forward')
        new_x = cur_x + (step * x_ch)
        new_y = cur_y + (step * y_ch)
    elif perc >= 0.75 and perc < 0.80: # turn left
        print('left')
        new_x = cur_x + (step * y_ch)
        new_y = cur_y + (step * x_ch)
    elif perc >= 0.80 and perc < 0.85: # turn right
        print('right')
        new_x = cur_x + (step * (y_ch * -1))
        new_y = cur_y + (step * (x_ch * -1))
#     elif perc >= 0.85 and perc < 0.90: # go back
#         print('back')
#         new_x = cur_x + (step * (x_ch * -1))
#         new_y = cur_y + (step * (y_ch * -1))
    elif perc >= 0.80: # stay
        print('stay')
        new_x = cur_x
        new_y = cur_y
    return [new_x, new_y]

def move_mob(old_x, old_y, cur_x, cur_y, step, unwalkable):
    new_coords = [cur_x, cur_y]
    status = 'undecided'
    while status == 'undecided':
        new_coords = pick_direction(old_x, old_y, cur_x, cur_y, step)
        if new_coords not in unwalkable:
            status = 'decided'
        else:
            old_x = cur_x
            old_y = cur_y
    return new_coords
