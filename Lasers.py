import pygame
import random
import schedule

from ImageLoader import load_image
from BulletLaser import BulletLaser
from ExplosionParticles import Explosion

"""
Enemy - laser. Shoots at 3-4 seconds, damage 20 hp, self hp = 60
"""


class Lasers(pygame.sprite.Sprite):
    d_x = ['Right', 'Left']
    d_y = ['UP', 'Down']

    def __init__(self, game, all_sprites):
        super().__init__(all_sprites)
        self.game = game
        self.all_sprites = all_sprites
        self.d_x = self.d_x[random.randint(0, 1)]
        self.d_y = self.d_y[random.randint(0, 1)]
        self.shoot_delay = random.randint(3, 4)
        self.alien_id = random.randint(0, 100)
        self.laser = None
        self.laser_life_time = 2
        self.init_laser()

    def init_laser(self):
        schedule.every(self.shoot_delay).seconds.do(self.shoot).tag(f'shoot {self.alien_id}')
        self.laser_speed = 2

        # создание спрайта персонажа
        self.image = load_image('Laser.png', (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.rect = pygame.Rect(random.randint(0, self.game.width - 80),
                                random.randint(0, int(self.game.height / 2)), 100, 90)

        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

        self.hp = 60

    def update(self, *args):
        self.pos = [self.pos_x, self.pos_y]
        schedule.run_pending()
        if self.d_x == 'Right':
            self.pos_x += self.laser_speed
        elif self.d_x == 'Left':
            self.pos_x -= self.laser_speed

        if self.pos_x <= 0:
            self.pos_x = 0
            self.d_x = 'Right'
        elif self.pos_x >= self.game.width - 80:
            self.pos_x = self.game.width - 80
            self.d_x = 'Left'

        if self.d_y == 'Up':
            self.pos_y += int(self.laser_speed / 2)
        elif self.d_y == 'Down':
            self.pos_y -= int(self.laser_speed / 2)

        if self.pos_y <= 0:
            self.pos_y = 0
            self.d_y = 'Up'
        elif self.pos_y >= int(self.game.height / 3):
            self.pos_y = int(self.game.height / 3)
            self.d_y = 'Down'

        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        if self.hp <= 0:
            del self.game.lasers[self.game.lasers.index(self)]
            if self.laser:
                try:
                    self.laser.sound.stop()
                except AttributeError:
                    pass
                self.laser.kill()
            schedule.clear(f'shoot {self.alien_id}')
            schedule.clear(f'laser {self.alien_id}')
            self.game.explosion_group.add(Explosion(self.rect.x, self.rect.y, 2))
            self.kill()

    def shoot(self):
        schedule.clear(f'shoot {self.alien_id}')
        laser = BulletLaser(self, self.pos[0], self.pos[1], self.all_sprites)
        self.game.bullets.append(laser)
        self.laser = laser
        schedule.every(self.laser_life_time).seconds.do(self.kill_laser).tag(f'laser {self.alien_id}')

    def kill_laser(self):
        for bullet in self.game.bullets:
            if type(bullet) == BulletLaser:
                try:
                    bullet.sound.stop()
                except AttributeError:
                    pass
                bullet.kill()
                schedule.clear(f'laser {self.alien_id}')
                del self.game.bullets[self.game.bullets.index(bullet)]
                self.laser = None
        schedule.every(self.shoot_delay).seconds.do(self.shoot).tag(f'shoot {self.alien_id}')

    def do_damage(self, damage):
        self.hp -= damage
