import math
import random

import pygame
import sys
from scripts.entities import Entity as e, Zombie as z
from scripts.tilemap import GameMap
from scripts.utils import Animations


class Game:
    def __init__(self):
        pygame.init()
        self.screen_dim = [640, 480]
        self.screen = pygame.display.set_mode(self.screen_dim)
        self.display = pygame.Surface((self.screen_dim[0] // 2, self.screen_dim[1] // 2))
        pygame.display.set_caption('survival')
        self.game_map = GameMap()
        self.player_loc = [self.screen_dim[0]//4, self.screen_dim[1]//4]
        self.player_state = 'idle'
        self.player_idle_dur = [12, 12, 12, 12, 12]
        self.player_walk_dur = [10, 10, 10, 10, 10, 10]
        self.player = e(self.player_loc, 'player', self.player_state)
        self.player_movement = [0, 0, 0, 0]
        self.movement_y = 0
        self.movement_x = 0
        self.true_scroll = [0, 0]
        self.scroll = [0, 0]
        self.flip = False
        self.clock = pygame.time.Clock()
        water_image = pygame.image.load('data/floor/water/0_water.png')
        sand_image = pygame.image.load('data/floor/sandfloor/4_sand.png')
        self.floor = [water_image, sand_image]
        self.zombies = []
        self.movement_key_bind = {pygame.K_a: 1,
                                  pygame.K_d: 0,
                                  pygame.K_w: 2,
                                  pygame.K_s: 3}

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.player_movement[self.movement_key_bind[event.key]] = 1
            if event.type == pygame.KEYUP:
                self.player_movement[self.movement_key_bind[event.key]] = 0

    def update(self):
        if self.player_movement[0]:
            self.flip = False
        elif self.player_movement[1]:
            self.flip = True
        self.movement_x = (self.player_movement[0] - self.player_movement[1]) * 2
        self.movement_y = (self.player_movement[3] - self.player_movement[2]) * 2
        if self.movement_y != 0 and self.movement_x != 0:
            self.movement_y *= math.sqrt(1 / 2)
            self.movement_x *= math.sqrt(1 / 2)
        if self.player_movement[0] == 1 or self.player_movement[1] == 1:
            self.player.set_state('walk')
        elif self.player_movement[2] == 1 or self.player_movement[3] == 1:
            self.player.set_state('walk_up_down')
        else:
            self.player.set_state('idle')
        self.player_loc[0] += self.movement_x
        self.player_loc[1] += self.movement_y
        self.player.loc[0] = self.player_loc[0]
        mpos = pygame.mouse.get_pos()
        mouse_offset = [mpos[0] - self.screen_dim[0] // 2, mpos[1] - self.screen_dim[1] // 2]
        self.true_scroll[0] += (self.player_loc[0] - self.true_scroll[0] - self.screen_dim[0] // 4 + (mouse_offset[0]) / 5) / 15
        self.true_scroll[1] += (self.player_loc[1] - self.true_scroll[1] - self.screen_dim[1] // 4 + (mouse_offset[1]) / 5) / 15
        self.scroll[0] = int(self.true_scroll[0])
        self.scroll[1] = int(self.true_scroll[1])
        self.spawn_zombies()
        for zombie in self.zombies:
            zombie.goal = self.player_loc
            if zombie.loc[0] > self.player_loc[0]:
                zombie.flip = True
            elif zombie.loc[0] <= self.player_loc[0]:
                zombie.flip = False
            zombie.update()

    def render(self):
        self.display.fill((150, 213, 255))
        self.game_map.world_render(self.player_loc, self.display, self.scroll, self.floor)
        for zombie in self.zombies:
            zombie.render(self.display, self.scroll, zombie.flip)
        self.player.render(self.display, self.scroll, self.flip)
        self.screen.blit(pygame.transform.scale(self.display, (self.screen_dim[0], self.screen_dim[1])), (0, 0))

    def run(self):
        while True:
            self.render()
            self.update()
            self.stay_away_from_water()
            self.event_handler()
            pygame.display.update()
            self.clock.tick(60)

    def spawn_zombies(self):
        spawn_chunk = [random.randint((self.player_loc[0]//128)-3, (self.player_loc[0]//128)+4), random.randint((self.player_loc[1]//128)-2, (self.player_loc[1]//128)+3)]
        if str(spawn_chunk[0])+';'+str(spawn_chunk[1]) not in self.game_map.GameMap:
            self.game_map.GameMap[str(spawn_chunk[0])+';'+str(spawn_chunk[1])] = self.game_map.chunk_generator(spawn_chunk[0], spawn_chunk[1])
        for tile in self.game_map.GameMap[str(spawn_chunk[0])+';'+str(spawn_chunk[1])]:
            if random.randint(0, 5000) == 5 and tile[1] == 1:
                self.zombies.append(z([tile[0][0]*16, tile[0][1]*16]))

    def stay_away_from_water(self):
        water_rects = []
        player_tile = [self.player_loc[0]//16, self.player_loc[1]//16]
        neighbour_tiles = []
        for i in range(-2, 2):
            for j in range(-2, 2):
                neighbour_tiles.append([player_tile[0]+i, player_tile[1]+j])
        for tile in neighbour_tiles:
            x = tile[0]
            y = tile[1]
            chunk_x = tile[0]//8
            chunk_y = tile[1] // 8
            x_pos = tile[0] - chunk_x*8
            y_pos = tile[1] - chunk_y*8
            target_chunk = str(chunk_x)+';'+str(chunk_y)
            if target_chunk not in self.game_map.GameMap:
                self.game_map.GameMap[target_chunk] = self.game_map.chunk_generator(chunk_x, chunk_y)
            if self.game_map.GameMap[target_chunk][int(y_pos*8 + x_pos)][1] == 0:
                water_rects.append(pygame.Rect(x*16, y*16, 8, 8))
        for rect in water_rects:
            print(rect)
            print(self.player_loc)
            self.player.rect = pygame.Rect(self.player_loc[0], self.player_loc[1], self.player.current_anim.get_frame_width(), self.player.current_anim.get_frame_height())
            pygame.draw.rect(self.display, (0, 0, 0), self.player.rect)
            if self.player.rect.colliderect(rect):
                if self.player_movement[0] or self.player_movement[1]:
                    if self.player_movement[1]:
                        self.player.rect.left = rect.right
                        self.player.collisions['left'] = True
                    elif self.player_movement[0]:
                        self.player.rect.right = rect.left
                        self.player.collisions['right'] = True
                if self.player_movement[2] or self.player_movement[3]:
                    if self.player_movement[2]:
                        self.player.rect.top = rect.bottom
                        self.player.collisions['top'] = True
                    elif self.player_movement[3]:
                        self.player.rect.bottom = rect.top
                        self.player.collisions['bottom'] = True
                self.player_loc[0] = self.player.rect.x - self.player.current_anim.get_frame_width()//2
                self.player_loc[1] = self.player.current_anim.get_frame_height()//2


Game().run()
