from Bullet import Bullet


def BasicFire(self):
    self.bullets.append(Bullet(self, self.hero.rect.x + 35, self.hero.rect.y, self.all_sprites))


def Shoot(self):
    if 'Shotgun' in self.hero.abilities_owned:
        if self.shotgun_fire_max == self.shotgun_fire_count:  # if out of bullets - set to zero vars
            del self.hero.abilities_owned[self.hero.abilities_owned.index('Shotgun')]
            self.shotgun_fire_count = 0
            BasicFire(self)
        else:
            self.shotgun_fire_count += 1

            shotgun_bullet_delta = 40  # distance between bullets

            self.bullets.append(
                Bullet(self, self.hero.rect.x + 35 - shotgun_bullet_delta, self.hero.rect.y,
                       self.all_sprites))  # left bullet
            self.bullets.append(
                Bullet(self, self.hero.rect.x + 35, self.hero.rect.y,
                       self.all_sprites))  # center bullet
            self.bullets.append(
                Bullet(self, self.hero.rect.x + 35 + shotgun_bullet_delta, self.hero.rect.y,
                       self.all_sprites))  # right bullet
    else:
        BasicFire(self)
