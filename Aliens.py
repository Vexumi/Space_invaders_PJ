import pygame
import random
import schedule
from BulletEnemy import BulletEnemy
from ImageLoader import load_image
from ExplosionParticles import Explosion

"""
Type of Enemy - Alien, damage 10, self hp = 30-150
"""


class Aliens(pygame.sprite.Sprite):
    type_of_aliens = ['S', 'M', 'L']
    d_x = ['Right', 'Left']
    d_y = ['UP', 'Down']

    def __init__(self, game, all_sprites):
        super().__init__(all_sprites)
        self.game = game
        self.all_sprites = all_sprites
        self.d_x = self.d_x[random.randint(0, 1)]
        self.d_y = self.d_y[random.randint(0, 1)]
        self.shoot_delay = random.randint(1, 3)
        self.type_of_alien = self.type_of_aliens[random.randint(0, 1)]
        self.alien_id = random.randint(1, 100)

        # self.type_of_alien = 'M'

        self.init_alien()

    def init_alien(self):
        schedule.every(self.shoot_delay).seconds.do(self.shoot).tag(f'shoot {self.alien_id}')
        self.alien_speed = random.randint(1, 2)

        # создание спрайта персонажа
        self.image = load_image('alien_1.png', (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = pygame.Rect(random.randint(0, self.game.width - 80),
                                random.randint(0, int(self.game.height / 2)), 100, 90)

        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

        if self.type_of_alien == 'S':
            self.hp = 30
        elif self.type_of_alien == 'M':
            self.hp = 50
        else:
            self.hp = 150

    def update(self, *args):
        self.pos = [self.pos_x, self.pos_y]
        schedule.run_pending()
        if self.type_of_alien == 'S':
            if self.d_x == 'Right':
                self.pos_x += self.alien_speed
            elif self.d_x == 'Left':
                self.pos_x -= self.alien_speed

            if self.pos_x <= 0:
                self.pos_x = 0
                self.d_x = 'Right'
            elif self.pos_x >= self.game.width - 80:
                self.pos_x = self.game.width - 80
                self.d_x = 'Left'
            self.rect.x = self.pos_x

        elif self.type_of_alien == 'M':
            if self.d_x == 'Right':
                self.pos_x += self.alien_speed
            elif self.d_x == 'Left':
                self.pos_x -= self.alien_speed

            if self.pos_x <= 0:
                self.pos_x = 0
                self.d_x = 'Right'
            elif self.pos_x >= self.game.width - 80:
                self.pos_x = self.game.width - 80
                self.d_x = 'Left'

            if self.d_y == 'Up':
                self.pos_y += int(self.alien_speed / 2)
            elif self.d_y == 'Down':
                self.pos_y -= int(self.alien_speed / 2)

            if self.pos_y <= 0:
                self.pos_y = 0
                self.d_y = 'Up'
            elif self.pos_y >= int(self.game.height / 3):
                self.pos_y = int(self.game.height / 3)
                self.d_y = 'Down'

            self.rect.x = self.pos_x
            self.rect.y = self.pos_y

        if self.hp <= 0:
            del self.game.aliens[self.game.aliens.index(self)]
            schedule.clear(f'shoot {self.alien_id}')
            self.game.explosion_group.add(Explosion(self.rect.x, self.rect.y, 2))
            self.kill()

    def shoot(self):
        self.game.bullets.append(BulletEnemy(self, self.pos[0] + 40, self.pos[1] + 70, self.all_sprites))

    def do_damage(self, damage):
        self.hp -= damage
