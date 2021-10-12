import pygame
from ImageLoader import load_image
import random


class AbilityViewHP(pygame.sprite.Sprite):
    def __init__(self, game, all_sprites):
        super().__init__(all_sprites)
        pygame.font.init()
        self.game = game
        self.speed = 1
        self.size = 30

        self.radius = 20
        self.image = load_image('AbilityViewHP.jpg', (0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = pygame.Rect(random.randint(self.size, self.game.width - self.size),
                                random.randint(0, int(self.game.height / 4)), self.size, self.size)
        self.claimed = False
        self.font = pygame.font.SysFont('Arial', 30)

    def draw(self):
        pygame.draw.circle(self.image, pygame.Color("green"), (self.radius, self.radius),
                           self.radius)

    def update(self, event):
        if not self.claimed:
            self.rect.y += self.speed
        else:
            for enemy in self.game.aliens + self.game.lasers + self.game.ints:
                text_pos = (enemy.rect.x + 30, enemy.rect.y + 80)
                if 70 <= enemy.hp:
                    textsurface = self.font.render(str(enemy.hp), False, (0, 255, 0))
                elif 30 <= enemy.hp <= 60:
                    textsurface = self.font.render(str(enemy.hp), False, (255, 165, 0))
                else:
                    textsurface = self.font.render(str(enemy.hp), False, (255, 0, 0))

                if enemy.hp >= 100:
                    text_pos = (enemy.rect.x + 20, enemy.rect.y + 80)
                self.game.screen.blit(textsurface, text_pos)

    def check_collision(self, target):
        if pygame.sprite.spritecollideany(self, target) and not self.claimed:
            self.claimed = True
            self.image = self.image.convert_alpha()
            self.image.set_alpha(0)
        return False
