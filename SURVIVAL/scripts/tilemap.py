import pygame
import noise
import random


class GameMap:
    def __init__(self):  # tile_size = 16, chunk_size = 8
        self.GameMap = {}
        self.chunk_size = 8
        self.tile_size = 16
        self.render_distance_x = 3
        self.render_distance_y = 2
        self.scale = random.uniform(0.05, 0.1)

    def chunk_generator(self, x, y):
        chunk = []
        spawn_chunks = {(1, 0), (2, 0), (1, 1), (2, 1)}
        for y_pos in range(self.chunk_size):
            for x_pos in range(self.chunk_size):
                target_x = x * self.chunk_size + x_pos
                target_y = y * self.chunk_size + y_pos
                height = noise.pnoise2(target_x * self.scale, target_y * self.scale, repeatx=9999, repeaty=9999)
                if height < -0.3 and (x, y) not in spawn_chunks:
                    tile_type = 0
                else:
                    tile_type = 1
                chunk.append([[target_x, target_y], tile_type])
        return chunk

    def world_render(self, player_pos, surf, scroll, images):
        for i in range(-self.render_distance_x, self.render_distance_x + 1):
            for j in range(-self.render_distance_y, self.render_distance_y + 1):
                target_x = i + player_pos[0] // (self.tile_size * self.chunk_size)
                target_y = j + player_pos[1] // (self.tile_size * self.chunk_size)
                target = str(target_x) + ';' + str(target_y)
                if target not in self.GameMap:
                    self.GameMap[target] = self.chunk_generator(target_x, target_y)
                for tile in self.GameMap[target]:
                    tile_pos = (tile[0][0] * self.tile_size - scroll[0], tile[0][1] * self.tile_size - scroll[1])
                    surf.blit(images[tile[1]], tile_pos)

    def get_tile_type(self, tile_rect):
        chunk_x = tile_rect.x // (self.chunk_size * self.tile_size)
        chunk_y = tile_rect.y // (self.chunk_size * self.tile_size)
        target_chunk = str(chunk_x)+';'+str(chunk_y)
        if target_chunk not in self.GameMap:
            self.GameMap[target_chunk] = self.chunk_generator(chunk_x, chunk_y)
        return self.GameMap[target_chunk][(tile_rect.y//self.tile_size)-chunk_y*self.chunk_size + (tile_rect.x//self.tile_size) - chunk_x*self.chunk_size][1]

# Note: Ensure that images list has enough elements and correct types
