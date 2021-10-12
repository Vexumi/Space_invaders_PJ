import cv2
import pygame


class Intro:
    def __init__(self, screen_size, music_on):
        self.screen_size = screen_size
        self.music_on = music_on
        self.intro_1()
        self.intro_2()

    def intro_1(self):
        cap = cv2.VideoCapture('Videos/Intro.mp4')
        if self.music_on:
            pygame.mixer.music.load('sounds/Intro_1.mp3')
            pygame.mixer.music.play()
        success, img = cap.read()
        shape = img.shape[1::-1]
        wn = pygame.display.set_mode(self.screen_size)
        clock = pygame.time.Clock()

        while success:
            clock.tick(60)
            success, img = cap.read()
            if not success:
                break
            shape = img.shape[:2]
            img = cv2.resize(img, (self.screen_size[0], self.screen_size[1]), interpolation=cv2.INTER_AREA)
            shape = img.shape[1::-1]
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    success = False
            image = pygame.image.frombuffer(img.tobytes(), shape, "BGR")
            wn.blit(image, (0, 0))
            pygame.display.update()
        pygame.mixer.music.stop()

    def intro_2(self):
        cap = cv2.VideoCapture('Videos/Intro_2.mp4')
        success, img = cap.read()
        shape = img.shape[1::-1]
        wn = pygame.display.set_mode(self.screen_size)
        if self.music_on:
            pygame.mixer.music.load('sounds/Intro_2 V2.mp3')
            pygame.mixer.music.play()
        clock = pygame.time.Clock()

        while success:
            clock.tick(30)
            success, img = cap.read()
            if not success:
                break
            shape = img.shape[:2]
            img = cv2.resize(img, (self.screen_size[0], self.screen_size[1]), interpolation=cv2.INTER_AREA)
            shape = img.shape[1::-1]
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    success = False
            image = pygame.image.frombuffer(img.tobytes(), shape, "BGR")
            wn.blit(image, (0, 0))
            pygame.display.update()
        pygame.mixer.music.stop()
