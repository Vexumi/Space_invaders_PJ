import pygame
from ImageLoader import load_image
import random


class AbilityLuckyBlock(pygame.sprite.Sprite):
    def __init__(self, game, all_sprites):
        super().__init__(all_sprites)
        pygame.font.init()
        self.game = game
        self.speed = 1
        self.size = 30

        self.radius = 20
        self.image = load_image('AbilityLuckyBlock.png', (0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = pygame.Rect(random.randint(self.size, self.game.width - self.size),
                                random.randint(0, int(self.game.height / 4)), self.size, self.size)
        self.font = pygame.font.SysFont('Arial', 30)

        self.power = random.choice([-20, -10, -15, 0, 10, 20, 30, 40])

    def draw(self):
        pygame.draw.circle(self.image, pygame.Color("green"), (self.radius, self.radius),
                           self.radius)

    def update(self, event):
        self.rect.y += self.speed

    def check_collision(self, target):
        if pygame.sprite.spritecollideany(self, target):
            if self.power >= 0:
                if self.power + self.game.hero.hp_hero < self.game.hero.hp_hero_max:
                    self.game.hero.hp_hero += self.power
                else:
                    self.game.hero.hp_hero = self.game.hero.hp_hero_max
            else:
                self.game.hero.do_damage(-self.power)
            self.kill()
            return pygame.sprite.spritecollideany(self, target)
        return False
