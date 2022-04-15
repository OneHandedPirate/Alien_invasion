import pygame

class Settings:
    """Класс для хранения всех настроек игры Alien Invasion."""
    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 30, 30)
        self.bg = pygame.image.load('images/bg.jpg')
        self.bg_rect = self.bg.get_rect()
        # Параметры снаряда
        self.bullet_speed = 1
        self.bullets_allowed = 3