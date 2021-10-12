import pygame
from Heroes.Atlas import Atlas
from Heroes.Nova import Nova
from Heroes.EnergyShield import Shield
# from Heroes.LighterS import Lighter

"""
Type of bullets for Enemy-Laser
"""


class BulletLaser(pygame.sprite.Sprite):
    def __init__(self, game, x, y, all_sprites):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.game = game
        self.bullet_speed = 7
        self.damage = 20
        self.laser_thin = 5
        self.laser_thin_delta = 1
        self.iter_anim = 0
        self.radius = 10
        self.laser_long = 400

        if self.game.game.music_on:
            self.sound = pygame.mixer.Sound('sounds/LaserSound.mp3').play()

        self.image = pygame.Surface((20, self.laser_long), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(self.x, self.y, 20, self.laser_long)

    def draw(self):
        pygame.draw.line(self.image, 'red', (10, 0), (10, self.y + self.laser_long), self.laser_thin)
        self.rect.x = self.game.rect.x + 13
        self.rect.y = self.game.rect.y + 75

    def update(self, event):
        self.draw()
        if self.iter_anim == 5:
            self.laser_thin += self.laser_thin_delta
            if self.laser_thin <= 5:
                self.laser_thin_delta = 1
            elif self.laser_thin >= 20:
                self.laser_thin_delta = -1
            self.iter_anim = 0

        self.iter_anim += 1

    def check_collision(self, target):
        if pygame.sprite.spritecollide(self, target, False):
            if type(pygame.sprite.spritecollide(self, target, False)[0]) == type(Atlas) or \
                    type(pygame.sprite.spritecollide(self, target, False)[0]) == type(Nova) or \
                    type(pygame.sprite.spritecollide(self, target, False)[0]) == type(Shield):
                if self.game.game.music_on:
                    self.sound.stop()
                self.kill()
                del self.game.game.bullets[self.game.game.bullets.index(self)]
                return pygame.sprite.spritecollideany(self, target)
        return False
