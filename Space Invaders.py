import pygame
import json
from main import MainGame
from Menu import Menu
from Intro import Intro
with open('settings.json', mode='r') as json_file:
    json_data = json.load(json_file)
    json_file.close()

difficulty = json_data['difficulty']
music_on = json_data['music_on']
screen_size = json_data['screen_size']

# инициализация Pygame
pygame.init()
pygame.display.set_caption('Space Invaders')


# создание игры
if __name__ == '__main__':
    intro = Intro(screen_size)
    game = Menu(screen_size, difficulty, music_on)
    pygame.quit()
