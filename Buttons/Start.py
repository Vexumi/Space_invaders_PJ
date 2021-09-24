import pygame


class Start(pygame.sprite.Sprite):
    def __init__(self, game, all_btns):
        super().__init__(all_btns)
        self.screen_size = game.screen_size

        self.btn_width = self.screen_size[0] // 4
        self.btn_height = self.btn_width // 2

        self.image = pygame.Surface((self.btn_width, self.btn_height), pygame.SRCALPHA, 32)

        self.rect = pygame.Rect(self.screen_size[0] // 2 - self.btn_width // 2,
                                self.screen_size[1] // 4, self.btn_width, self.btn_height)
        pygame.draw.rect(self.image, (30, 60, 150), (0, 0, self.btn_width, self.btn_height))

    def update(self):
        pass