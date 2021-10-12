import pygame
import random
import schedule

from ImageLoader import load_image
from BulletLaser import BulletLaser
from ExplosionParticles import Explosion


"""
FirstBoss
"""


class WhiteDeath(pygame.sprite.Sprite): #TODO Boss WhiteDeath

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

    def init_boss(self):
        self.laser_speed = 2

        # создание спрайта персонажа
        self.image = load_image('WhiteDeath.png', (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.rect = pygame.Rect(random.randint(0, self.game.width - 80),
                                random.randint(0, int(self.game.height / 2)), 100, 90)

        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

        self.hp = 60

    def update(self, *args):
        pass

    def do_damage(self, damage):
        self.hp -= damage
