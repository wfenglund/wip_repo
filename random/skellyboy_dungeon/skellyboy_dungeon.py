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

def maintain_mob(game_window, mob_list, player_coords, attack_coords, weapon_dmg):
    one_tile = 25

    if attack_coords != 'undefined': # if player is attacking
        new_mob_list = []
        for mob in mob_list:
            if mob['coords'] == attack_coords:
                mob['status'] = 'attacked'
                if weapon_dmg < mob['hitpoints']:
                    mob['damage'] = weapon_dmg
                else:
                    mob['damage'] = mob['hitpoints']
                mob['hitpoints'] = mob['hitpoints'] - weapon_dmg
                mob['coords'][0] = mob['coords'][0] + (mob['coords'][0] - player_coords[0]) * 2 # make mob bounce back from being hit
                mob['coords'][1] = mob['coords'][1] + (mob['coords'][1] - player_coords[1]) * 2 # -"-
            new_mob_list = new_mob_list + [mob]
        mob_list = new_mob_list
 
    new_mob_list = []
    for mob in mob_list:
        # draw mob:
        pygame.draw.rect(game_window, (255, 255, 255), (mob['coords'][0], mob['coords'][1], one_tile, one_tile))
        
        # add hitpoints bar:
        pygame.draw.rect(game_window, (255, 0, 0), (mob['coords'][0], mob['coords'][1], one_tile, one_tile / 10))
        pygame.draw.rect(game_window, (0, 255, 0), (mob['coords'][0], mob['coords'][1], one_tile * (mob['hitpoints'] / mob['max_hp']), one_tile / 10))

        if mob['status'] == 'attacked': # do something if mob is attacked
            hit_font = pygame.font.SysFont('Comic Sans MS', 30)
            hit_surface = hit_font.render('-' + str(mob['damage']), False, (255, 0, 0)) # draw hitsplat
            game_window.blit(hit_surface, (mob['coords'][0], mob['coords'][1]))
#             pygame.draw.rect(game_window, (255, 0, 0), (mob['coords'][0], mob['coords'][1], one_tile, one_tile))
            mob['status'] = 'normal'
        if mob['hitpoints'] > 0:
            new_mob_list = new_mob_list + [mob]
    return new_mob_list
        

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
    pygame.font.init()

    # Assign variables:
    x = 250 # starting x coordinate
    y = 475 # starting y coordinate
    one_tile = 25 # determine fundamental unit of measurement
    run = True
    prev_x = x
    prev_y = y
    cur_map = 'map1' # prefix name of the starting map
    weapon_dmg = 2 # assign how much damage attacking does does

    # Mob list:
    mob1 = {}
    mob1['coords'] = [125, 125]
    mob1['max_hp'] = 5
    mob1['hitpoints'] = mob1['max_hp']
    mob1['status'] = 'normal'
    mob_list = [mob1]
    mob_delayer = 1

    # Start game loop:
    while run:
        pygame.time.delay(75) # determine game speed

        for event in pygame.event.get():  # for all events
            if event.type == pygame.QUIT: # check if game window gets closed
                run = False  # end game loop
                print('Game Closed')

        no_walk_list = translate_map_char(cur_map + '.maplay', '#') # find unwalkable tiles
        no_walk_list = no_walk_list + [i['coords'] for i in mob_list]
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
#         new_mob_list = []
#         for mob in mob_list:
#             mob['coords'] = test_ai.move_mob(mob['coords'][0], mob['coords'][1], mob['coords'][0], mob['coords'][1], one_tile, no_walk_list)
#             new_mob_list = new_mob_list + [mob]
#         mob_list = new_mob_list

        if str(x) + ',' + str(y) in connection_dict.keys():
            connection_info = connection_dict[str(x) + ',' + str(y)]
            cur_map = connection_info[0].strip()
            coord_list = connection_info[1].split(',')
            x = int(coord_list[0].strip())
            y = int(coord_list[1].strip())
        
        if mob_delayer == 1: # make this whole indentation into a function
            new_mob_list = []
            for mob in mob_list:
                mob_x = mob['coords'][0]
                mob_y = mob['coords'][1]
                x_diff = mob_x - x
                y_diff = mob_y - y
                if x_diff > 0:
                    mob_x = mob_x - one_tile
                elif x_diff < 0:
                    mob_x = mob_x + one_tile
                if y_diff > 0:
                    mob_y = mob_y - one_tile
                elif y_diff < 0:
                    mob_y = mob_y + one_tile
                if [mob_x, mob_y] != [x, y] and [mob_x, mob_y] not in no_walk_list:
                    mob['coords'] = [mob_x, mob_y]
                new_mob_list = new_mob_list + [mob]
            mob_list = new_mob_list
            
        mob_delayer = mob_delayer + 1
        if mob_delayer > 3:
            mob_delayer = 1

        game_window.fill((0,0,0))  # fill screen with black
#         draw_all_coor(game_window, 'map1.txt', '0', (128,128,128), 'color') # draw all '0' characters as dark gray
        draw_all_coor(game_window, cur_map + '.maplay', '0', ('tile_test.png'), 'picture') # draw all '0' characters as test tile
        pygame.draw.rect(game_window, (255,0,0), (x, y, one_tile, one_tile))  # draw player

        attack_coords = 'undefined'
        if keys[pygame.K_SPACE]:
            sword_test = pygame.image.load('test_sword.png').convert_alpha() # load image
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                attack_coords = [x, y - one_tile]
                print('attack up')
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                attack_coords = [x, y + one_tile]
                sword_test = pygame.transform.rotate(sword_test, 180) # rotate sword downwards
                print('attack down')
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                attack_coords = [x - one_tile, y]
                sword_test = pygame.transform.rotate(sword_test, 90) # rotate sword to the left
                print('attack left')
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                attack_coords = [x + one_tile, y]
                sword_test = pygame.transform.rotate(sword_test, 270) # rotate sword to the right
                print('attack right')

        mob_list = maintain_mob(game_window, mob_list, [x, y], attack_coords, weapon_dmg)
        
        if attack_coords != 'undefined':
            game_window.blit(sword_test, (attack_coords[0], attack_coords[1]))

        pygame.display.update() # update screen
        
        # store current x and as previous x and y:
        prev_x = x
        prev_y = y
        
    pygame.quit()

start_game()
