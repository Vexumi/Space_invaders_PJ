import cv2
import pygame


class Intro:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.run()

    def run(self):
        cap = cv2.VideoCapture('Intro.mp4')
        success, img = cap.read()
        shape = img.shape[1::-1]
        wn = pygame.display.set_mode(self.screen_size)
        clock = pygame.time.Clock()

        while success:
            clock.tick(60)
            success, img = cap.read()
            shape = img.shape[:2]
            img = cv2.resize(img, (self.screen_size[0], self.screen_size[1]), interpolation=cv2.INTER_AREA)
            shape = img.shape[1::-1]
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    success = False
            image = pygame.image.frombuffer(img.tobytes(), shape, "BGR")
            wn.blit(image, (0, 0))
            pygame.display.update()
