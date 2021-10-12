import pygame


class BulletEnemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, all_sprites, damage=10):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.game = game
        self.bullet_speed = 7
        self.damage = damage

        if self.game.game.music_on:
            pygame.mixer.Sound('sounds/EnemyBulletSound.mp3').play()

        self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)

    def draw(self):
        pygame.draw.circle(self.image, pygame.Color("red"), (self.radius, self.radius),
                           self.radius)

    def update(self, event):
        self.draw()
        self.rect.y += self.bullet_speed

    def check_collision(self, target):
        if pygame.sprite.spritecollide(self, target, False):
            if type(pygame.sprite.spritecollide(self, target, False)[0]) != type(self.game):
                self.kill()
                del self.game.game.bullets[self.game.game.bullets.index(self)]
                return pygame.sprite.spritecollideany(self, target)
        return False
