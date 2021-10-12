import pygame
from ImageLoader import load_image
import random


class AbilityShotgun(pygame.sprite.Sprite):
    def __init__(self, game, all_sprites):
        super().__init__(all_sprites)
        self.game = game
        self.speed = 1
        self.size = 30
        self.time = 30  # sec

        self.radius = 20
        self.image = load_image('AbilityShotgun.jpg', (0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = pygame.Rect(random.randint(self.size, self.game.width - self.size),
                                random.randint(0, int(self.game.height / 4)), self.size, self.size)

    def draw(self):
        pygame.draw.circle(self.image, pygame.Color("green"), (self.radius, self.radius),
                           self.radius)

    def update(self, event):
        self.rect.y += self.speed

    def check_collision(self, target):
        if pygame.sprite.spritecollideany(self, target):
            self.kill()
            self.game.hero.abilities_owned.append('Shotgun')
            return pygame.sprite.spritecollideany(self, target)
        return False
