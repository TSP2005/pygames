import random
import sys
import pygame
import os

screen_dim = [800, 640]


class SpaceShooter:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_dim)
        pygame.display.set_caption('space shooter')
        self.clock = pygame.time.Clock()
        self.surf = pygame.Surface((2 * screen_dim[0] / 3, 2 * screen_dim[1] / 3))
        self.player = pygame.image.load('data/ships/ship_1.png').convert_alpha()
        self.player_rect = self.player.get_rect(center=(screen_dim[0] / 3, screen_dim[1] / 3))
        self.planet_images = load_images('data/planets')
        self.bullet_image = pygame.image.load('data/bullets/turbo_blue.png').convert_alpha()
        self.planets = []
        self.bullets = []
        self.planet_timer = 0
        self.planet_interval = 1500
        self.movement_x = 0
        self.movement_y = 0
        self.speed = 5
        self.collision_count = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over = False

    def run(self):
        while True:
            if not self.game_over:
                self.event_handler()
                self.update()
            self.render()

    def update(self):
        # Update player position
        movement_vector = pygame.math.Vector2(self.movement_x, self.movement_y)
        if movement_vector.length() > 0:
            movement_vector = movement_vector.normalize()

        self.player_rect.x += movement_vector.x * self.speed
        self.player_rect.y += movement_vector.y * self.speed
        self.player_rect.clamp_ip(self.surf.get_rect())

        # Generate planets at intervals
        current_time = pygame.time.get_ticks()
        if current_time - self.planet_timer > self.planet_interval:
            self.planets.append(self.create_planet())
            self.planet_timer = current_time

        # Update bullets' positions and check for collisions
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
            else:
                for planet in self.planets[:]:
                    if bullet.rect.colliderect(planet.rect):
                        self.planets.remove(planet)
                        self.bullets.remove(bullet)
                        self.collision_count += 1
                        break

        # Update planets' positions and check for collisions with player
        for planet in self.planets[:]:
            planet.update()
            if self.check_collision(planet):
                self.game_over = True
                return

        self.planets = [planet for planet in self.planets if planet.rect.top <= self.surf.get_height()]

        pygame.display.update()
        self.screen.blit(self.surf, (0, 0))
        pygame.transform.scale(self.surf, screen_dim, self.screen)
        self.clock.tick(60)

    def render(self):
        self.surf.fill((0, 0, 0))
        self.surf.blit(self.player, self.player_rect)
        for planet in self.planets:
            self.surf.blit(planet.image, planet.rect)
        for bullet in self.bullets:
            self.surf.blit(bullet.image, bullet.rect)

        # Display score (collision count) in the top right
        score_text = self.font.render(f"Score: {self.collision_count}", True, (255, 255, 255))
        score_rect = score_text.get_rect(topright=(self.surf.get_width() - 10, 10))
        self.surf.blit(score_text, score_rect)

        # Display FPS in the top left
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        fps_rect = fps_text.get_rect(topleft=(10, 10))
        self.surf.blit(fps_text, fps_rect)

        if self.game_over:
            self.display_game_over()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.movement_x = -1
                if event.key == pygame.K_RIGHT:
                    self.movement_x = 1
                if event.key == pygame.K_UP:
                    self.movement_y = -1
                if event.key == pygame.K_DOWN:
                    self.movement_y = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.movement_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.movement_y = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bullet = self.create_bullet()
                    self.bullets.append(bullet)

    def create_planet(self):
        planet_image = random.choice(list(self.planet_images.values()))
        planet_rect = planet_image.get_rect(midtop=(random.randint(0, self.surf.get_width()), 0))
        return Planet(planet_image, planet_rect)

    def create_bullet(self):
        bullet_rect = self.bullet_image.get_rect(midbottom=self.player_rect.midtop)
        return Bullet(self.bullet_image, bullet_rect)

    def check_collision(self, planet):
        if planet.hitbox_type == "rect":
            return self.player_rect.colliderect(planet.rect)
        elif planet.hitbox_type == "circle":
            player_center = pygame.math.Vector2(self.player_rect.center)
            planet_center = pygame.math.Vector2(planet.rect.center)
            distance = player_center.distance_to(planet_center)
            return distance < (self.player_rect.width // 2 + planet.hitbox_radius)

    def display_game_over(self):
        game_over_text = self.font.render("You Died", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=self.surf.get_rect().center)
        self.surf.blit(game_over_text, game_over_rect)
        pygame.display.update()
        pygame.time.delay(2000)  # Wait for 2 seconds before closing the game
        pygame.quit()
        sys.exit()


class Planet:
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect
        self.speed = 2
        self.hitbox_type = random.choice(["rect", "circle"])
        if self.hitbox_type == "circle":
            self.hitbox_radius = min(self.rect.width, self.rect.height) // 2

    def update(self):
        self.rect.y += self.speed


class Bullet:
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed


def load_images(directory):
    images = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        image = pygame.image.load(filepath).convert_alpha()
        images[filename] = image
    return images


if __name__ == "__main__":
    game = SpaceShooter()
    game.run()
