from Aliens import Aliens
from Lasers import Lasers
from SpaceInt import SpaceInt
from Abilities.AbilityViewHP import AbilityViewHP
from Abilities.AbilityHealth import AbilityHealth
from Abilities.AbilityLuckyBlock import AbilityLuckyBlock
from Abilities.AbilityShotgun import AbilityShotgun
from Abilities.AbilityMine import AbilityMine


def Spawner(self, wave):
    aliens = []
    laser = []
    ints = []

    if self.width == 1920:
        screen_size_delta = 2
    else:
        screen_size_delta = 1

    for _ in range(screen_size_delta):

        for i in range(wave['Aliens']):
            aliens.append(Aliens(self, self.all_sprites))

        for i in range(wave['Lasers']):
            laser.append(Lasers(self, self.all_sprites))

        for i in range(wave['SpaceInt']):
            ints.append(SpaceInt(self, self.all_sprites))

    abilities_data = wave['Abilities']
    if len(abilities_data.keys()) != 0:
        for key in abilities_data.keys():
            for _ in range(abilities_data[key]):
                self.abilities.append(eval(f'Ability{key}(self, self.all_sprites)'))

    return [aliens, laser, ints]
