import pygame
import random
from ImageLoader import load_image


class Bombs(pygame.sprite.Sprite):

    def __init__(self, game, all_sprites):
        super().__init__(all_sprites)
        self.game = game
        self.all_sprites = all_sprites
        self.init_bomb()

    def init_bomb(self):
        self.image = load_image('Bomb.png', (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = pygame.Rect(random.randint(0, self.game.width - 80),
                                random.randint(0, int(self.game.height / 2)), 100, 90)

    def update(self, *args):

    def do_damage(self, damage):
        print('Booom')
