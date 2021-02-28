# библиотеки
import pygame
import math
from level import draw_level, Exit
from hero import Hero, Camera
from Projectile import bullet, reactionLine
import os
import sys


# функция загрзки сохранненого изображения
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


# функция стартового экрана
def start_screen():
    # таймер внутри функции отвечающий за анимацию и отрисовку кадра
    timer = 100

    # блок шрифта и текста
    font = pygame.font.Font(None, 85)
    logo = font.render("Blind", True, (200, 200, 200))
    place = logo.get_rect(center=(infoObject.current_w // 2, 50))

    text1 = font.render("Где я?", True, (200, 200, 200))
    text2 = font.render("Полная темнота и тишина", True, (200, 200, 200))
    text3 = font.render("Я в каком то подземелье?", True, (200, 200, 200))
    text4 = font.render("Царь все таки отомстил мне за ту песню...", True, (200, 200, 200))
    text5 = font.render("У меня осталась только верная флейта", True, (200, 200, 200))
    text6 = font.render("Нужно поскорее выбираться отсюда!", True, (200, 200, 200))
    text7 = font.render("Управление", True, (200, 200, 200))
    text8 = font.render("нажмите любую клавишу, чтобы начать", True, (200, 200, 200))

    place1 = text1.get_rect(center=(200, 100))
    place2 = text2.get_rect(center=(infoObject.current_w - 500, 100))
    place3 = text3.get_rect(center=(475, 175))
    place4 = text4.get_rect(center=(700, 250))
    place5 = text5.get_rect(center=(665, 325))
    place6 = text6.get_rect(center=(645, 400))
    place7 = text7.get_rect(center=(infoObject.current_w // 2, infoObject.current_h - 220))
    place8 = text8.get_rect(center=(infoObject.current_w // 2, infoObject.current_h - 50))

    # загрузка нужных изображений
    mouse = load_image("mouse2.png")
    control = load_image("control.png")
    react = load_image("reaction.png")

    # основной цикл функции
    running = True
    while running:
        # начало отрисовки нового кадра
        screen.fill("black")
        screen.blit(logo, place)

        # проверка на события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if timer > 1600:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if timer > 1600:
                    running = False

        # изменение таймера
        timer += 1
        if timer == 1800:
            timer = 1600

        # отрисовка кадра в зависимости от прошедшего времени (timer)
        if timer > 200:
            text1 = font.render("Где я?", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(text1, place1)
        if timer > 400:
            text2 = font.render("Полная темнота и тишина", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(text2, place2)
        if timer > 600:
            text3 = font.render("Я в каком то подземелье?", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(text3, place3)
        if timer > 800:
            text4 = font.render("Царь все таки отомстил мне за ту песню...", True,
                                (timer % 200, timer % 200, timer % 200))
            screen.blit(text4, place4)
        if timer > 1000:
            text5 = font.render("У меня осталась только верная флейта", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(text5, place5)
        if timer > 1200:
            text6 = font.render("Нужно поскорее выбираться отсюда!", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(text6, place6)
        if timer > 1400:
            text7 = font.render("Управление", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(text7, place7)
            screen.blit(control, (infoObject.current_w // 2 - 400, infoObject.current_h - 300))
            screen.blit(mouse, (infoObject.current_w // 2 + 250, infoObject.current_h - 300))
            screen.blit(react, (infoObject.current_w // 2 + 400, infoObject.current_h - 300))
        if timer > 1600:
            text8 = font.render("нажмите любую клавишу, чтобы начать", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(text8, place8)

        # новый кадр
        pygame.display.flip()
        clock.tick(FPS)


# функция промежуточного экрана
def between_screen(level):
    # таймер внутри функции отвечающий за анимацию
    timer = 100

    # блок шрифта и текста
    font = pygame.font.Font(None, 85)
    logo = font.render("Вы нашли:", True, (200, 200, 200))
    place = logo.get_rect(center=(infoObject.current_w // 2, 100))
    text2 = font.render("Нажмите любую клавишу, чтобы продолжить", True, (200, 200, 200))
    place2 = text2.get_rect(center=(infoObject.current_w // 2, infoObject.current_h - 100))

    # в зависимости от уровня, на экране появляется разный текст и изображение
    if level == 2:
        unlock = load_image("newGuitar.png")
        text1 = font.render("Гитара", True, (200, 200, 200))
        place1 = text1.get_rect(center=(infoObject.current_w // 2, 150))
    elif level == 3:
        unlock = load_image("newHarp.png")
        text1 = font.render("Арфа", True, (200, 200, 200))
        place1 = text1.get_rect(center=(infoObject.current_w // 2, 150))

    # основной цикл функции
    running = True
    while running:
        # начало отрисовки нового кадра
        screen.fill("black")

        # проверка на события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if timer > 600:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if timer > 600:
                    running = False

        # изменение таймера
        timer += 1
        if timer == 800:
            timer = 600

        # отрисовка кадра в зависимости от прошедшего времени (timer)
        if timer > 200:
            logo = font.render("Вы нашли:", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(logo, place)
        if timer > 400:
            if level == 2:
                text1 = font.render("Гитара", True, (timer % 200, timer % 200, timer % 200))
                screen.blit(unlock, (infoObject.current_w // 2 - 200, 200))
            elif level == 3:
                text1 = font.render("Арфа", True, (timer % 200, timer % 200, timer % 200))
                screen.blit(unlock, (infoObject.current_w // 2 - 150, 200))
            screen.blit(text1, place1)
        if timer > 600:
            text2 = font.render("Нажмите любую клавишу, чтобы продолжить", True,
                                (timer % 200, timer % 200, timer % 200))
            screen.blit(text2, place2)

        # новый кадр
        pygame.display.flip()
        clock.tick(FPS)


# функция конечного экрана
def end_screen():
    # таймер внутри функции отвечающий за анимацию и отрисовку кадра
    timer = 100

    # блок шрифта и текста
    font = pygame.font.Font(None, 85)
    logo = font.render("Blind", True, (200, 200, 200))
    place = logo.get_rect(center=(infoObject.current_w // 2, 50))

    text1 = font.render("Фух, было нелегко...", True, (200, 200, 200))
    text2 = font.render("Но похоже это только начало", True, (200, 200, 200))
    text3 = font.render("СПАСИБО ЗА ИГРУ", True, (200, 200, 200))
    text4 = font.render("esc, чтобы выйти", True, (200, 200, 200))
    place1 = text1.get_rect(center=(400, 150))
    place2 = text2.get_rect(center=(infoObject.current_w - 500, 250))
    place3 = text3.get_rect(center=(infoObject.current_w // 2, 450))
    place4 = text4.get_rect(center=(infoObject.current_w // 2, 650))

    # основной цикл функции
    running = True
    while running:
        # начало отрисовки нового кадра
        screen.fill("black")
        screen.blit(logo, place)

        # проверка на события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if timer > 1000:
                    running = False

        # изменение таймера
        timer += 1
        if timer == 1200:
            timer = 1000

        # отрисовка кадра в зависимости от прошедшего времени (timer)
        if timer > 200:
            text1 = font.render("Фух, было нелегко...", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(text1, place1)
        if timer > 400:
            text2 = font.render("Но похоже это только начало", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(text2, place2)
        if timer > 600:
            text3 = font.render("СПАСИБО ЗА ИГРУ", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(text3, place3)
        if timer > 1000:
            text4 = font.render("esc, чтобы выйти", True, (timer % 200, timer % 200, timer % 200))
            screen.blit(text4, place4)

        # новый кадр
        pygame.display.flip()
        clock.tick(FPS)


# основная программа
if __name__ == '__main__':
    # создание окна
    pygame.init()
    infoObject = pygame.display.Info()
    size = width, height = infoObject.current_w, infoObject.current_h
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill("black")

    # добавление ограничение фпс
    clock = pygame.time.Clock()
    FPS = 60

    # создание групп спрайтов
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    projectile_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    exit_zone = pygame.sprite.Group()
    reaction_group = pygame.sprite.Group()

    # отрисовка первого уровня
    horizontal_borders, vertical_borders = draw_level("level1.txt")
    wall_group.add(horizontal_borders)
    wall_group.add(vertical_borders)
    all_sprites.add(horizontal_borders)
    all_sprites.add(vertical_borders)

    # создание камеры и персонажа
    camera = Camera(width, height)
    hero = Hero(20, 790)
    all_sprites.add(hero)

    # добавление игрового курсора
    cursor = load_image("cursor.png")
    pygame.mouse.set_visible(False)
    mx = 0
    my = 0

    # создание переменных нажатия клавиш
    up = False
    left = False
    right = False

    # создание элементов отвечающих за музыку
    sound = 0
    song = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2,
            1, 1, 1, 2, 2, 2, 2, 2, 1, 2]
    note = 0
    notClick = True
    harpTime = 0
    reactionTime = 0
    pauseTime = 0

    # добавление дополнительных изображений
    frame_instrument = load_image("pan_flute.png")
    E_button = load_image("E.png")

    # создание переменной текущего уровня
    level = 1

    # создание места перехода на другой уровень
    exit = Exit(0, 0, 160, 160)
    exit_zone.add(exit)

    # запуск стартового экрана
    start_screen()

    # основной цикл
    running = True
    while running:
        # начало отрисовки нового кадра
        screen.fill("black")

        # проверка на события
        for event in pygame.event.get():
            # проверка закрытия окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            # проверка кнопок управления (w, a, d)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                up = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                right = True
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                up = False
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                right = False

            # проверка перехода на следующий уровень
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                # если персонаж находится в зоне перехода
                if pygame.sprite.spritecollideany(hero, exit_zone):
                    # удаление старого персонажа и уровня
                    hero.kill()
                    for i in wall_group:
                        i.kill()
                    wall_group.empty()
                    projectile_group.empty()
                    all_sprites.empty()
                    exit_zone.empty()
                    # создание локации, героя, музыки и инструмента в зависимости от уровня
                    if level == 1:
                        horizontal_borders, vertical_borders = draw_level("level2.txt")
                        hero = Hero(960, 1280)
                        exit = Exit(960, 0, 80, 80)
                        frame_instrument = load_image("guitar.png")
                        song = [4, 2, 2, 4, 2, 2, 4, 2, 2,
                                4, 4, 4, 4, 4, 4, 4, 4]
                        note = 0
                        reactionTime = 0
                        pauseTime = 0
                        sound = 0
                        for i in reaction_group:
                            i.kill()
                    elif level == 2:
                        horizontal_borders, vertical_borders = draw_level("level3.txt")
                        hero = Hero(80, 240)
                        exit = Exit(2560, 160, 160, 160)
                        frame_instrument = load_image("harp.png")
                        song = [1, 1, 1, 1, 1, 1, 2,
                                1, 1, 1, 1, 1, 1, 2,
                                1, 1, 1, 2,
                                1, 1, 1, 1, 2]
                        note = 0
                        reactionTime = 0
                        pauseTime = 0
                        sound = 0
                        for i in reaction_group:
                            i.kill()
                    elif level == 3:
                        end_screen()
                        pygame.quit()

                    # переход на новый уровень
                    level += 1
                    # добавление в группы элементов
                    wall_group.add(horizontal_borders)
                    wall_group.add(vertical_borders)
                    all_sprites.add(horizontal_borders)
                    all_sprites.add(vertical_borders)
                    all_sprites.add(hero)
                    exit_zone.add(exit)
                    # запуск экрана между уровней
                    between_screen(level)

            # проверка на нажатие кнопки мышки
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # сбор координат персонажа и курсора
                mx, my = event.pos
                hx, hy = hero.pos()

                # рачеты угла полета снаряда
                distance_x = mx - hx
                distance_y = my - hy
                angle = math.atan2(distance_y, distance_x)

                # если игрок нажал вовремя
                if 0 < reactionTime < 15 and notClick:
                    # защита от двойного нажатия
                    notClick = False

                    # создание снарядов в зависимости от уровня
                    if level == 1:
                        projectile_group.add(bullet(hx + 20, hy + 10, angle, "flute", sound))
                        sound = (sound + 1) % len(song)
                    if level == 2:
                        projectile_group.add(bullet(hx + 20, hy + 10, angle, "guitar", sound))
                        projectile_group.add(bullet(hx + 20, hy + 10, angle + 0.25, "guitar"))
                        projectile_group.add(bullet(hx + 20, hy + 10, angle - 0.25, "guitar"))
                        sound = (sound + 1) % 14
                        sound = (sound + 1) % len(song)
                    if level == 3:
                        harpTime = 18

            # проверка на движение мышкой
            if event.type == pygame.MOUSEMOTION:
                mx, my = event.pos

        # проверка таймера арфы для запуска снарядов через промежуток времени
        if harpTime != 0:
            if harpTime % 6 == 0:
                hx, hy = hero.pos()
                distance_x = mx - hx
                distance_y = my - hy
                angle = math.atan2(distance_y, distance_x)
                if harpTime == 18:
                    projectile_group.add(bullet(hx + 20, hy + 10, angle, "harp", sound))
                    sound = (sound + 1) % len(song)
                else:
                    projectile_group.add(bullet(hx + 20, hy + 10, angle, "harp"))
            harpTime -= 1

        # обработка музыки и возможности запускать снаряд
        pauseTime -= 1
        reactionTime -= 1
        if pauseTime < 0:
            reaction_group.add(reactionLine(infoObject.current_w // 2 - 295, infoObject.current_h - 130))
            pauseTime = 50 * song[note]
            note = (note + 1) % len(song)
            reactionTime = 50
            notClick = True

        # обновление камеры, персонажа, снарядов, стен
        camera.update(hero)
        hero.update(up, left, right, wall_group)
        projectile_group.update(horizontal_borders, vertical_borders, exit_zone)
        wall_group.update()

        # отрисовка кадра
        exit_zone.draw(screen)
        all_sprites.draw(screen)
        projectile_group.draw(screen)
        screen.blit(frame_instrument, (10, infoObject.current_h - 130))

        # камера
        for sprite in exit_zone:
            camera.apply(sprite)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in projectile_group:
            camera.apply(sprite)

        # Отрисока курсора
        screen.blit(cursor, (mx - 20, my - 20))
        # отрисовка кнопки над персонажем, если он входит в зону перехода
        if pygame.sprite.spritecollideany(hero, exit_zone):
            hx, hy = hero.pos()
            screen.blit(E_button, (hx + 15, hy - 40))

        # отрисовка рамки и полоски для реакции
        pygame.draw.rect(screen, (200, 200, 200),
                         (infoObject.current_w // 2 - 295, infoObject.current_h - 130, 30, 120), 2)
        reaction_group.update()
        reaction_group.draw(screen)

        # обновление экрана
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
