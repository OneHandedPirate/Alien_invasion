import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from random import choice
from time import sleep
from game_stats import GameStats
from button import Button
from pygame.sprite import Group


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        pygame.display.set_caption('Alien Invasion')
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.event.set_grab(True)
        self.invis_mouse = pygame.mouse.set_visible(False)
        self.stats = GameStats(self)
        self.bullets = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.aliens = pygame.sprite.Group()
        self.score_count = 0
        self.ship = Ship(self)
        self._create_fleet()
        self.play_button = Button(self)
        self.fleet_count = 1
        self.exp = pygame.image.load('images/blast/3.png')
        self.exp_rect = self.exp.get_rect()
        self.lives_left()
        with open('High_score.txt') as hs:
            high_score = hs.read()
            self.high = high_score[:]


    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEMOTION and self.stats.game_active == True:
                if event.pos[0] < (self.settings.screen_width-100):
                    self.ship.rect.x = event.pos[0]
            elif event.type == pygame.MOUSEBUTTONDOWN and self.stats.game_active == True:
                self._fire_bullet()

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            fire = pygame.mixer.Sound(f'sounds/blast{choice(range(3))}.mp3')
            fire.set_volume(0.5)
            fire.play()

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Проверка попаданий в пришельцев.
        # При обнаружении попадания удалить снаряд и пришельца.

        self._check_bullet_alien_collision()

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец — корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверить, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()

    def game_over(self):
        if self.stats.ship_left == 0:
            self.aliens.empty()
            self.bullets.empty()
            self.ship.image.set_alpha(0)
            game_over = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 90).render('GAME OVER', True, (200, 200, 200))
            high_score = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 50).render('high score', True, (200, 200, 200))
            total_score = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 50).render(f'{"0"*(8-len(str(self.score_count)))}{self.score_count}', True, (200, 200, 200))
            restart = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 30).render('press R to restart or Esc to exit', True, (200, 200, 200))
            self.screen.blit(game_over, (415, 300))
            self.screen.blit(high_score, (495, 400))
            self.screen.blit(total_score, (510, 450))
            self.screen.blit(restart, (410, 550))
            self.stats.game_active = False

    def lives_left(self):
        """Сообщает количество оставшихся кораблей."""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self)
            ship.image = pygame.image.load(f'images/ship_small.png')
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def _check_bullet_alien_collision(self):
        """Обработка коллизий снарядов с пришельцами."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            self.score_count += 100 * self.fleet_count
            alien_blast = pygame.mixer.Sound(f'sounds/exp{choice(range(3))}.mp3')
            alien_blast.set_volume(0.7)
            alien_blast.play()

            # Создает новый флот при уничтожении предыдущего
            if not self.aliens.sprites():
                self.bullets.empty()
                sleep(0.3)
                self._create_fleet()
                self.bullets.empty()
                self.settings.alien_speed += self.settings.alien_acceleration
                self.fleet_count += 1

        if self.aliens.lostsprites:
            self.exp_rect.x = self.aliens.lostsprites[0][0]
            self.exp_rect.y = self.aliens.lostsprites[0][1]
        else:
            self.exp_rect.x = 1300
            self.exp_rect.y = 1300


    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            if int(self.high) < self.score_count:
                with open('High_score.txt', 'w+') as f:
                    f.write(f'{self.score_count}')
            sys.exit()
        elif event.key == pygame.K_EQUALS:
            pygame.mixer.music.set_volume((pygame.mixer.music.get_volume() + 0.1))
        elif event.key == pygame.K_MINUS:
            pygame.mixer.music.set_volume((pygame.mixer.music.get_volume() - 0.1))
        elif event.key == pygame.K_q:
            pygame.mixer.music.load(f'music/{str(choice(range(4)))}.mp3')
            pygame.mixer.music.play(10)
        elif event.key == pygame.K_SPACE and self.stats.game_active == False:
            self.stats.game_active = True
        elif event.key == pygame.K_r and self.stats.ship_left == 0:
            if int(self.high) < self.score_count:
                with open('High_score.txt', 'w+') as f:
                    f.write(f'{self.score_count}')
            self.reset()

    def score(self):
        text_surface = self.settings.my_font.render(
            f'SCORE {"0"*(8-len(str(self.score_count)))}{self.score_count}', True, (200, 200, 200))
        self.screen.blit(text_surface, (950, 10))
        level = self.settings.my_font.render(f'{self.fleet_count}', True, (200, 200, 200))
        self.screen.blit(level, (1150, 35))
        hs_surface = self.settings.my_font.render(f'{self.high}', True, (200, 200, 200))
        self.screen.blit(hs_surface, (600, 10))

    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (4*alien_width)
        number_aliens_x = int(available_space_x//(2*alien_width))-3

        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             1.1 * alien_height - ship_height)
        number_rows = available_space_y//(2 * alien_height)-1

        # Создание первого ряда пришельцев.
        for row_number in range(int(number_rows)):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 3 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.blit(self.settings.bg, self.settings.bg_rect)
        if self.stats.ship_left != 0:
            self.score()
        if self.exp_rect.x and self.exp_rect.y:
            self.screen.blit(self.exp, (self.exp_rect.x, self.exp_rect.y))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullets()
        self.aliens.draw(self.screen)
        self.ships.draw(self.screen)
        if not self.stats.game_active and self.stats.ship_left != 0:
            self.play_button.draw_button()
        if self.stats.ship_left == 0:
            self.game_over()


        pygame.display.flip()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        if self.stats.ship_left > 0:
            # Уменьшение ships_left.
            self.stats.ship_left -= 1
            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()
            ship_dead = pygame.mixer.Sound(f'sounds/ship_dead.mp3')
            ship_dead.play()
            # Пауза
            sleep(0.5)
            self.lives_left()
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom-50:
            # Происходит то же, что при столкновении с кораблем.
                self._ship_hit()
                break

    def reset(self):
        self.__init__()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(75)


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
