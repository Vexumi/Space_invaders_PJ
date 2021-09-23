import pygame
import random


class BackgroundStars:
    def __init__(self, game, stars_count):
        self.game = game
        self.speed = 1
        self.screen = game.screen

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()

        # generate N stars
        self.stars = [
            [random.randint(0, game.width), random.randint(0, game.height)]
            for _ in range(stars_count)
        ]

    def draw(self):
        self.background.fill((0, 0, 0))
        for star in self.stars:
            pygame.draw.line(self.background,
                             (255, 255, 255), (star[0], star[1]), (star[0], star[1]))
            star[1] += self.speed
            if star[1] > self.game.height:
                star[0] = random.randint(0, self.game.width)
                star[1] = 0
        self.screen.blit(self.background, (0, 0))
