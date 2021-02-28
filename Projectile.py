# библиотеки
import pygame
from pygame import *
import pygame as pg
import math
import os

# блок звуков и музыки
pg.init()
FlC1 = pg.mixer.Sound(os.path.join('data', "FluteC1.mp3"))
FlD1 = pg.mixer.Sound(os.path.join('data', "FluteD1.mp3"))
FlE1 = pg.mixer.Sound(os.path.join('data', "FluteE1.mp3"))
FlF1 = pg.mixer.Sound(os.path.join('data', "FluteF1.mp3"))
FlG1 = pg.mixer.Sound(os.path.join('data', "FluteG1.mp3"))
FlA1 = pg.mixer.Sound(os.path.join('data', "FluteA1.mp3"))
FlB1 = pg.mixer.Sound(os.path.join('data', "FluteB1.mp3"))
FlC2 = pg.mixer.Sound(os.path.join('data', "FluteC2.mp3"))
FlD2 = pg.mixer.Sound(os.path.join('data', "FluteD2.mp3"))
FlE2 = pg.mixer.Sound(os.path.join('data', "FluteE2.mp3"))

GtAm = pg.mixer.Sound(os.path.join('data', "GuitarAm.mp3"))
GtF = pg.mixer.Sound(os.path.join('data', "GuitarF.mp3"))
GtG = pg.mixer.Sound(os.path.join('data', "GuitarG.mp3"))
GtDm = pg.mixer.Sound(os.path.join('data', "GuitarDm.mp3"))

HpFAB = pg.mixer.Sound(os.path.join('data', "HarpFAB.mp3"))
HpBDB = pg.mixer.Sound(os.path.join('data', "HarpBDB.mp3"))
HpFAE = pg.mixer.Sound(os.path.join('data', "HarpFAE.mp3"))
HpBFB = pg.mixer.Sound(os.path.join('data', "HarpBFB.mp3"))
HpEFB = pg.mixer.Sound(os.path.join('data', "HarpEFB.mp3"))
HpFEF = pg.mixer.Sound(os.path.join('data', "HarpFEF.mp3"))
HpDCD = pg.mixer.Sound(os.path.join('data', "HarpDCD.mp3"))
HpBAB = pg.mixer.Sound(os.path.join('data', "HarpBAB.mp3"))
HpDEF = pg.mixer.Sound(os.path.join('data', "HarpDEF.mp3"))

fluteSound = [FlE2, FlD2, FlE2, FlC2, FlE2, FlB1, FlE2, FlA1, FlE2, FlG1, FlE2, FlF1, FlE2, FlD2,
              FlD2, FlC2, FlD2, FlB1, FlD2, FlA1, FlD2, FlG1, FlD2, FlF1, FlD2, FlE1, FlD2, FlC2,
              FlC2, FlB1, FlC2, FlA1, FlC2, FlG1, FlC2, FlF1, FlC2, FlE1, FlC2, FlD1, FlC2, FlB1,
              FlB1, FlA1, FlB1, FlG1, FlF1, FlE1, FlD1, FlC1, FlB1, FlA1]

guitarSound = [GtAm, GtF, GtG, GtAm, GtF, GtG, GtAm, GtF, GtG,
               GtAm, GtF, GtDm, GtG, GtAm, GtF, GtDm, GtG]

harpSound = [HpFAB, HpBDB, HpFAB, HpBDB, HpFAB, HpBDB, HpFAB,
             HpFAB, HpBDB, HpFAE, HpBFB, HpFAB, HpBDB, HpEFB,
             HpFEF, HpDCD, HpBAB, HpDEF,
             HpFEF, HpDCD, HpBAB, HpDEF, HpFAB]

projectile_group = pygame.sprite.Group()

# переменные снаряда
RADIUS = 5
SPEED = 10
TIME = 125


# класс снаряда
class bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, instrument, sound=None):
        super().__init__(projectile_group)
        # характеристики объекта
        self.x = x
        self.y = y
        self.time = TIME
        self.radius = RADIUS
        self.vx = SPEED * math.cos(angle)
        self.vy = SPEED * math.sin(angle)
        # отрисовка объекта
        self.radius = RADIUS
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"),
                           (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
        # звук при создании
        if not sound == None:
            if instrument == "flute":
                fluteSound[sound].play()
            elif instrument == "guitar":
                guitarSound[sound].play()
            elif instrument == "harp":
                harpSound[sound].play()

    # функция обновления
    def update(self, horizontal_borders, vertical_borders, exit_zone):
        # перемещиние объекта
        self.rect = self.rect.move(self.vx, self.vy)
        # уменьшение таймера жизни объекта
        self.time -= 1
        # изменение размера при нахождении в зоне перехода
        if pygame.sprite.spritecollideany(self, exit_zone):
            self.radius = 10
        else:
            self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        # изменение яркости объекта в зависимости от оставшегося времени жизни
        pygame.draw.circle(self.image, (self.time * 2, self.time * 2, self.time * 2),
                           (self.radius, self.radius), self.radius)
        # отражение от стенок
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            pygame.sprite.spritecollideany(self, horizontal_borders).knock()
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            pygame.sprite.spritecollideany(self, vertical_borders).knock()
            self.vx = -self.vx
        # удаление снаряда при нулевом таймере
        if self.time == 0:
            self.kill()


# класс полоски реакции
class reactionLine(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(projectile_group)
        # переменные объекта
        self.x = x + 295
        self.y = y
        self.live = 300
        # отрисовка объекта
        self.image = pygame.Surface((30, 120))
        pygame.draw.rect(self.image, pygame.Color("white"), (0, 0, 30, 120))
        self.rect = pygame.Rect(self.x, self.y, 30, 120)

    # функция обновления
    def update(self):
        # уменьшает время жизни объекта и двигает его влево
        self.live -= 6
        self.rect = self.rect.move(-6, 0)
        # если жизнь меньше 0 удаление объекта
        if self.live < 0:
            self.kill()
