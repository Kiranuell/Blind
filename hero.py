# библиотеки
from pygame import *
import pygame
import os
import sys

# характеристики персонажа
HEIGHT = 70  # высота
WIDTH = 60  # ширина
STEP = 0.5  # величина на которую увеличивается горизонтальная скорость
MAXRUN = 5  # максимальная горизонтальная скорость
JUMP_POWER = 11  # сила прыжка
GRAVITY = 0.35  # гравитация


# функция загрузки изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# класс героя
class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(pygame.sprite.Group())
        # переменные героя
        self.x = x
        self.y = y
        self.yvel = 0
        self.xvel = 0
        self.onGround = False
        self.seeRight = True

        # переменные анимации
        self.frames = []
        self.cut_sheet(load_image("HeroAnimation.png"), 13, 1)
        self.stay_frame = 0
        self.run_frame = 4
        self.image = self.frames[0]
        self.staytick = 0
        self.runtick = 0
        self.image = Surface((WIDTH, HEIGHT))
        self.rect = Rect(x, y, WIDTH, HEIGHT)

    # разбитие загруженного изображения на картинки анимации
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    # функция обновления
    def update(self, up, left, right, wals):
        if up and self.onGround:
            self.yvel -= JUMP_POWER
        if left:
            self.xvel -= STEP
            if self.xvel < MAXRUN * -1:
                self.xvel = MAXRUN * -1
            if self.seeRight:
                self.seeRight = False
                self.image = pygame.transform.flip(self.image, True, False)
        if right:
            self.xvel += STEP
            if self.xvel > MAXRUN:
                self.xvel = MAXRUN
            if not self.seeRight:
                self.seeRight = True
                self.image = pygame.transform.flip(self.image, True, False)

        if left or right:
            self.runtick += 1
            if self.runtick == 5:
                self.run_frame += 1
                if self.run_frame == 10:
                    self.run_frame = 4
                self.runtick = 0
            self.image = self.frames[self.run_frame]
            if not self.seeRight:
                self.image = pygame.transform.flip(self.image, True, False)

        if not (left or right):
            if self.xvel > 0:
                self.xvel -= STEP * 2
                if self.xvel < 0:
                    self.xvel = 0
            if self.xvel < 0:
                self.xvel += STEP * 2
                if self.xvel > 0:
                    self.xvel = 0

            if self.xvel == 0:
                self.staytick += 1
                if self.staytick == 15:
                    self.stay_frame += 1
                    if self.stay_frame == 4:
                        self.stay_frame = 0
                    self.staytick = 0
                self.image = self.frames[self.stay_frame]
                if not self.seeRight:
                    self.image = pygame.transform.flip(self.image, True, False)

        if not self.onGround:
            self.yvel += GRAVITY

        if self.yvel < -5:
            self.image = self.frames[10]
            if not self.seeRight:
                self.image = pygame.transform.flip(self.image, True, False)
        elif -5 < self.yvel < 5 and not self.onGround:
            self.image = self.frames[11]
            if not self.seeRight:
                self.image = pygame.transform.flip(self.image, True, False)
        elif self.yvel > 5:
            self.image = self.frames[12]
            if not self.seeRight:
                self.image = pygame.transform.flip(self.image, True, False)

        self.onGround = False
        self.rect.x += self.xvel
        self.colide(self.xvel, 0, wals)
        self.rect.y += self.yvel
        self.colide(0, self.yvel, wals)

    # функция столкновения
    def colide(self, xvel, yvel, wals):
        for p in wals:
            if sprite.collide_rect(self, p):
                if sprite.collide_rect(self, p):
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        self.xvel = 0

                    if xvel < 0:
                        self.rect.left = p.rect.right
                        self.xvel = 0

                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 1

                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 1

    # функция позиции персонажа
    def pos(self):
        return self.rect.x, self.rect.y


# класс камеры
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, width, height):
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)
