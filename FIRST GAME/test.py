import pygame
import sys


def hex_rbg_converter(hex_col):
    hex_col = hex_col.lstrip('#')
    return tuple(int(hex_col[i: i+2], 16) for i in (0, 2, 4))


class Game:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.outlines = [pygame.Rect(0, 0, 800, 100), pygame.Rect(0, 100, 10, 490), pygame.Rect(0, 590, 800, 10), pygame.Rect(790, 100, 10, 490)]
        self.tealgreen = hex_rbg_converter('#167D7F')
        self.teal = hex_rbg_converter('#29A0B1')
        self.tile_size = 15
        self.snake = Snake(self)

    def run(self):
        while True:
            self.screen.fill(self.tealgreen)
            for outline in self.outlines:
                pygame.draw.rect(self.screen, self.teal, outline)

            self.snake.move()
            self.snake.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.snake.movement = [True, False, False, False]
                    if event.key == pygame.K_LEFT:
                        self.snake.movement = [False, True, False, False]
                    if event.key == pygame.K_UP:
                        self.snake.movement = [False, False, True, False]
                    if event.key == pygame.K_DOWN:
                        self.snake.movement = [False, False, False, True]

            pygame.display.update()
            self.clock.tick(5)


class Snake:
    def __init__(self, game):
        self.game = game
        self.snake = [pygame.Rect(self.game.width // 2, self.game.height // 2, self.game.tile_size, self.game.tile_size)]
        self.snake_color = (0, 255, 0)
        self.movement = [False, False, False, False]  # Right, Left, Up, Down

    def move(self):
        head = self.snake[0].copy()
        if self.movement[0]:
            head.x += self.game.tile_size
        if self.movement[1]:
            head.x -= self.game.tile_size
        if self.movement[2]:
            head.y -= self.game.tile_size
        if self.movement[3]:
            head.y += self.game.tile_size

        # Insert new head position
        self.snake.insert(0, head)
        # Remove last segment of the snake
        self.snake.pop()

    def render(self, surf):
        for bit in self.snake:
            pygame.draw.rect(surf, self.snake_color, bit)


Game().run()
