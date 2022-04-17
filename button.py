import pygame

class Button:
    def __init__(self, ai_game):
        """Инициализирует атрибуты кнопки."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Построение объекта rect кнопки и выравнивание по центру экрана.
        self.butt = pygame.image.load('images/start.png')
        self.rect = self.butt.get_rect()
        self.rect.center = self.screen_rect.center

    def draw_button(self):
        self.screen.blit(self.butt, (380, 300))