# загрузка библиотек
import pygame
import os
import sys
import random

# инициализация Pygame
pygame.init()
pygame.display.set_caption('Space Invaders')


# создание картинки для спрайтов
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# главный класс игры
class MainGame:
    def __init__(self, width, height, dificulty):
        self.width = width
        self.height = height
        self.dificulty = dificulty
        self.all_sprites = pygame.sprite.Group()
        self.bullets = []
        self.init_game()
        self.run()

    def init_game(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(pygame.Color('black'))

        if self.dificulty == 'Low':
            self.hp = 1000
        elif self.dificulty == 'Normal':
            self.hp = 100
        elif self.dificulty == 'Hard':
            self.hp = 20
        elif self.dificulty == 'God of gamers':
            self.hp = 1

        self.hero = Hero(self, self.hp, self.all_sprites, self.screen.get_size())
        self.alien = Aliens(self, self.all_sprites)

    def run(self):
        self.running = True
        self.speed = 2.3
        self.fps = 60
        self.clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.bullets.append(
                            Bullet(self, self.hero.rect.x + 35,
                                   self.hero.rect.y, self.all_sprites))
                eventt = event
            self.delete_bullet()
            self.update_sprites(eventt)
            self.screen.fill((0, 0, 0))
            self.display_hero_stats()
            self.all_sprites.draw(self.screen)
            self.clock.tick(int(self.fps * self.speed))
            pygame.display.flip()
        pygame.quit()

    def delete_bullet(self):
        for bullet in self.bullets:
            if bullet.rect.y <= 0:
                bullet.kill()
                del self.bullets[self.bullets.index(bullet)]

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(textsurface, (110, 160))

    def display_hero_stats(self):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 30)
        textsurface = font.render('HP: ' + str(self.hero.hp_hero), False, (0, 255, 0))
        self.screen.blit(textsurface, (self.width - 100, self.height - 50))

    def update_sprites(self, event):
        for i in self.all_sprites:
            i.update(event)
        self.hero.check_collision()

    # класс героя


class Hero(pygame.sprite.Sprite):
    def __init__(self, game, hp, all_sprites, sc_size):
        super().__init__(all_sprites)
        self.hp_hero = hp
        self.game = game
        self.all_sprites = all_sprites
        self.diraction = None
        self.screen_size = sc_size
        self.init_hero()

    # инициализация героя
    def init_hero(self):
        self.hero_speed = 4

        # создание спрайта персонажа, как точку
        self.image = load_image('hero.png', (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = pygame.Rect(int(self.game.width / 2), self.game.height - 50, 100, 90)

        self.pos_x = int(self.game.width / 2)
        self.pos_y = self.game.height - 50

    # движение, стрельба героя и т.д
    def update(self, event):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN]:
            self.pos_y += self.hero_speed
            self.rect.y = self.pos_y
        if pressed[pygame.K_UP]:
            self.pos_y -= self.hero_speed
            self.rect.y = self.pos_y
        if pressed[pygame.K_LEFT]:
            self.pos_x -= self.hero_speed
            self.rect.x = self.pos_x
            if self.diraction == None:
                self.diraction = 'Left'
            elif self.diraction == 'Right':
                self.diraction = None
        if pressed[pygame.K_RIGHT]:
            self.pos_x += self.hero_speed
            self.rect.x = self.pos_x
            if self.diraction == None:
                self.diraction = 'Right'
            elif self.diraction == 'Left':
                self.diraction = None
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or \
                    event.key == pygame.K_LEFT or \
                    event.key == pygame.K_UP or \
                    event.key == pygame.K_DOWN:
                self.diraction = None

        self.change_image()
        self.check_collision()

    def change_image(self):
        if self.diraction == None:
            self.image = load_image('hero.png', (255, 255, 255))
            self.image = pygame.transform.scale(self.image, (80, 80))
        elif self.diraction == 'Left':
            self.image = load_image('hero_left.png', (255, 255, 255))
            self.image = pygame.transform.scale(self.image, (80, 80))
        elif self.diraction == 'Right':
            self.image = load_image('hero_right.png', (255, 255, 255))
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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, all_sprites):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.game = game
        self.bullet_speed = 7

        self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)

    def draw(self):
        pygame.draw.circle(self.image, pygame.Color("red"), (self.radius, self.radius),
                           self.radius)
        self.rect.y -= self.bullet_speed

    def update(self, event):
        self.draw()


class Aliens(pygame.sprite.Sprite):
    type_of_aliens = ['S', 'M', 'L']

    def __init__(self, game, all_sprites):
        super().__init__(all_sprites)
        self.game = game
        self.all_sprites = all_sprites
        self.d_x = 'Right'
        self.d_y = 'UP'
        self.type_of_alien = self.type_of_aliens[random.randint(0, 2)]

        self.type_of_alien = 'M'

        self.init_alien()

    def init_alien(self):
        self.alien_speed = 2

        # создание спрайта персонажа, как точку
        self.image = load_image('alien_1.png', (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = pygame.Rect(int(self.game.width / 2), 0, 100, 90)

        self.pos_x = int(self.game.width / 2)
        self.pos_y = 0

    def update(self, *args):
        if self.type_of_alien == 'S':
            if self.d_x == 'Right':
                self.pos_x += self.alien_speed
            elif self.d_x == 'Left':
                self.pos_x -= self.alien_speed

            if self.pos_x <= 0:
                self.pos_x = 0
                self.d_x = 'Right'
            elif self.pos_x >= self.game.width - 80:
                self.pos_x = self.game.width - 80
                self.d_x = 'Left'
            self.rect.x = self.pos_x

        elif self.type_of_alien == 'M':
            if self.d_x == 'Right':
                self.pos_x += self.alien_speed
            elif self.d_x == 'Left':
                self.pos_x -= self.alien_speed

            if self.pos_x <= 0:
                self.pos_x = 0
                self.d_x = 'Right'
            elif self.pos_x >= self.game.width - 80:
                self.pos_x = self.game.width - 80
                self.d_x = 'Left'

            if self.d_y == 'Up':
                self.pos_y += int(self.alien_speed / 2)
            elif self.d_y == 'Down':
                self.pos_y -= int(self.alien_speed / 2)

            if self.pos_y <= 0:
                self.pos_y = 0
                self.d_y = 'Up'
            elif self.pos_y >= int(self.game.height / 3):
                self.pos_y = int(self.game.height / 3)
                self.d_y = 'Down'

            self.rect.x = self.pos_x
            self.rect.y = self.pos_y


# создание игры
if __name__ == '__main__':
    game = MainGame(550, 700, 'Normal')
