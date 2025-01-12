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

def draw_all_coor(game_window, map_file, character, color):
    one_tile = 25
    for xcoor, ycoor in translate_map_char(map_file, character): # for every instance of 'character'
        pygame.draw.rect(game_window, color, (xcoor, ycoor, one_tile, one_tile))

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

    # Start game loop:
    while run:
        pygame.time.delay(75) # determine game speed

        for event in pygame.event.get():  # for all events
            if event.type == pygame.QUIT: # check if game window gets closed
                run = False  # end game loop
                print('Game Closed')

        no_walk_list = translate_map_char('map1.txt', '#') # find unwalkable tiles

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            if x > 0 and [x - one_tile, y] not in no_walk_list:
                x = x - one_tile
            print(f'{x},{y}')

        if keys[pygame.K_RIGHT]:
            if x < 475 and [x + one_tile, y] not in no_walk_list:
                x = x + one_tile
            print(f'{x},{y}')

        if keys[pygame.K_UP]:
            if y > 0 and [x, y - one_tile] not in no_walk_list:
                y = y - one_tile
            print(f'{x},{y}')

        if keys[pygame.K_DOWN]:
            if y < 475 and [x, y + one_tile] not in no_walk_list:
                y = y + one_tile
            print(f'{x},{y}')

        # start testing with ai-wandering:
        x, y = test_ai.move_mob(prev_x, prev_y, x, y, one_tile, no_walk_list)
        # store current x and y for this purpose:
        prev_x = x
        prev_y = y

        game_window.fill((0,0,0))  # fill screen with black
        draw_all_coor(game_window, 'map1.txt', '0', (128,128,128)) # draw all '0' characters as dark gray
        pygame.draw.rect(game_window, (255,0,0), (x, y, one_tile, one_tile))  # draw player
        pygame.display.update() # update screen
        
    pygame.quit()

start_game()
