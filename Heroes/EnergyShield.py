import pygame
from ImageLoader import load_image
import random


class Shield(pygame.sprite.Sprite):
    def __init__(self, game, sprite_group):
        super().__init__(game.game.all_sprites)
        self.game = game
        self.speed = 1
        self.size = 110

        self.radius = 20
        self.image = load_image('EnergyShield.png', (0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = pygame.Rect(random.randint(self.size, self.game.game.width - self.size),
                                random.randint(0, int(self.game.game.height / 4)), self.size, self.size)

    def draw(self):
        pygame.draw.circle(self.image, pygame.Color("green"), (self.radius, self.radius),
                           self.radius)

    def update(self, event):
        self.rect.x = self.game.rect.x - 15
        self.rect.y = self.game.rect.y - 15

        bullet_collided = pygame.sprite.spritecollideany(self, self.game.game.bullets)
        if bullet_collided:
            bullet_collided.kill()

