import random

def generate_numbers(n_nums, blocked_nums, blocked_coords):
    num_list = [blocked_nums[blocked_coords.index(i)] if i in blocked_coords else 0 for i in range(0, n_nums)]
    counter = 0
    while 0 in num_list:
        cur_num = random.randint(1, 9)
        if cur_num not in num_list:
            num_list[num_list.index(0)] = cur_num
        counter = counter + 1
        if counter >= 1000:
            print('Too many iterations.')
            break
    return num_list

def generate_line(kakuro_list):
    line = 'processing'
    while line == 'processing':
        crossing_line = kakuro_list[random.randint(0, len(kakuro_list) - 1)]
        intersect_index = random.randint(0, len(crossing_line[1]) - 1)
        line_len = random.randint(2, 9)
        cur_intersect = random.randint(0, line_len - 1)
        intersect_value = crossing_line[0][intersect_index]
        new_line = generate_numbers(line_len, [crossing_line[0][intersect_index], [cur_intersect])
        
        intersect_coords = crossing_line[1][intersect_index]
        print(intersect_coords)
        if intersect_index == intersect_coords[0]: # if line goes along y axis
            new_coords = [[intersect_coords[0], i + (intersect_coords[1] - new_line.index(intersect_value))] for i in range(0, line_len)]
        if intersect_index == intersect_coords[1]: # if line goes along x axis
            new_coords = [[i, intersect_coords[1]] for i in range(0, line_len)]
            new_coords = [[i + (intersect_coords[0] - new_line.index(intersect_value)), intersect_coords[1]] for i in range(0, line_len)]

        # needs to:
        # - generate coordinates so that intersecting number has the same coordinates in both entries
        # - check if other lines are intersected
        # - check and try again if the line is not logical or possible (sum wise etc)
        
        new_entry = [[new_line] + [new_coords]]
        return kakuro_list + new_entry

intersects = 2

kakuro_list = [] # an entry has the format [line, coords]
for lines in range(intersects):
    if len(kakuro_list) > 0:
        kakuro_list = generate_line(kakuro_list)
    else:
        line_len = random.randint(2, 9)
        cur_line = generate_numbers(line_len, [], [])
        cur_coords = [[x, 0] for x in range(0, len(cur_line))]
        kakuro_list = kakuro_list + [[cur_line, cur_coords]]

for i in kakuro_list:
    print(i)
