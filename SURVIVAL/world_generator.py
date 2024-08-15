import json
import numpy as np
from noise import pnoise2


def chunk_generator(center_x, center_y, width, height, scale, octaves, threshold):
    chunk = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            x = center_x - width // 2 + i
            y = center_y - height // 2 + j
            noise_value = pnoise2(x / scale, y / scale, octaves=octaves, persistence=0.5, lacunarity=2.0, repeatx=1024,
                                  repeaty=1024, base=0)
            print("Noise Value at ({}, {}):".format(x, y), noise_value)
            chunk[i][j] = 1 if noise_value > threshold else 0
    return chunk.tolist()


def save_chunk_tojson(chunk, filename):
    with open('map.Json', 'w') as f:
        json.dump(chunk, f)


# Inside the render_world_around_player function
def render_world_around_player(world, player_position, render_distance, CHUNK_SIZE):
    player_x, player_y = player_position
    print("Player Position:", player_x, player_y)
    rendered_world = []
    for i in range(player_x - render_distance, player_x + render_distance + 1):
        row = []
        for j in range(player_y - render_distance, player_y + render_distance + 1):
            chunk_x, chunk_y = i // CHUNK_SIZE, j // CHUNK_SIZE
            print("Chunk Position:", chunk_x, chunk_y)
            if (chunk_x, chunk_y) not in world:
                print("Generating Chunk:", chunk_x, chunk_y)
                world[(chunk_x, chunk_y)] = chunk_generator(chunk_x * CHUNK_SIZE, chunk_y * CHUNK_SIZE, CHUNK_SIZE,
                                                            CHUNK_SIZE, scale, octaves, threshold)
            chunk = world[chunk_x, chunk_y]
            print("Chunk Data:")
            for chunk_row in chunk:
                print(chunk_row)
            row.append(chunk[i % CHUNK_SIZE][j % CHUNK_SIZE])
        rendered_world.append(row)
    return rendered_world


# Parameters
CHUNK_SIZE = 32  # Size of each chunk
scale = 50.0
octaves = 6
threshold = 0.5
player_position = (0, 0)  # Example player position
render_distance = 10  # Render distance around the player

# Initialize world data structure to store generated chunks
world = {}

# Render world around player
rendered_world = render_world_around_player(world, player_position, render_distance, CHUNK_SIZE)

# Print the rendered portion of the world (for demonstration)
for row in rendered_world:
    print(row)
