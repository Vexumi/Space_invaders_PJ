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

        self.hero = Hero(self, self.hp, self.all_sprites)

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
            self.all_sprites.draw(self.screen)
            self.clock.tick(int(self.fps * self.speed))
            pygame.display.flip()
        pygame.quit()

    def delete_bullet(self):
        for bullet in self.bullets:
            if bullet.rect.y <= 0:
                del self.bullets[self.bullets.index(bullet)]

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(textsurface, (110, 160))

    def update_sprites(self, event):
        for i in self.all_sprites:
            i.update(event)

    # класс героя


class Hero(pygame.sprite.Sprite):
    def __init__(self, game, hp, all_sprites):
        super().__init__(all_sprites)
        self.hp_hero = hp
        self.game = game
        self.all_sprites = all_sprites
        self.diraction = None
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

    ### in developing
    def check_collision(self):
        pass


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


# создание игры
if __name__ == '__main__':
    game = MainGame(500, 700, 'Normal')
