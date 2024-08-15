import sys
import pygame

from game import hex_rbg_converter, text, Game

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption('First Game')
play_button = pygame.Rect(screen.get_width() * 3 // 8, screen.get_height() // 2, screen.get_width() // 4,
                          screen.get_height() // 8)
settings_button = pygame.Rect(screen.get_width() * 3 // 8, screen.get_height() * 2 // 3, screen.get_width() // 4,
                              screen.get_height() // 8)
quit_button = pygame.Rect(screen.get_width() * 3 // 8, screen.get_height() * 5 // 6, screen.get_width() // 4,
                          screen.get_height() // 8)
Navy_blue = hex_rbg_converter("#05445E")
Blue_green = hex_rbg_converter('#75E6DA')
Baby_blue = hex_rbg_converter('#D4F1F4')
Blue_grotto = hex_rbg_converter('#189AB4')


def main_menu():
    while True:
        screen.fill(Navy_blue)
        pygame.draw.rect(screen, Blue_grotto, play_button)
        pygame.draw.rect(screen, Blue_grotto, settings_button)
        pygame.draw.rect(screen, Blue_grotto, quit_button)
        if play_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, Blue_green, play_button)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Game().run()
        if settings_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, Blue_green, settings_button)
        if quit_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, Blue_green, quit_button)
        text_font = pygame.font.SysFont('Arial', 30)
        text(screen, 'Play', text_font, Baby_blue, 400, 315)
        text(screen, 'Settings', text_font, Baby_blue, 400, 415)
        text(screen, 'Quit', text_font, Baby_blue, 400, 515)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == '__main__':
    main_menu()
