import sys
import json
import pygame
import pygame_gui
# from Buttons.Start import Start
from BackgroundStars import BackgroundStars
from main import MainGame
from ImageLoader import load_image
import random


class Logo(pygame.sprite.Sprite):
    def __init__(self, logo_group, pos):
        super().__init__(logo_group)
        self.image = load_image('Logo.png', (0, 0, 0))
        self.image = pygame.transform.scale(self.image, (270, 140))
        self.rect = pygame.Rect(int(pos[0] / 2), pos[1], 270, 140)


class Menu:
    def __init__(self, screen_size, difficulty, music_on):
        self.screen_size = screen_size
        self.width, self.height = screen_size
        self.difficulty = difficulty
        self.music_on = music_on
        self.logo_group = pygame.sprite.Group()

        self.run()

    def run(self):
        pygame.init()
        self.music = random.choice(['MainMenu_1.mp3', 'MainMenu_2.mp3'])
        if self.music_on:
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.load('sounds/' + self.music)
            pygame.mixer.music.play()

        self.screen = pygame.display.set_mode(self.screen_size)

        self.running = True
        self.speed = 1
        self.fps = 30
        self.clock = pygame.time.Clock()
        self.logo = Logo(self.logo_group, (self.width // 2 + 35, self.height // 4 - 80))
        bg = BackgroundStars(self, 400)

        manager = pygame_gui.UIManager(self.screen_size)

        btn_start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3), (250, 50)),
            text='Start', manager=manager)
        btn_settings = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3 + 80), (250, 50)),
            text='Settings', manager=manager)
        btn_quit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3 + 160), (250, 50)),
            text='Quit', manager=manager)

        btn_size_1920_1080 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3),
                                      (250, 50)),
            text='1920*1080', manager=manager)

        btn_size_600_700 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3 + 80),
                                      (200, 50)),
            text='600*700', manager=manager)

        btn_size_500_500 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3 + 160),
                                      (150, 50)),
            text='500*500', manager=manager)
        btn_return = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - 250 // 2, self.height // 3 + 240),
                                      (250, 50)),
            text='Back To Menu', manager=manager)

        btn_difficulty = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 190, self.height - 60),
                                      (180, 50)),
            text=self.difficulty, manager=manager)

        if self.music_on:
            btn_sound = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((10, self.height - 80),
                                          (70, 70)), text='SoundOn', manager=manager)
        else:
            btn_sound = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((10, self.height - 80),
                                          (70, 70)), text='SoundOff', manager=manager)

        # btn_sound_image = pygame.transform.scale(pygame.image.load('sprites/SoundOn.jpg'), (70, 70))
        # btn_sound.set_image(btn_sound_image)

        btn_size_1920_1080.hide()
        btn_size_600_700.hide()
        btn_size_500_500.hide()
        btn_difficulty.hide()
        btn_sound.hide()
        btn_return.hide()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == btn_start:  # start game
                            game = MainGame(self.screen_size, self.difficulty, self.music_on)
                        elif event.ui_element == btn_settings:  # open settings
                            btn_start.hide()
                            btn_settings.hide()
                            btn_quit.hide()

                            btn_size_1920_1080.show()
                            btn_size_600_700.show()
                            btn_size_500_500.show()
                            btn_difficulty.show()
                            btn_return.show()
                            btn_sound.show()

                        elif event.ui_element == btn_quit:  # quit game
                            pygame.quit()
                            sys.exit(-1)

                        elif event.ui_element == btn_return:  # close settings
                            btn_size_1920_1080.hide()
                            btn_size_600_700.hide()
                            btn_size_500_500.hide()
                            btn_difficulty.hide()
                            btn_return.hide()
                            btn_sound.hide()

                            btn_start.show()
                            btn_settings.show()
                            btn_quit.show()

                            self.difficulty = btn_difficulty.text

                            with open('settings.json', mode='w') as json_file:
                                new_settings = {"screen_size": self.screen_size,
                                                "music_on": self.music_on,
                                                "difficulty": self.difficulty}
                                new_json = json.dumps(new_settings)
                                json_file.write(new_json)

                        elif event.ui_element == btn_sound:  # turn off/on sound
                            if btn_sound.text == 'SoundOn':
                                btn_sound.set_text('SoundOff')
                                self.music_on = False
                            else:
                                btn_sound.set_text('SoundOn')
                                self.music_on = True
                        elif event.ui_element == btn_size_1920_1080:  # change screen size
                            self.screen_size = (1920, 1080)
                        elif event.ui_element == btn_size_600_700:  # change screen size
                            self.screen_size = (600, 700)
                        elif event.ui_element == btn_size_500_500:  # change screen size
                            self.screen_size = (500, 500)
                        elif event.ui_element == btn_difficulty:
                            if btn_difficulty.text == 'Low':
                                btn_difficulty.set_text('Normal')
                            elif btn_difficulty.text == 'Normal':
                                btn_difficulty.set_text('Hard')
                            elif btn_difficulty.text == 'Hard':
                                btn_difficulty.set_text('God Of Gamers')
                            else:
                                btn_difficulty.set_text('Low')

                manager.process_events(event)

            manager.update(time_delta=self.clock.tick(self.fps) / 1000.0)
            bg.draw()
            manager.draw_ui(self.screen)
            self.logo_group.draw(self.screen)
            pygame.display.flip()
