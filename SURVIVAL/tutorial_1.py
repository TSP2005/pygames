import pygame
import sys

pygame.init()
screen_dim = [960, 640]
screen = pygame.display.set_mode((screen_dim[0], screen_dim[1]))
display = pygame.Surface((screen_dim[0] // 2, screen_dim[1] // 2))
pygame.display.set_caption('sample')
clock = pygame.time.Clock()

# Load images
player_image = pygame.image.load('data/entities/player/idle/0_idle.png')
sand_top_image = pygame.image.load('data/floor/sandfloor/1_sand.png')
sand_image = pygame.image.load('data/floor/sandfloor/4_sand.png')

# Preload animations
idle_animation = [pygame.image.load(f'data/entities/player/idle/{i}_idle.png') for i in range(5)]
walk_animation = [pygame.image.load(f'data/entities/player/walk/{i}_walk.png') for i in range(6)]

movement_x = [False, False]
player_pos = [50, 50]
player_y_momentum = 0
player_rect = pygame.Rect(player_pos[0], player_pos[1], player_image.get_width(), player_image.get_height())
tile_size = 16
PHYSICS_TILES = {1, 2}
NEIGHBOUR_TILES = [[1, 0], [-1, 0], [0, 1], [0, -1], [0, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
backgrounds = [[0.25, 100, 100, 40, 400], [0.5, 10, 100, 50, 300], [0.25, 200, 300, 60, 400], [0.5, 300, 20, 50, 100]]
air_time = 0
jumps = 1
true_scroll = [0, 0]
frame_counter = 0


def load_map(path):
    with open(path, 'r') as f:
        data = f.read().split('\n')
    return [list(row) for row in data]


Game_map = load_map('map')


def collision_test(rect, tiles):
    return [tile for tile in tiles if rect.colliderect(tile)]


def move(rect, movement, tiles):
    collision_types = {'right': False, 'left': False, 'top': False, 'bottom': False}
    rect.x += movement[0]
    hit_box = collision_test(rect, tiles)
    for tile in hit_box:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_box = collision_test(rect, tiles)
    for tile in hit_box:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def get_animation_frame(animation, frame_counter, flip=False):
    frame = animation[frame_counter // (60 // len(animation)) % len(animation)]
    return pygame.transform.flip(frame, flip, False)


while True:
    frame_counter = (frame_counter + 1) % 60
    true_scroll[0] += (player_rect.x - true_scroll[0] - 240) / 15
    true_scroll[1] += (player_rect.y - true_scroll[1] - 160) / 15
    scroll = [int(true_scroll[0]), int(true_scroll[1])]
    display.fill((148, 241, 255))

    player_movement = [0, 0]
    if movement_x[0]:
        player_movement[0] += 2
    if movement_x[1]:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum = min(player_y_momentum + 0.2, 3)

    background_rects = []
    for background in backgrounds:
        obj_rect = pygame.Rect(background[1] - scroll[0] * background[0], background[2] - scroll[1] * background[0],
                               background[3], background[4])
        background_rects.append(obj_rect)
        color = (0, 140, 0) if background[0] == 0.5 else (0, 200, 0)
        pygame.draw.rect(display, color, obj_rect)

    tile_rects = []
    for y, row in enumerate(Game_map):
        for x, tile in enumerate(row):
            if tile == '1':
                display.blit(sand_image, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
            elif tile == '2':
                display.blit(sand_top_image, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))

    player_rect, collision_types = move(player_rect, player_movement, tile_rects)
    if collision_types['bottom']:
        player_y_momentum = 0
        air_time = 0
        jumps = 1
    else:
        air_time += 1
    if collision_types['top']:
        player_y_momentum = 0

    if not any(movement_x):
        frame = get_animation_frame(idle_animation, frame_counter)
    elif movement_x[0]:
        frame = get_animation_frame(walk_animation, frame_counter)
    elif movement_x[1]:
        frame = get_animation_frame(walk_animation, frame_counter, flip=True)

    display.blit(frame, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                movement_x[1] = True
            if event.key == pygame.K_RIGHT:
                movement_x[0] = True
            if event.key == pygame.K_SPACE and air_time < 12 and jumps == 1:
                player_y_momentum = -5
                jumps = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                movement_x[1] = False
            if event.key == pygame.K_RIGHT:
                movement_x[0] = False

    surf = pygame.transform.scale(display, screen_dim)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)
