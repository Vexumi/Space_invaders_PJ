import pygame
import json
import sys

from Aliens import Aliens
from BulletEnemy import BulletEnemy
from Hero import Hero
from Bullet import Bullet
from SpawnLevelEntities import Spawner
from Lasers import Lasers
from FirstRoundInstructions import give_instructions
from HeroShoot import Shoot
from BackgroundStars import BackgroundStars

"""
This file contains main cycle
"""


class MainGame:
    def __init__(self, screen_size, difficulty, music_on):
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.difficulty = difficulty
        self.music_on = music_on
        self.all_sprites = pygame.sprite.Group()
        self.wave_count = 0
        self.bullets = []
        self.aliens = []
        self.abilities = []
        self.shotgun_fire_count = 0
        self.shotgun_fire_max = 5
        self.explosion_group = pygame.sprite.Group()
        self.n_aliens = 1
        self.wait_new_wave = False
        self.init_game()
        self.run()

    def init_game(self):
        with open('waves.json', mode='r') as json_file:
            self.waves = json.load(json_file)
            json_file.close()

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(pygame.Color('black'))

        if self.difficulty == 'Low':
            self.hp = 200
        elif self.difficulty == 'Normal':
            self.hp = 100
        elif self.difficulty == 'Hard':
            self.hp = 20
        elif self.difficulty == 'God of gamers':
            self.hp = 1

        self.hero = Hero(self, self.hp, self.all_sprites, self.screen.get_size())

        wave = self.waves[f'Wave {str(self.wave_count)}']
        spawned = Spawner(self, wave)
        self.aliens = spawned[0]
        self.lasers = spawned[1]

    def run(self):
        self.running = True
        self.speed = 2.3
        self.fps = 60
        self.clock = pygame.time.Clock()
        bg = BackgroundStars(self, 400)

        while self.running:
            # self.screen.fill((0, 0, 0))
            bg.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit(-1)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    Shoot(self)
                eventt = event

            self.delete_bullet()
            self.damage_test()
            self.ability_test()
            self.enemies_left()
            self.update_sprites(eventt)
            self.display_hero_stats()
            self.all_sprites.draw(self.screen)
            self.explosion_group.draw(self.screen)
            self.explosion_group.update()
            self.clock.tick(int(self.fps * self.speed))
            pygame.display.flip()
        # pygame.quit()

    def delete_bullet(self):
        for bullet in self.bullets:
            if bullet.rect.y <= 0 or bullet.rect.y >= self.height:
                bullet.kill()
                del self.bullets[self.bullets.index(bullet)]

    def ability_test(self):
        for ability in self.abilities:
            if ability.check_collision(pygame.sprite.Group(self.hero)):
                del self.abilities[self.abilities.index(ability)]
                ability.kill()

    def damage_test(self):
        for n, bullet in enumerate(self.bullets):
            if bullet.check_collision(self.aliens):
                if type(bullet) == Bullet:
                    self.aliens[self.aliens.index(bullet.check_collision(self.aliens))].do_damage(self.hero.damage)
                    del self.bullets[self.bullets.index(bullet)]
                    bullet.kill()

            if bullet.check_collision(self.lasers):
                if type(bullet) == Bullet:
                    self.lasers[self.lasers.index(bullet.check_collision(self.lasers))].do_damage(self.hero.damage)
                    try:
                        del self.bullets[self.bullets.index(bullet)]
                    except ValueError:
                        print('Bullet ValueError')
                    bullet.kill()

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

    def enemies_left(self):
        if len(self.aliens) + len(self.lasers) == 0:
            if not self.wait_new_wave:
                self.wait_new_wave = True
            else:
                if self.hero.pos_y <= -50:
                    self.hero.pos_x = self.width / 2
                    self.hero.pos_y = self.height - self.height / 4
                    self.hero.rect.x = self.width / 2
                    self.hero.rect.y = self.height - self.height / 4
                    for ability in self.abilities:
                        ability.kill()
                    self.wave_count += 1
                    try:
                        wave = self.waves[f'Wave {str(self.wave_count)}']
                        spawned = Spawner(self, wave)
                        self.aliens = spawned[0]
                        self.lasers = spawned[1]
                    except KeyError:
                        self.running = False
                    self.hero.invisible_wall = True
                elif self.wave_count == 0:  # if first round give instructions
                    give_instructions(self)
                    self.draw_arrow_up()
                    self.hero.invisible_wall = False

                else:
                    font = pygame.font.Font(None, 60)
                    text = f'WAVE {str(self.wave_count + 1)}'
                    text_pos = (self.width / 2 - 80, self.height / 4 - 50)
                    self.screen.blit(font.render(text, False, (255, 255, 255)), text_pos)
                    self.draw_arrow_up()
                    self.hero.invisible_wall = False

    def draw_arrow_up(self):
        arrow_thin = 3

        # arrow up head
        arrow_head_pts = [[self.width / 2, self.height / 16],
                          [self.width / 2 + 20, self.height / 16 + 20],
                          [self.width / 2 - 20, self.height / 16 + 20]]
        pygame.draw.polygon(self.screen, 'white', arrow_head_pts, arrow_thin)

        # arrow up body
        arrow_body_pts = [self.width / 2 - 8, self.height / 16 + 20, 18, 50]
        pygame.draw.rect(self.screen, 'white', arrow_body_pts, arrow_thin)
