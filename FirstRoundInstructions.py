import pygame


def give_instructions(self):
    font = pygame.font.Font(None, 60)

    # start
    text_pos = (self.width / 2 - 50, self.height / 8 + 40)
    self.screen.blit(font.render('Start', False, (255, 255, 255)), text_pos)

    # control
    text_pos = (self.width / 2 - 190, self.height - self.height / 4)
    self.screen.blit(font.render('WASD - Управление', False, (255, 255, 255)), text_pos)

    # fire
    text_pos = (self.width / 2 - 160, self.height - self.height / 4 + 40)
    self.screen.blit(font.render('Space - Стрелять', False, (255, 255, 255)), text_pos)
