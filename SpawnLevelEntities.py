from Aliens import Aliens
from Lasers import Lasers
from AbilityHealth import AbilityHealth
from AbilityShotgun import AbilityShotgun


def Spawner(self, wave):
    aliens = []
    laser = []
    for i in range(wave['Aliens']):
        aliens.append(Aliens(self, self.all_sprites))

    for i in range(wave['Lasers']):
        laser.append(Lasers(self, self.all_sprites))

    abilities_data = wave['Abilities']
    if len(abilities_data.keys()) != 0:
        for key in abilities_data.keys():
            for _ in range(abilities_data[key]):
                self.abilities.append(eval(f'Ability{key}(self, self.all_sprites)'))

    return [aliens, laser]
