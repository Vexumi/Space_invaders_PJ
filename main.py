import pygame
import random
import json
import sys

from Bullet import Bullet

from SpawnLevelEntities import Spawner
from HeroShoot import Shoot

from FirstRoundInstructions import give_instructions
from BackgroundStars import BackgroundStars
from Outro import OutroWin

from Heroes.Atlas import Atlas
from Heroes.Nova import Nova
from Heroes.LighterS import LighterS

"""
This file contains main cycle
"""


class MainGame:
    def __init__(self, screen_size, difficulty, music_on, ship):
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.difficulty = difficulty
        self.music_on = music_on
        self.ship = ship

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
        self.music = random.choice(['InGame 1.mp3', 'InGame 2.mp3', 'InGame 3.mp3', 'InGame 4.mp3', ])
        if self.music_on:
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.load('sounds/' + self.music)
            pygame.mixer.music.play()

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
        elif self.difficulty == 'God Of Gamers':
            self.hp = 1

        # ---
        self.hero = eval(f'{self.ship}(self, self.hp, self.all_sprites, self.screen.get_size())')
        # ---

        wave = self.waves[f'Wave {str(self.wave_count)}']
        spawned = Spawner(self, wave)
        self.aliens = spawned[0]
        self.lasers = spawned[1]
        self.ints = spawned[2]

    def run(self):
        self.running = True
        self.speed = 2
        self.fps = 60
        self.clock = pygame.time.Clock()
        bg = BackgroundStars(self, 300, (1, 2))

        while self.running:
            self.delete_ghosted_bullets()

            bg.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit(-1)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    bullet_count = 0
                    for b in self.bullets:
                        if type(b) == Bullet:
                            bullet_count += 1

                    if bullet_count < 3:
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

            if bullet.check_collision(self.ints):
                if type(bullet) == Bullet:
                    self.ints[self.ints.index(bullet.check_collision(self.ints))].do_damage(self.hero.damage)
                    del self.bullets[self.bullets.index(bullet)]
                    bullet.kill()

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(textsurface, (110, 160))

    def delete_ghosted_bullets(self):  # fix delete ghost-bullet
        for b in self.bullets:
            if len(b.groups()) == 0:
                b.kill()

    def display_hero_stats(self):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 30)
        text_pos = (self.hero.rect.x + 30, self.hero.rect.y + 80)
        if 70 <= self.hero.hp_hero:
            textsurface = font.render(str(self.hero.hp_hero), False, (0, 255, 0))
        elif 30 <= self.hero.hp_hero <= 60:
            textsurface = font.render(str(self.hero.hp_hero), False, (255, 165, 0))
        else:
            textsurface = font.render(str(self.hero.hp_hero), False, (255, 0, 0))

        if self.hero.hp_hero >= 100:
            text_pos = (self.hero.rect.x + 20, self.hero.rect.y + 80)

        self.screen.blit(textsurface, text_pos)

    def update_sprites(self, event):
        for i in self.all_sprites:
            i.update(event)
        self.hero.check_collision()

    def enemies_left(self):
        if len(self.aliens) + len(self.lasers) + len(self.ints) == 0:
            if not self.wait_new_wave:
                self.wait_new_wave = True
            else:
                if self.hero.pos_y <= -50:  # go to next level
                    self.hero.pos_x = self.width / 2
                    self.hero.pos_y = self.height - self.height / 4
                    self.hero.rect.x = self.width / 2
                    self.hero.rect.y = self.height - self.height / 4

                    for ability in self.abilities:
                        ability.kill()
                    self.abilities.clear()

                    self.wave_count += 1
                    try:
                        wave = self.waves[f'Wave {str(self.wave_count)}']
                        spawned = Spawner(self, wave)
                        self.aliens = spawned[0]
                        self.lasers = spawned[1]
                        self.ints = spawned[2]
                    except KeyError:
                        self.running = False
                        OutroWin((self.width, self.height))

                    self.hero.invisible_wall = True
                elif self.wave_count == 0:  # if first round give instructions
                    give_instructions(self)
                    self.draw_arrow_up()
                    self.hero.invisible_wall = False

                else:
                    font = pygame.font.Font(None, 60)  # draw wave text and arrow
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
