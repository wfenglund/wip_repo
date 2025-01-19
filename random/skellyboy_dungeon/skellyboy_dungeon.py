import pygame
import test_ai

def translate_map_char(map_file, character): # Get all coordinates of a character in a map file
    with open(map_file) as raw_map:
        map_list = []
        row = 0
        one_tile = 25
        for lines in raw_map:
            map_list = map_list + [[col*one_tile, row*one_tile] for col, char in enumerate(lines.strip()) if char == character]
            row = row + 1
        return map_list

def parse_mapinf(map_file):
    connection_dict = {}
    with open(map_file) as map_info:
        for line in map_info:
            if line.startswith('connection:'):
                raw_connection = line.strip().replace('connection:', '')
                coords, new_loc = raw_connection.split('=')
                connection_dict[coords] = new_loc.split(':')
    return connection_dict

def draw_all_coor(game_window, map_file, character, color, choice):
    one_tile = 25
    if choice == 'color':
        for xcoor, ycoor in translate_map_char(map_file, character): # for every instance of 'character'
            pygame.draw.rect(game_window, color, (xcoor, ycoor, one_tile, one_tile))
    if choice == 'picture':
        tile_test = pygame.image.load(color).convert() # load image
        for xcoor, ycoor in translate_map_char(map_file, character): # for every instance of 'character'
            game_window.blit(tile_test, (xcoor, ycoor))

def start_game():
    # Initiate game:
    pygame.init()
    game_window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Skellyboy Dungeon")

    # Assign variables:
    x = 250 # starting x coordinate
    y = 475 # starting y coordinate
    one_tile = 25 # determine fundamental unit of measurement
    run = True
    prev_x = x
    prev_y = y
    cur_map = 'map1' # prefix name of the starting map

    # Start game loop:
    while run:
        pygame.time.delay(75) # determine game speed

        for event in pygame.event.get():  # for all events
            if event.type == pygame.QUIT: # check if game window gets closed
                run = False  # end game loop
                print('Game Closed')

        no_walk_list = translate_map_char(cur_map + '.maplay', '#') # find unwalkable tiles
        connection_dict = parse_mapinf(cur_map + '.mapinf')

        keys = pygame.key.get_pressed()
        
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not keys[pygame.K_SPACE]:
            if y > 0 and [x, y - one_tile] not in no_walk_list:
                y = y - one_tile
            elif str(x) + ',' + str(y - one_tile) in connection_dict.keys():
                y = y - one_tile
                print('connection')
            print(f'{x},{y}')

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not keys[pygame.K_SPACE]:
            if y < 475 and [x, y + one_tile] not in no_walk_list:
                y = y + one_tile
            elif str(x) + ',' + str(y + one_tile) in connection_dict.keys():
                y = y + one_tile
                print('connection')
            print(f'{x},{y}')

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not keys[pygame.K_SPACE]:
            if x > 0 and [x - one_tile, y] not in no_walk_list:
                x = x - one_tile
            elif str(x - one_tile) + ',' + str(y) in connection_dict.keys():
                x = x - one_tile
                print('connection')
            print(f'{x},{y}')

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not keys[pygame.K_SPACE]:
            if x < 475 and [x + one_tile, y] not in no_walk_list:
                x = x + one_tile
            elif str(x + one_tile) + ',' + str(y) in connection_dict.keys():
                x = x + one_tile
                print('connection')
            print(f'{x},{y}')

        # start testing with ai-wandering:
#         x, y = test_ai.move_mob(prev_x, prev_y, x, y, one_tile, no_walk_list)

        if str(x) + ',' + str(y) in connection_dict.keys():
            connection_info = connection_dict[str(x) + ',' + str(y)]
            cur_map = connection_info[0].strip()
            coord_list = connection_info[1].split(',')
            x = int(coord_list[0].strip())
            y = int(coord_list[1].strip())

        game_window.fill((0,0,0))  # fill screen with black
#         draw_all_coor(game_window, 'map1.txt', '0', (128,128,128), 'color') # draw all '0' characters as dark gray
        draw_all_coor(game_window, cur_map + '.maplay', '0', ('tile_test.png'), 'picture') # draw all '0' characters as test tile
        pygame.draw.rect(game_window, (255,0,0), (x, y, one_tile, one_tile))  # draw player
        if keys[pygame.K_SPACE]:
            sword_test = pygame.image.load('test_sword.png').convert_alpha() # load image
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                game_window.blit(sword_test, (x, y - one_tile))
                print('attack up')
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                sword_test_down = pygame.transform.rotate(sword_test, 180) # rotate sword downwards
                game_window.blit(sword_test_down, (x, y + one_tile))
                print('attack down')
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                sword_test_left = pygame.transform.rotate(sword_test, 90) # rotate sword to the left
                game_window.blit(sword_test_left, (x - one_tile, y))
                print('attack left')
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                sword_test_right = pygame.transform.rotate(sword_test, 270) # rotate sword to the right
                game_window.blit(sword_test_right, (x + one_tile, y))
                print('attack right')
        pygame.display.update() # update screen
        
        # store current x and as previous x and y:
        prev_x = x
        prev_y = y
        
    pygame.quit()

start_game()
