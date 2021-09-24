import pygame
from ImageLoader import load_image

"""
Particles for explose of bullets or enemy death
"""


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, type_exp):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        if type_exp == 1:
            self.size = 50
            for num in range(1, 6):
                img = pygame.image.load(f"sprites/ExplosionAnim/Explosion{num}.png")
                img = pygame.transform.scale(img, (self.size, self.size))
                self.images.append(img)

        elif type_exp == 2:
            self.size = 200
            for num in range(1, 8):
                # img = pygame.image.load(f"sprites/Explosion2Anim/Explosion{num}.png")
                img = load_image(f'Explosion2Anim/Explosion{num}.png', (0, 0, 0))
                img = pygame.transform.scale(img, (self.size, self.size))
                self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
