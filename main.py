import pygame
import sys
import os
import random
import math

pygame.init()

TIMER_EVENT_TYPE = 30
CYAN = (54, 255, 247)

a_move_Flag = False
d_move_Flag = False  # Флаги передвижения
last_button = 'd'
money = 100
shop_flag = False  # Флаг нахождения рядом с магазином
cur_page = 1  # Переменные для страниц в магазине
max_page = 1
shop_openned = False  # Флаг открытого магазина

cur_wood_hp = 1000  # Переменные прочности дерева
max_wood_hp = 1000
wood_value = 50  # Сколько монет выпадает после срубки дерева

coin_value = 1  # Ценность монеты
add_coin_chance = 0  # Вероятность выпадения дополнительной монеты
more_value_coin_chance = 0  # Вероятность выпадения более ценной монеты
crit_chance = 0  # Вероятность крита (крит. удар повторяется дважды)
auto_hit = 0  # Сколько монет в секунду добывается автоматически
hit_cnt = 0  # Счетчик ударов (для гарантированных критов)
hit_dmg = 1  # Урон от удара

# Апгрейд записывается следующим образом: [Название, описание, цена, максимальный ранг улучшения, текущий ранг
# улучшения, требуемые улучшения в виде кортежа индексов этих улучшений в upgrades (None, если требований нет)]

upgrades = [['Ценная древесина', '+1 к ценности монет.', 50, 5, 1, None],  # 0
            ['Продажа оптом', '+10% шанс на выпадение доп. монеты.', 100, 10, 1, None],  # 1
            ['Авто-рубка', 'Вы добываете +1/сек. монету, находясь рядом с деревом.', 250, 5, 1, (0, 1)],  # 2
            ['Деревообработка', '+10% шанс на выпадение более ценной монеты.', 300, 5, 1, (0, 1)],  # 3
            ['Широкий замах', '+5% шанс нанести крит. удар (удвоение монет).', 450, 5, 1, (0, 1)],  # 4
            ['Точные удары', 'Каждая 10 атака с шансом 50% + 10% будет критической.', 650, 3, 1, (0, 1, 2, 3)],  # 5
            ['Заточка топора', 'Вы наносите +1 урона по дереву.', 150, 10, 1, None],  # 6
            ['Железное лезвие', 'Вы наносите +15 урона по дереву', 2000, 2, 1, (0, 1, 2, 3, 5)],  # 7
            ['Алмазное лезвие', 'Вы наносите +25 урона по дереву', 5000, 2, 1, (0, 1, 2, 3, 4, 5, 6)],  # 8
            ['Огромные деревья', 'Вы получаете на 50 монет больше за срубку дерева.', 3000, 4, 1, (0, 1, 2, 3, 4, 5)],
            # 9
            ]
upgrades_done = set()  # Сделанные улучшения
upgrades_full = set()  # Полностью законченные улучшения


def load_image(name, colorkey=None):
    fullname = os.path.join('jpg sprites', name)  # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Woodcutter(pygame.sprite.Sprite):  # Класс дровосека
    image = pygame.image.load('jpg sprites/woodcutter.png')

    def __init__(self, pos):
        super().__init__()
        self.image = Woodcutter.image
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.move_delay = 5
        pygame.time.set_timer(TIMER_EVENT_TYPE, self.move_delay)

    def move(self):  # Функция передвижения, за границы экрана выходить нельзя
        if a_move_Flag:
            if self.rect.x > -10:
                self.rect.x -= 2

        if d_move_Flag:
            if self.rect.x < 1130:
                self.rect.x += 2

    def flip_img(self):  # Функция поворота при движении в противоположную сторону (вызываетя из игрового цикла)
        self.image = pygame.transform.flip(self.image, True, False)


class Wood(pygame.sprite.Sprite):  # Класс дерева
    image = load_image('wood.jpg', colorkey=CYAN)

    def __init__(self, pos):
        super().__init__()
        self.image = Wood.image
        self.image = pygame.transform.scale(self.image, (150, 700))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.auto_hit_delay = 1000
        pygame.time.set_timer(TIMER_EVENT_TYPE + 1, self.auto_hit_delay)  # Таймер авто-добычи

    def clicked(self):  # Функция клика по дереву (спавн монет, отнятие хп у дерева)
        global cur_wood_hp
        global max_wood_hp
        global hit_dmg
        global wood_value
        if 350 <= cutter.rect.x <= 750:
            coin = GoldCoin((random.randrange(540, 580), random.randrange(350, 400)))
            all_sprites.add(coin)
            coins_list.add(coin)
            cur_wood_hp -= hit_dmg
            if cur_wood_hp <= 0:
                for i in range(wood_value):
                    coin = GoldCoin((random.randrange(540, 580), random.randrange(350, 400)))
                    all_sprites.add(coin)
                    coins_list.add(coin)
                max_wood_hp += 250
                cur_wood_hp = max_wood_hp


class WoodHpBar(pygame.sprite.Sprite):  # Класс полоски прочности дерева
    image = pygame.image.load('jpg sprites/wood_hp_icon.png')
    green_bg = pygame.image.load('jpg sprites/wood_hp_bg.png')

    def __init__(self, pos):
        super().__init__()
        self.image = WoodHpBar.image
        self.image = pygame.transform.scale(self.image, (220, 90))
        self.bg = WoodHpBar.green_bg
        self.bg = pygame.transform.scale(self.image, (220, 90))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):  # Обновление полоски
        global cur_wood_hp
        global max_wood_hp

        hp_font = pygame.font.SysFont('Comic Sans MS', 16)
        textsurface_hp = hp_font.render(str(cur_wood_hp) + '/' + str(max_wood_hp), False, (0, 0, 0))

        pygame.draw.rect(screen, (40, 157, 20), (510, 47, 160 * (cur_wood_hp / max_wood_hp), 40))
        screen.blit(textsurface_hp, (555, 55))
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pass


class Earth(pygame.sprite.Sprite):  # Класс земли (просто картинка)
    image = load_image('earth.jpg', colorkey=CYAN)

    def __init__(self, pos):
        super().__init__()
        self.image = Earth.image
        self.image = pygame.transform.scale(self.image, (1200, 100))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class GoldCoin(pygame.sprite.Sprite):  # Класс монетки
    image_coin1 = pygame.image.load('jpg sprites/coin1.png')
    image_coin2 = pygame.image.load('jpg sprites/coin2.png')
    image_coin3 = pygame.image.load('jpg sprites/coin3.png')

    def __init__(self, pos):
        global coin_value
        super().__init__()
        self.num_more = random.randint(1, 10)
        self.set_image()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.x_vel = random.randrange(-5, 5)
        self.y_vel = random.randrange(4, 9)

    def update(self):
        global more_value_coin_chance
        global coin_value
        global money
        if self.earth_collide(earth_back):  # Монета останавливается при контакте с землей
            self.y_vel = 0
            self.x_vel = 0
        if self.player_collide(cutter):
            money += coin_value
            if self.num_more <= more_value_coin_chance:  # Если шанс сработал, монета стоит дороже
                money += 1
            self.kill()  # Уничтожение монеты при контакте с игроком
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel  ## Полет монеты

    def set_image(self):  # Картинка монеты определяется ее ценностью (на данный момент есть 3 вида)
        global coin_value
        global more_value_coin_chance
        coin_val = coin_value
        if self.num_more <= more_value_coin_chance:
            coin_val += 1
        if coin_val == 1:
            self.image = GoldCoin.image_coin1
            self.image = pygame.transform.scale(self.image, (30, 30))
        elif coin_val == 2:
            self.image = GoldCoin.image_coin2
            self.image = pygame.transform.scale(self.image, (25, 35))
        else:
            self.image = GoldCoin.image_coin3
            self.image = pygame.transform.scale(self.image, (40, 40))

    def earth_collide(self, earth):
        return pygame.sprite.collide_mask(self, earth)

    def player_collide(self, player):
        return pygame.sprite.collide_mask(self, player)


class GoldenChest(pygame.sprite.Sprite):  # Класс сундука (магазина)
    image = pygame.image.load('jpg sprites/golden_chest.png')

    def __init__(self, pos):
        super().__init__()
        self.image = GoldenChest.image
        self.image = pygame.transform.scale(self.image, (112, 75))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def open_shop(self):  # Если игрок рядом с сундуком, ставит флаг магазина на true
        global shop_flag
        if 25 <= cutter.rect.x <= 175:
            shop_flag = True
        else:
            shop_flag = False


class Button(pygame.sprite.Sprite):  # Общий класс всех кнопок
    def __init__(self, pos, img, scale_pos):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, scale_pos)
        self.rect = self.image.get_rect()
        self.setCords(pos)

    def setCords(self, pos):
        self.rect.topleft = pos

    def pressed(self, mouse):  # Функция нажатия на кнопку
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


class UpgradeMenuButton(Button):  # Класс кнопки магазина (в правом верхнем углу)
    def __init__(self, pos):
        super().__init__(pos, 'jpg sprites/upgrade_menu_button_scroll.png', (46, 60))

    def open_menu(self):  # Вызывается при клике на кнопку, ставит флаг открытия магазина на true
        global shop_openned
        shop_openned = True


class UpgradeButton(Button):  # Класс кнопки улучшения
    def __init__(self, pos, upgrade, upg_index):
        super().__init__(pos, 'jpg sprites/upgrade_button_background.png', (200, 75))
        self.name = upgrade[0]
        self.desc = upgrade[1]
        self.cost = upgrade[2] * upgrade[4]  # Цена равна изначальной, помноженной на текущий ранг улучшения
        self.cur_rank = upgrade[4]
        self.upg_index = upg_index
        upg_name_font = pygame.font.SysFont('Comic Sans MS', 18)
        upg_desc_font = pygame.font.SysFont('Comic Sans MS', 12)
        upg_cost_font = pygame.font.SysFont('Comic Sans MS', 15)
        upg_name_font.set_bold(True)
        upg_cost_font.set_bold(True)

        textsurface_name = upg_name_font.render(str(self.name), False, (0, 0, 0))
        textsurface_cost = upg_cost_font.render(str(self.cost), False, (0, 0, 0))
        textsurface_rank = upg_name_font.render(str(self.cur_rank), False, (0, 0, 0))

        self.image.blit(textsurface_name, (17, 0))
        self.image.blit(textsurface_cost, (162, 22))
        self.image.blit(textsurface_rank, (165, 45))
        self.blit_text(text=self.desc, pos=(15, 20), font=upg_desc_font)

    def upgrade(self):  # Функция обновления всех показателей
        global money
        if money >= self.cost:
            money -= self.cost
            upgrades[self.upg_index][4] += 1
            self.cost = upgrades[self.upg_index][2] * upgrades[self.upg_index][4]
            self.global_up()

    def global_up(self):  # Функция улучшения
        global coin_value
        global add_coin_chance
        global auto_hit
        global crit_chance
        global more_value_coin_chance
        global guarnt_crit
        global hit_dmg
        global wood_value
        # Ниже идет проверка по индексу и само улучшения глобального параметра
        if self.upg_index == 0:
            upgrades_done.add(0)
            coin_value += 1
        if self.upg_index == 1:
            upgrades_done.add(1)
            add_coin_chance += 1
        if self.upg_index == 2:
            upgrades_done.add(2)
            auto_hit += 1
        if self.upg_index == 3:
            upgrades_done.add(3)
            more_value_coin_chance += 1
        if self.upg_index == 4:
            upgrades_done.add(4)
            crit_chance += 1
        if self.upg_index == 5:
            upgrades_done.add(5)
            guarnt_crit = 5 + upgrades[self.upg_index][4]
        if self.upg_index == 6:
            upgrades_done.add(6)
            hit_dmg += 1
        if self.upg_index == 7:
            upgrades_done.add(7)
            hit_dmg += 15
        if self.upg_index == 8:
            upgrades_done.add(8)
            hit_dmg += 25
        if self.upg_index == 9:
            upgrades_done.add(9)
            wood_value += 50

    def blit_text(self, text, pos, font, color=pygame.Color('black')):  # Функция переноса текста (взял с форума)
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.image.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width - 35:
                    x = pos[0]  # Reset the x.
                    y += word_height - 3  # Start on new row.
                self.image.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.


class UpgradeMenu(pygame.sprite.Sprite):  # Класс меню улучшений
    image = pygame.image.load('jpg sprites/scroll_background.png')

    def __init__(self, pos):
        global cur_page
        global max_page
        super().__init__()
        self.image = UpgradeMenu.image
        self.image = pygame.transform.scale(self.image, (300, 600))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.page1 = pygame.sprite.Group()
        self.page2 = pygame.sprite.Group()
        self.page3 = pygame.sprite.Group()

        self.pages = [self.page1, self.page2, self.page3]

    def fill_with_upgrades(self):  # Функция заполнения меню возможными улучшениями
        global max_page
        count = 0
        pg = 1
        required_ok = True  # Флаг доступности улучшения
        req_ok_upgrades = 0
        for upg in upgrades:
            if upg[4] < upg[3]:  # Если текущий ранг улучшения меньше максимального
                if upg[5] is not None:  # Если у улучшения есть требования
                    for i in upg[5]:
                        if i not in upgrades_done:  # Если ребования не соблюдены
                            required_ok = False
                            break
                    if required_ok:  # Если все требования соблюдены
                        new_upg = UpgradeButton((50, 75 + 80 * count), upg, upgrades.index(upg))
                        exec('self.page' + str(pg) + '.add(new_upg)')
                        count += 1
                        if count == 5:
                            count = 0
                            pg += 1
                        req_ok_upgrades += 1

                else:  # Если требований нет
                    new_upg = UpgradeButton((50, 75 + 80 * count), upg, upgrades.index(upg))
                    exec('self.page' + str(pg) + '.add(new_upg)')
                    count += 1
                    if count == 5:
                        count = 0
                        pg += 1
                    req_ok_upgrades += 1
            else:  # Если ранг достиг максимального
                upgrades_full.add(upgrades.index(upg))
        max_page = math.ceil(req_ok_upgrades / 5)  # Определяет максимальную страницу в магазине

    def update(self):  # Функция обновления
        global shop_openned
        global cur_page
        global max_page
        if not shop_flag:  # Если игрок отошел от магазина, меню закрывается
            shop_openned = False
        if shop_openned:
            for page in self.pages:
                for upg in page:
                    upg.kill()  # Уничтожает все кнопки
            self.image = UpgradeMenu.image  # Перерисовывает меню
            self.image = pygame.transform.scale(self.image, (300, 600))
            self.fill_with_upgrades()  # Заполняет меню заново

            page_font = pygame.font.SysFont('Comic Sans MS', 15)
            page_font.set_bold(True)
            textsurface_page = page_font.render(str(cur_page) + '/' + str(max_page), False, (0, 0, 0))
            self.image.blit(textsurface_page, (140, 25))  # Отображает текущую страницу/максимальную страницу

            exec('self.page' + str(cur_page) + '.draw(self.image)')

    def clicked(self, mouse_pos):  # Функция клика по кнопке улучшения
        x = mouse_pos[0] - 900
        y = mouse_pos[1]
        n_pos = (x, y)
        for i in range(len(self.pages)):
            if i + 1 == cur_page:
                for upg_but in self.pages[i].spritedict:
                    if upg_but.pressed(n_pos):
                        upg_but.upgrade()


class ArrowButton(Button):  # Класс стрелок, переключающих страницу
    def __init__(self, pos, direction):
        super().__init__(pos, 'jpg sprites/arrow_button.png', (35, 35))
        self.direct = direction
        if self.direct == 'left':  # Отражает картинку по горизонтали для левой стрелки
            self.image = pygame.transform.flip(self.image, True, False)

    def shift_page(self):  # Фукнция переключения страниц
        global cur_page
        global max_page
        if self.direct == 'left':
            if cur_page > 1:
                cur_page -= 1
        else:
            if cur_page < max_page:
                cur_page += 1

    def update(self):
        if not shop_flag:
            pass


size = width, height = 1200, 800

all_sprites = pygame.sprite.Group()
coins_list = pygame.sprite.Group()
shop_sprites = pygame.sprite.Group()
upg_menu_but = UpgradeMenuButton((1128, 15))
screen = pygame.display.set_mode(size)
arrow_sprites = pygame.sprite.Group()

cutter = Woodcutter((350, 600))
resource_wood = Wood((500, 0))
earth_back = Earth((0, 700))
golden_chest = GoldenChest((100, 626))
wood_durability = WoodHpBar((450, 20))

upg_menu = UpgradeMenu((900, 0))

left_arr = ArrowButton((943, 15), 'left')
right_arr = ArrowButton((1122, 15), 'right')

gold_icon = pygame.image.load('jpg sprites/coin1.png')
gold_icon = pygame.transform.scale(gold_icon, (35, 35))
gold_icon_rect = gold_icon.get_rect()
gold_icon_rect.x = 25
gold_icon_rect.y = 30

myfont = pygame.font.SysFont('Comic Sans MS', 30)

all_sprites.add(golden_chest)
all_sprites.add(resource_wood)
all_sprites.add(cutter)
all_sprites.add(earth_back)
all_sprites.add(wood_durability)

arrow_sprites.add(upg_menu)
arrow_sprites.add(left_arr)
arrow_sprites.add(right_arr)
shop_sprites.add(upg_menu_but)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # Передвижение
            if event.key == pygame.K_a:
                a_move_Flag = True
                if last_button == 'd':
                    cutter.flip_img()
                last_button = 'a'
            elif event.key == pygame.K_d:
                d_move_Flag = True
                if last_button == 'a':
                    cutter.flip_img()
                last_button = 'd'
        if event.type == pygame.KEYUP:  # Передвижение
            if event.key == pygame.K_a:
                a_move_Flag = False
            elif event.key == pygame.K_d:
                d_move_Flag = False
        if event.type == pygame.MOUSEBUTTONUP:  # Клики
            pos = pygame.mouse.get_pos()
            if resource_wood.rect.collidepoint(pos):  # Клик по дереву
                num_add = random.randint(1, 10)
                num_crit = random.randint(1, 10)
                hit_cnt += 1
                if hit_cnt == 10:
                    hit_cnt = 0
                    num_crit = 0
                iter = 1
                if num_add <= add_coin_chance:
                    iter += 1
                if num_crit <= crit_chance:
                    iter *= 2
                for i in range(iter):
                    resource_wood.clicked()
            if shop_flag:
                if upg_menu_but.pressed(pos):  # Кнопка меню
                    upg_menu_but.open_menu()
                if left_arr.pressed(pos):  # Стрелки
                    left_arr.shift_page()
                if right_arr.pressed(pos):
                    right_arr.shift_page()
                if upg_menu.rect.collidepoint(
                        pos):  # Клик в пределах меню, функция определяет, был ли клик по кнопке улучшения
                    upg_menu.clicked(pos)

        if event.type == TIMER_EVENT_TYPE:  # Общеигровой таймер
            cutter.move()  # Передвижение
            golden_chest.open_shop()  # Проверка нахождения игрока рядом с магазином

        if event.type == TIMER_EVENT_TYPE + 1:  # Таймер авто-добычи
            if auto_hit >= 1:
                for i in range(auto_hit):
                    resource_wood.clicked()

    screen.fill(pygame.Color(CYAN))  # Отрисовка
    all_sprites.draw(screen)
    if shop_flag:
        shop_sprites.draw(screen)
    if shop_openned:
        arrow_sprites.draw(screen)

    screen.blit(gold_icon, gold_icon_rect)
    textsurface_gold = myfont.render(str(money), False, (0, 0, 0))
    screen.blit(textsurface_gold, (70, 25))

    all_sprites.update()  # Обновление
    shop_sprites.update()
    arrow_sprites.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()  # Выход :)
