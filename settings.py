import pygame
from random import choice

class Settings:
    """Класс для хранения всех настроек игры Alien Invasion."""
    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 30, 30)
        self.bg = pygame.image.load(f'images/bg{str(choice(range(4)))}.jpg')
        self.bg_rect = self.bg.get_rect()
        # Параметры снаряда
        self.bullet_speed = 5
        self.bullets_allowed = 3
        # Параметры звука и музыки
        pygame.mixer.music.load(f'music/{str(choice(range(4)))}.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(50)
        #Параметры шрифта
        pygame.font.init()
        self.my_font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 30)
        #Настройки пришельцев
        self.alien_speed = 3
        self.fleet_drop_speed = 20
        self.alien_acceleration = 1
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1
        # Количество жизней
        self.ship_limit = 3
