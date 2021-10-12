import pygame

from Bullet import Bullet
from ImageLoader import load_image
from ExplosionParticles import Explosion
from Outro import OutroLose


class LighterS(pygame.sprite.Sprite):
    def __init__(self, game, hp, all_sprites, sc_size):
        super().__init__(all_sprites)
        self.hp_hero = hp
        self.hp_hero_max = hp
        self.game = game
        self.all_sprites = all_sprites
        self.direction = None
        self.abilities_owned = []
        self.screen_size = sc_size
        self.init_hero()
        self.damage = 8
        self.invisible_wall = True
        self.shield_on = None

    # инициализация героя
    def init_hero(self):
        self.hero_speed = 6

        self.image = load_image('Lighter-S.png', (255, 255, 255))

        # создание спрайта персонажа, как точку
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = pygame.Rect(int(self.game.width / 2), self.game.height - 50, 100, 90)

        self.pos_x = int(self.game.width / 2)
        self.pos_y = self.game.height - 50

    # движение, стрельба героя и т.д
    def update(self, event):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.pos_y += self.hero_speed
            self.rect.y = self.pos_y
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            if self.invisible_wall:
                if self.rect.y >= self.screen_size[1] // 2:
                    self.pos_y -= self.hero_speed
                    self.rect.y = self.pos_y
            else:
                self.pos_y -= self.hero_speed
                self.rect.y = self.pos_y
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.pos_x -= self.hero_speed
            self.rect.x = self.pos_x
            self.direction = 'Left'

        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.pos_x += self.hero_speed
            self.rect.x = self.pos_x
            self.direction = 'Right'

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT \
                    or event.key == pygame.K_a or event.key == pygame.K_d:
                if not pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
                    self.direction = None
                elif pressed[pygame.K_RIGHT] and pressed[pygame.K_LEFT]:
                    self.direction = None

        self.change_image()
        self.check_collision()

    def change_image(self):
        if not self.direction:
            self.image = load_image('Lighter-S.png', (255, 255, 255))
            self.image = pygame.transform.scale(self.image, (80, 80))
        elif self.direction == 'Left':
            self.image = load_image('Lighter-S_left.png', (255, 255, 255))
            self.image = pygame.transform.scale(self.image, (80, 80))
        elif self.direction == 'Right':
            self.image = load_image('Lighter-S_right.png', (255, 255, 255))
            self.image = pygame.transform.scale(self.image, (80, 80))

    def check_collision(self):
        if self.rect.x <= 0:
            self.rect.x = 0
            self.pos_x = 0
        elif self.rect.x >= self.screen_size[0] - 80:
            self.rect.x = self.screen_size[0] - 80
            self.pos_x = self.screen_size[0] - 80

        if self.rect.y >= self.screen_size[1] - 80:
            self.rect.y = self.screen_size[1] - 80
            self.pos_y = self.screen_size[1] - 80

        bullet_collided = pygame.sprite.spritecollideany(self, self.game.bullets)
        if bullet_collided:
            if type(bullet_collided) != Bullet:
                self.do_damage(bullet_collided.damage)
                try:
                    bullet_collided.sound.stop()
                except AttributeError:
                    pass
                bullet_collided.kill()
                del self.game.bullets[self.game.bullets.index(bullet_collided)]

    def do_damage(self, damage):
        self.hp_hero -= damage
        self.game.explosion_group.add(Explosion(self.rect.x + 35, self.rect.y, 2))

        if self.game.music_on:
            pygame.mixer.Sound('sounds/ExploseSound.mp3').play()

        if self.hp_hero <= 0:
            # del self.game.hero[self.game.hero.index(self)]
            self.kill()
            OutroLose(self.screen_size)
            self.game.running = False
