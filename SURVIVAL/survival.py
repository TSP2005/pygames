import time
import noise
import pygame
import sys

pygame.init()
screen_dim = [960, 640]
screen = pygame.display.set_mode(screen_dim)
pygame.display.set_caption('survival')
display = pygame.Surface((screen_dim[0] // 2, screen_dim[1] // 2))
clock = pygame.time.Clock()

# Load images
player_img = pygame.image.load('data/entities/player/idle/0_idle.png')
player_idle = [pygame.image.load(f'data/entities/player/idle/{i}_idle.png') for i in range(5)]
player_walk = [pygame.image.load(f'data/entities/player/walk/{i}_walk.png') for i in range(6)]
player_walk_up_down = [pygame.image.load(f'data/entities/player/walk_up_down/{i}_walk_up_down.png') for i in range(3)]
zombie_walk = [pygame.image.load(f'data/entities/zombie/walk/{i}_walk.png') for i in range(4)]
snake_move = [pygame.image.load(f'data/entities/snake/move/{i}_move.png') for i in range(3)]
NEIGHBOURS = [(0, -1), (0, 1), (1, 0), (-1, 0)]
player_rect = pygame.Rect(screen_dim[0] // 4, screen_dim[1] // 4, player_img.get_width(), player_img.get_height())
moving_right = False
moving_left = False
moving_up = False
moving_down = False
true_scroll = [0, 0]
scroll = [0, 0]
frame_counter = 0
flip = False
tile_size = 16
chunk_size = 8

# Simple game map
game_map = {}


class Zombie:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, zombie_walk[0].get_width(), zombie_walk[0].get_height())
        self.anim_index = 0
        self.flip = False

    def update(self, target):
        # Animation
        self.anim_index += 1
        if self.anim_index >= 60:
            self.anim_index = 0
        frame_index = (self.anim_index // 15) % len(zombie_walk)
        frame_image = zombie_walk[frame_index]
        if self.flip:
            frame_image = pygame.transform.flip(frame_image, True, False)

        # Movement towards the player
        if self.rect.x < target.x:
            self.rect.x += 1
            self.flip = False
        if self.rect.x > target.x:
            self.rect.x -= 1
            self.flip = True
        if self.rect.y < target.y:
            self.rect.y += 1
        if self.rect.y > target.y:
            self.rect.y -= 1

        # Blit the zombie
        display.blit(frame_image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))


def generate_chunk(x, y):
    chunk_data = []
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            target_x = x * chunk_size + x_pos
            target_y = y * chunk_size + y_pos
            tile_type = 2
            height = noise.pnoise2(target_x * 0.1, target_y * 0.1, repeatx=9999, repeaty=9999)
            if height > -0.2:
                tile_type = 1
            elif height <= -0.2:
                tile_type = 0
            if tile_type != 2:
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data


sand_top_image = pygame.image.load('data/floor/sandfloor/1_sand.png')
sand_image = pygame.image.load('data/floor/sandfloor/4_sand.png')
water_image = pygame.image.load('data/floor/water/0_water.png')
sand_particles = pygame.image.load('data/tiny particles/sand_particles/0.png')
tile_index = [water_image, sand_image]
while True:
    start_time = time.time()
    frame_counter += 1
    if frame_counter >= 60:
        frame_counter = 0

    display.fill((142, 219, 255))

    mpos = pygame.mouse.get_pos()
    mouse_offset = [mpos[0] - screen_dim[0] // 2, mpos[1] - screen_dim[1] // 2]
    true_scroll[0] += (player_rect.x - true_scroll[0] - screen_dim[0] // 4 + (mouse_offset[0]) / 5) / 15
    true_scroll[1] += (player_rect.y - true_scroll[1] - screen_dim[1] // 4 + (mouse_offset[1]) / 5) / 15
    scroll[0] = int(true_scroll[0])
    scroll[1] = int(true_scroll[1])

    for y in range(-2, 4):
        for x in range(-2, 6):
            target_x = x + int(scroll[0] / (chunk_size * tile_size))
            target_y = y + int(scroll[1] / (chunk_size * tile_size))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x, target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]],
                             (tile[0][0] * tile_size - scroll[0], tile[0][1] * tile_size - scroll[1]))

    move_x = (moving_right - moving_left) * 2
    move_y = (moving_down - moving_up) * 2
    if moving_right:
        flip = False
    elif moving_left:
        flip = True

    if move_y != 0 and move_x != 0:
        move_y *= 0.7071
        move_x *= 0.7071

    player_rect.x += move_x
    player_rect.y += move_y

    if moving_left or moving_right or moving_up or moving_down:
        if moving_left or moving_right:
            anim = player_walk
            num_frames = 6
        else:
            anim = player_walk_up_down
            num_frames = 3

        frame_index = (frame_counter // (60 // num_frames)) % num_frames
        frame_image = anim[frame_index]
        if flip:
            frame_image = pygame.transform.flip(frame_image, True, False)
        display.blit(frame_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    else:
        frame_index = (frame_counter // 12) % 5
        frame_image = player_idle[frame_index]
        if flip:
            frame_image = pygame.transform.flip(frame_image, True, False)
        display.blit(frame_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    surf = pygame.transform.scale(display, screen_dim)
    screen.blit(surf, (0, 0))
    end_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    pygame.display.update()
    clock.tick(60)
