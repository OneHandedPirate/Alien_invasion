import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from random import choice


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self)
        self.invis_mouse = pygame.mouse.set_visible(False)
        self.grab_mouse = pygame.event.set_grab(True)
        self.bullets = pygame.sprite.Group()
        self.music = pygame.mixer.music.load(f'music/{str(choice(range(1,5)))}.mp3')
        self.music_play = pygame.mixer.music.play()
        self.music_volume = pygame.mixer.music.set_volume(0.5)

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            # Отслеживание событий клавиатуры и мыши.
            self._check_events()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE)):
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                if event.pos[0] < (self.settings.screen_width-100):
                    self.ship.rect.x = event.pos[0]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._fire_bullet()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                pygame.mixer.music.set_volume((pygame.mixer.music.get_volume() + 0.1))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                pygame.mixer.music.set_volume((pygame.mixer.music.get_volume() - 0.1))

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.blit(self.settings.bg, self.settings.bg_rect)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullets()
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()