import pygame
import random


class BackgroundStars:
    def __init__(self, game, stars_count, speed_range):
        self.game = game
        self.screen = game.screen
        self.speed_range = speed_range

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()

        # generate N stars
        self.stars = [
            [random.randint(0, game.width), random.randint(0, game.height)]
            for _ in range(stars_count)
        ]
        self.stars_speed = [random.randint(speed_range[0], speed_range[1]) for _ in range(stars_count)]

    def draw(self):
        self.background.fill((0, 0, 0))
        for n, star in enumerate(self.stars):
            pygame.draw.line(self.background,
                             (255, 255, 255), (star[0], star[1]), (star[0], star[1]))
            star[1] += self.stars_speed[n]
            if star[1] > self.game.height:
                star[0] = random.randint(0, self.game.width)
                star[1] = 0
                self.stars_speed[n] = random.randint(self.speed_range[0], self.speed_range[1])
        self.screen.blit(self.background, (0, 0))
