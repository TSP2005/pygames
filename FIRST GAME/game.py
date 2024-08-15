import pygame
import sys
import random


def text(surf, string, font, text_col, x, y):
    img = font.render(string, True, text_col)
    surf.blit(img, (x, y))


def hex_rbg_converter(hex_col):
    hex_col = hex_col.lstrip('#')
    return tuple(int(hex_col[i: i + 2], 16) for i in (0, 2, 4))


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.width = 900
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('snake game')
        self.clock = pygame.time.Clock()
        self.outlines = {'top': pygame.Rect(0, 0, 900, 105),
                         'left': pygame.Rect(0, 100, 15, 485),
                         'bottom': pygame.Rect(0, 585, 900, 15),
                         'right': pygame.Rect(885, 100, 15, 485)}
        self.tealgreen = hex_rbg_converter('#167D7F')
        self.teal = hex_rbg_converter('#29A0B1')
        self.spearmint = hex_rbg_converter('#98D7C2')
        self.tile_size = 15
        self.snake = Snake(self)
        self.food = Food(self, self.snake)
        self.score = 0
        self.highscore = 0
        self.pause_button = pygame.Rect(450, 20, 30, 30)
        self.FPS = 10
        self.paused = False
        self.blue_green = hex_rbg_converter('#75E6DA')
        self.blue_grotto = hex_rbg_converter('#189AB4')
        self.baby_blue = hex_rbg_converter('#D4F1F4')
        self.textfont = pygame.font.SysFont('Arial', 30)
        self.resume_button = pygame.Rect(self.width * 3 // 8, self.height * 3 // 8, self.width // 4, self.height // 8)
        self.quit_button = pygame.Rect(self.width * 3 // 8, self.height * 5 // 8 - 50, self.width // 4,
                                       self.height // 8)

    def run(self):
        with open('highscore.txt', 'r') as file:
            self.highscore = int(file.read().split(':')[1].strip())
        while True:
            self.handle_events()
            if not self.paused:
                self.update()
            self.render()
            pygame.display.update()
            self.clock.tick(self.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('highscore.txt', 'w') as file:
                    file.write(f'highscore:{self.highscore}')
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not self.snake.movement[1]:
                    self.snake.movement = [False, False, False, False]
                    self.snake.movement[0] = True
                if event.key == pygame.K_LEFT and not self.snake.movement[0]:
                    self.snake.movement = [False, False, False, False]
                    self.snake.movement[1] = True
                if event.key == pygame.K_UP and not self.snake.movement[3]:
                    self.snake.movement = [False, False, False, False]
                    self.snake.movement[2] = True
                if event.key == pygame.K_DOWN and not self.snake.movement[2]:
                    self.snake.movement = [False, False, False, False]
                    self.snake.movement[3] = True
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_button.collidepoint(event.pos):
                    self.paused = not self.paused
                if self.paused and self.resume_button.collidepoint(event.pos):
                    self.paused = not self.paused
                if self.quit_button.collidepoint(event.pos):
                    with open('highscore.txt', 'w') as file:
                        file.write(f'highscore:{self.highscore}')
                    return

    def update(self):
        self.snake.move()
        self.food.spawn()
        if self.food.exists:
            if self.food.food.colliderect(self.snake.snake[0]):
                self.food.exists = 0
                self.snake.eat()
                self.score += 1
                self.highscore = max(self.score, self.highscore)
        for outline in self.outlines.values():
            if self.snake.snake[0].colliderect(outline):
                self.reset()
        if (self.snake.snake[0].x, self.snake.snake[0].y) in self.snake.pos:
            self.highscore = max(self.score, self.highscore)
            self.reset()
        self.FPS += 0.003

    def render(self):
        self.screen.fill(self.tealgreen)
        self.textfont = pygame.font.SysFont('Arial', 30)
        for outline in self.outlines.values():
            pygame.draw.rect(self.screen, self.teal, outline)
        pygame.draw.rect(self.screen, (0, 255, 0), self.pause_button)
        pygame.draw.polygon(self.screen, (255, 255, 255), [(460, 25), (460, 45), (475, 35)])
        self.snake.render(self.screen)
        self.food.render(self.screen)
        text(self.screen, f'Score : {self.score} ', self.textfont, self.spearmint, 20, 20)
        text(self.screen, f'high score: {self.highscore}', self.textfont, self.spearmint, 710, 20)
        if self.paused:
            self.pause_screen()

    def reset(self):
        self.snake.__init__(self)
        self.score = 0
        self.FPS = 10

    def pause_screen(self):
        pausescreen_rect = pygame.Rect(self.width // 4, self.height // 4, self.width // 2, self.height // 2)
        pygame.draw.rect(self.screen, self.blue_green, pausescreen_rect)
        pygame.draw.rect(self.screen, self.blue_grotto, self.resume_button)
        text(self.screen, 'resume', self.textfont, self.baby_blue, self.width // 2 - 50, self.height // 2 - 50)
        pygame.draw.rect(self.screen, self.blue_grotto, self.quit_button)
        text(self.screen, 'Back', self.textfont, self.baby_blue, self.width // 2 - 50, self.height // 2 + 50)


class Snake:
    def __init__(self, game):
        self.food = None
        self.game = game
        self.snake = []
        self.snake.append(
            pygame.Rect(self.game.width // 2, self.game.height // 2, self.game.tile_size, self.game.tile_size))
        self.snake_color = (0, 255, 0)
        self.movement = [False, False, False, False]
        self.pos = set((self.snake[i].x, self.snake[i].y) for i in range(len(self.snake)))
        self.state = 'None'

    def move(self):
        head = self.snake[0].copy()
        head.x += (self.movement[0] - self.movement[1]) * self.game.tile_size
        head.y += (self.movement[3] - self.movement[2]) * self.game.tile_size
        self.snake.insert(0, head)
        self.snake.pop()
        self.pos = set((self.snake[i].x, self.snake[i].y) for i in range(1, len(self.snake)))

    def render(self, surf):
        for bit in self.snake:
            pygame.draw.rect(surf, self.snake_color, bit)

    def eat(self):
        self.snake.insert(len(self.snake) - 1, self.snake[-1])


class Food:
    def __init__(self, game, snake):
        self.snake = snake
        self.color = (255, 0, 0)
        self.game = game
        self.exists = 0
        self.pos = [0, 0]
        self.food = pygame.Rect(0, 0, 0, 0)
        self.pos[0] = (random.randint(15, 885) // self.game.tile_size) * self.game.tile_size
        self.pos[1] = (random.randint(105, 585) // self.game.tile_size) * self.game.tile_size

    def spawn(self):
        while (self.pos[0], self.pos[1]) in self.snake.pos:
            self.pos[0] = (random.randint(15, 885) // self.game.tile_size) * self.game.tile_size
            self.pos[1] = (random.randint(105, 585) // self.game.tile_size) * self.game.tile_size
        if self.exists == 0:
            self.food = pygame.Rect(self.pos[0], self.pos[1], self.game.tile_size, self.game.tile_size)
            self.exists = 1

    def render(self, surf):
        if self.exists:
            pygame.draw.rect(surf, self.color, self.food)


Game().run()
