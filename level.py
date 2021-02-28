import pygame
import os

# группы
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


# функция загрузки уровня
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r', encoding="utf-8") as mapFile:
        level_map = [line.strip() for line in mapFile]

    return level_map


# класс стенки
class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(pygame.sprite.Group())
        self.light = 0
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.image.fill("black")
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.image.fill("black")
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    # функция обновления
    def update(self):
        # изменение яркости стенки
        if self.light != 0:
            self.light -= 1
            self.image.fill((self.light * 2, self.light * 2, self.light * 2))

    # функция вызываемая при столкновении со снарядом
    def knock(self):
        self.light = 100


# класс перехода на новый уровень
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(pygame.sprite.Group())
        self.image = pygame.Surface([width, height])
        self.rect = pygame.Rect(x, y, width, height)


# функция отрисовки уровня
def draw_level(filename):
    # получение уровня из файла
    levelMap = load_level(filename)
    # Создание стенок
    horiz = True
    y = 0
    for i in levelMap:
        if horiz:
            tile = 0
            for j in i:
                if j == "#":
                    Border(0 + 80 * tile, y, 80 + 80 * tile, y)
                tile += 1
        else:
            tile = 0
            for j in i:
                if j == "#":
                    Border(80 * tile, y, 80 * tile, y + 80)
                tile += 1
            y += 80
        horiz = not horiz
    # возвращает две группы стенок
    return horizontal_borders, vertical_borders
