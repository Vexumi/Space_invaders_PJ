import sys
import json
import pygame
import pygame_gui
from ImageLoader import load_image
from BackgroundStars import BackgroundStars
from main import MainGame
from ImageLoader import load_image
import random


class Logo(pygame.sprite.Sprite):
    def __init__(self, logo_group, pos):
        super().__init__(logo_group)
        self.image = load_image('Logo.png', (0, 0, 0))
        self.image = pygame.transform.scale(self.image, (270, 140))
        self.rect = pygame.Rect(pos[0], pos[1], 270, 140)


class Atlas(pygame.sprite.Sprite):
    def __init__(self, ships_group, pos):
        super().__init__(ships_group)
        self.image = load_image('Atlas.png', (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (200, 180))
        self.rect = pygame.Rect(pos[0], pos[1], 200, 187)

    def get_name(self):
        return 'Atlas'


class Nova(pygame.sprite.Sprite):
    def __init__(self, ships_group, pos):
        super().__init__(ships_group)
        self.image = load_image('Nova.png', (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (200, 180))
        self.rect = pygame.Rect(pos[0], pos[1], 200, 187)

    def get_name(self):
        return 'Nova'


class LighterS(pygame.sprite.Sprite):
    def __init__(self, ships_group, pos):
        super().__init__(ships_group)
        self.image = load_image('Lighter-S.png', (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (200, 180))
        self.rect = pygame.Rect(pos[0], pos[1], 200, 187)

    def get_name(self):
        return 'Lighter-S'


class Menu:
    pygame.mixer.init()

    def __init__(self, screen_size, difficulty, music_on):
        pygame.init()
        pygame.font.init()

        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(self.screen_size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.width, self.height = screen_size
        self.difficulty = difficulty
        self.music_on = music_on
        self.logo_group = pygame.sprite.Group()
        self.ships_group = pygame.sprite.Group()
        self.ships = [Atlas, Nova, LighterS]
        self.now_ship = 0

        self.init_ships()
        self.init_buttons()
        self.run()

    def init_ships(self):
        self.ship_pos = (self.width // 2 - 100, self.height // 2 - 90)
        self.ship_describe = ['-The most common ship for travel in space, has 10 damage',
                              '-Large enough ship with energy shield and 5 damage',
                              '-Small enough, fast and very maneuverable ship']
        self.ship_recommended = ['-Recommended for beginners',
                                 '-Recommended for advanced players',
                                 '-Recommended for advanced players']
        self.ship_names = ['Atlas', 'Nova', 'LighterS']

    def init_buttons(self):
        self.manager = pygame_gui.UIManager(self.screen_size, 'themes/theme.json')

        self.btn_start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3), (250, 50)),
            text='Start', manager=self.manager)
        self.btn_settings = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3 + 80), (250, 50)),
            text='Settings', manager=self.manager)
        self.btn_quit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3 + 160), (250, 50)),
            text='Quit', manager=self.manager, object_id='quit')

        self.dropdownmenu_screen_size = pygame_gui.elements.UIDropDownMenu(
            options_list=['500*500', '600*700', '1920*1080'],
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3 + 20),
                                      (250, 50)), manager=self.manager,
            starting_option='*'.join(map(str, self.screen_size)))

        self.btn_return = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3 + 210),
                                      (250, 50)),
            text='Back To Menu', manager=self.manager)

        if self.music_on:
            starting_option = 'On'
        else:
            starting_option = 'Off'

        self.dropdownmenu_sound = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3 + 120),
                                      (250, 50)), options_list=['On', 'Off'], manager=self.manager,
            starting_option=starting_option)
        self.label_change_screen_size = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.width // 2 - 220 // 2, self.height // 3 - 10),
                                      (220, 30)), text='Screen Size', manager=self.manager)
        self.label_change_music_on = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.width // 2 - 220 // 2, self.height // 3 + 90),
                                      (220, 30)), text='Music and Sound', manager=self.manager)

        self.btn_next = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 35, self.height // 2 - 150), (35, 300)),
            text='>', manager=self.manager)
        self.btn_previous = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.height // 2 - 150), (35, 300)),
            text='<', manager=self.manager)

        self.dropdownmenu_difficulty = pygame_gui.elements.UIDropDownMenu(
            options_list=['Low', 'Normal', 'Hard', 'God Of Gamers'],
            relative_rect=pygame.Rect((self.width - 255, self.height - 55),
                                      (250, 50)), manager=self.manager, starting_option=self.difficulty,
            object_id='drop_down_menu_difficulty')
        self.label_difficulty = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.width - 255 - 100, self.height - 55),
                                      (100, 50)), text='Difficulty:', manager=self.manager)

        self.feature_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.height // 2 - 3 + self.height // 4), (self.width, 25)),
            text='Abilities:',
            manager=self.manager)
        self.feature_describe_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.height // 2 + self.height // 4 + 25), (self.width, 25)),
            text=self.ship_describe[self.now_ship],
            manager=self.manager, parent_element=self.feature_text)
        self.feature_recomendation_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.height // 2 + self.height // 4 + 50), (self.width, 25)),
            text=self.ship_recommended[self.now_ship],
            manager=self.manager, parent_element=self.feature_text)

        self.label_ship_name = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (200, 80)),
            text='',
            manager=self.manager, object_id='label_ship_name')

        self.start_trigger = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 150, self.height // 2 - 150), (300, 300)),
            text='', manager=self.manager, object_id='start_trigger')
        self.go_to_menu = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((5, self.height - 5 - 50), (120, 50)),
            text='Go To Menu', manager=self.manager, object_id='quit')

        self.btn_next.hide()
        self.btn_previous.hide()

        self.start_trigger.hide()

        self.dropdownmenu_screen_size.hide()
        self.dropdownmenu_sound.hide()
        self.dropdownmenu_difficulty.hide()
        self.label_difficulty.hide()
        self.btn_return.hide()
        self.label_change_screen_size.hide()
        self.label_change_music_on.hide()
        self.label_ship_name.hide()
        self.go_to_menu.hide()

        self.feature_text.hide()
        self.feature_describe_text.hide()
        self.feature_recomendation_text.hide()

    def hide_all_btns(self):
        self.go_to_menu.hide()
        self.btn_start.hide()
        self.btn_settings.hide()
        self.btn_quit.hide()
        self.dropdownmenu_screen_size.hide()
        self.dropdownmenu_difficulty.hide()
        self.label_difficulty.hide()
        self.btn_return.hide()
        self.dropdownmenu_sound.hide()
        self.label_ship_name.hide()

    def menu_init(self):
        self.hide_all_btns()

        self.btn_start.show()
        self.btn_settings.show()
        self.btn_quit.show()
        self.draw_logo = True

        self.btn_next.hide()
        self.btn_previous.hide()
        self.feature_text.hide()
        self.dropdownmenu_difficulty.hide()
        self.feature_describe_text.hide()
        self.label_difficulty.hide()
        self.start_trigger.hide()
        self.go_to_menu.hide()
        self.feature_recomendation_text.hide()
        self.label_ship_name.hide()
        self.ship.kill()

    def load_music(self):
        self.music = random.choice(['MainMenu_1.mp3', 'MainMenu_2.mp3'])
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.load('sounds/' + self.music)

        if self.music_on:
            pygame.mixer.music.play()

    def save_settings(self):
        with open('settings.json', mode='w') as json_file:
            new_settings = {"screen_size": self.screen_size,
                            "music_on": self.music_on,
                            "difficulty": 'Normal'}
            new_json = json.dumps(new_settings)
            json_file.write(new_json)

    def run(self):
        self.load_music()

        self.running = True
        self.speed = 2
        self.fps = 30
        self.clock = pygame.time.Clock()
        self.logo = Logo(self.logo_group, (self.width // 2 - 130, self.height // 4 - 80))
        self.draw_logo = True
        bg = BackgroundStars(self, 500, (1, 5))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.btn_start:  # ship choice
                            if self.music_on:
                                pygame.mixer.Sound('sounds/ButtonMenu.mp3').play()

                            self.hide_all_btns()

                            self.draw_logo = False
                            self.btn_next.show()
                            self.btn_previous.show()
                            self.feature_text.show()
                            self.dropdownmenu_difficulty.show()
                            self.feature_describe_text.show()
                            self.label_difficulty.show()
                            self.start_trigger.show()
                            self.feature_recomendation_text.show()
                            self.label_ship_name.show()
                            self.go_to_menu.show()
                            self.ship = self.ships[0](self.ships_group, self.ship_pos)

                        elif event.ui_element == self.btn_settings:  # open settings
                            if self.music_on:
                                pygame.mixer.Sound('sounds/ButtonMenu.mp3').play()

                            self.hide_all_btns()

                            self.dropdownmenu_screen_size.show()
                            self.btn_return.show()
                            self.dropdownmenu_sound.show()
                            self.label_change_screen_size.show()
                            self.label_change_music_on.show()

                        elif event.ui_element == self.start_trigger:  # start game
                            game = MainGame(screen_size=self.screen_size, music_on=self.music_on,
                                            difficulty=self.difficulty, ship=self.ship_names[self.now_ship])
                            self.menu_init()
                            self.load_music()

                        elif event.ui_element == self.btn_quit:  # quit game
                            if self.music_on:
                                pygame.mixer.Sound('sounds/ButtonQuit.mp3').play()

                            pygame.quit()
                            sys.exit(-1)

                        elif event.ui_element == self.btn_return:  # close settings
                            if self.music_on:
                                pygame.mixer.Sound('sounds/ButtonQuit.mp3').play()

                            self.hide_all_btns()

                            self.btn_start.show()
                            self.btn_settings.show()
                            self.btn_quit.show()
                            self.label_change_screen_size.hide()
                            self.label_change_music_on.hide()

                            self.save_settings()


                        elif event.ui_element in self.dropdownmenu_screen_size.get_focus_set():  # change screen size data
                            if self.music_on:
                                pygame.mixer.Sound('sounds/ButtonMenu.mp3').play()

                            if event.ui_element.text != '▼':
                                self.screen_size = list(map(int, event.ui_element.text.split('*')))

                        elif event.ui_element in self.dropdownmenu_difficulty.get_focus_set():  # change difficulty
                            if self.music_on:
                                pygame.mixer.Sound('sounds/ButtonMenu.mp3').play()
                            if event.ui_element.text != '▼':
                                self.difficulty = event.ui_element.text


                        elif event.ui_element in self.dropdownmenu_sound.get_focus_set():  # change music data
                            if self.music_on:
                                pygame.mixer.Sound('sounds/ButtonMenu.mp3').play()

                            if event.ui_element.text == 'On':
                                self.music_on = True
                                pygame.mixer.music.play()
                            else:
                                self.music_on = False
                                pygame.mixer.music.pause()

                        if event.ui_element == self.btn_next:  # next ship
                            if self.music_on:
                                pygame.mixer.Sound('sounds/ButtonMenu.mp3').play()

                            if self.now_ship + 1 < len(self.ships):
                                self.now_ship += 1
                                self.ship.kill()
                                self.ship = self.ships[self.now_ship](self.ships_group, self.ship_pos)
                                self.feature_describe_text.set_text(self.ship_describe[self.now_ship])
                                self.feature_recomendation_text.set_text(self.ship_recommended[self.now_ship])

                        elif event.ui_element == self.btn_previous:  # previous ship
                            if self.music_on:
                                pygame.mixer.Sound('sounds/ButtonMenu.mp3').play()

                            if self.now_ship - 1 >= 0:
                                self.now_ship -= 1
                                self.ship.kill()
                                self.ship = self.ships[self.now_ship](self.ships_group, self.ship_pos)
                                self.feature_describe_text.set_text(self.ship_describe[self.now_ship])
                                self.feature_recomendation_text.set_text(self.ship_recommended[self.now_ship])
                        elif event.ui_element == self.go_to_menu:
                            if self.music_on:
                                pygame.mixer.Sound('sounds/ButtonQuit.mp3').play()

                            self.menu_init()

                        text_pos = (self.width // 2 - self.label_ship_name.rect[2] // 2, self.height // 5)
                        self.label_ship_name.rect = pygame.Rect(
                            text_pos, (self.label_ship_name.rect[2], self.label_ship_name.rect[3]))
                        self.label_ship_name.set_text(self.ships[self.now_ship].get_name(False))
                self.manager.process_events(event)

            self.manager.update(time_delta=self.clock.tick(self.fps) / 1000.0)
            bg.draw()
            self.manager.draw_ui(self.screen)
            self.ships_group.draw(self.screen)
            if self.draw_logo:
                self.logo_group.draw(self.screen)

            pygame.display.flip()
