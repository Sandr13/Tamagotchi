import time
import pygame
import math
import functions

pygame.init()  # Инициализация pygame

############################# Параметры экрана #############################
display_width = 1400
display_height = 700
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("My Walker")
clock = pygame.time.Clock()  # Переменная для подсчёта тиков

############################# Класс объекта-игрока ##############################
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\\knight\\front.png')
        self.rect = self.image.get_rect()
        self.rect.center = (display_width / 2, display_height / 2)
        self.hp = 5
        self.items = []

############################# Класс инвентаря ##############################
class Inventory:
    def __init__(self):
        self.items = []

############################# Класс объекта-бара хп ##############################
class Bar_HP(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\\health\\5.png')
        self.rect = self.image.get_rect()
        self.rect.center = (1215,675)

################################ Класс Противника ##################################
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\\enemy\\ghost_left.png')
        self.rect = self.image.get_rect()
        self.speed = 2

################################ Класс ячейки инвентаря ##################################
class Ceil_of_inventory(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\\inventory\\ceil_of_inventory.png')
        self.rect = self.image.get_rect()
        self.is_empty = True


################################ Класс места для предмета в ячейке инвентаря ##################################
class Place_for_item_in_ceil(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\\inventory\\items\\empty_slot.png')
        self.rect = self.image.get_rect()

################################ Класс сундука ##################################
class Chest(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\\objects\\chest.png')
        self.rect = self.image.get_rect()

############################# Класс гозизонтальной стены ##############################
class Wall_Horizontal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\\level elements\\wall.png')
        self.rect = self.image.get_rect()

############################# Класс вертикальной стены ##############################
class Wall_Vertical(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\\level elements\\wall.png')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, 90)

############################# Класс хилки ##############################
class Heal_bottle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/inventory/items/heal_bottle.png')
        self.rect = self.image.get_rect()
        self.name = 'heal_bottle'

############################# Класс лука ##############################
class Bow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/inventory/items/bow.png')
        self.rect = self.image.get_rect()
        self.name = 'bow'

############################# Класс снаряда ##############################
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\\attacking\\arrow.png')
        self.rect = self.image.get_rect()
        self.direction = 0

################################ Класс заднего фона ##################################
class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\\level elements\\background-1.png')
        self.rect = self.image.get_rect()
        self.index_of_room = 1

    def change_the_room(self, count_of_room):
        directory = 'resources\\level elements\\background-' + str(count_of_room + 1) + '.png'
        self.image = pygame.image.load(directory)

def run_game():   # Основная функция игры
    game = True
    first = True

    ############################# Создаём группы объектов на карте ##############################
    all_sprites = pygame.sprite.Group()  # Группа спрайтов
    walls = pygame.sprite.Group()   # Группа стен
    all_enemy = pygame.sprite.Group()  # Группа монстров
    all_items_ont_the_ground = pygame.sprite.Group()   # Группа предметов на земле
    all_bullets = pygame.sprite.Group()   # Группа снарядов

    ############################# Задний фон ##############################
    background = Background()
    all_sprites.add(background)

    ############################# Сундуки ##############################
    def generate_chests():
        chest = Chest()  # Создаём сундук
        all_sprites.add(chest)
        chests.add(chest)
        chest.rect.center = (500, 100)

    ############################# Игрок ##############################
    user = Player()   # Создаём игрока
    all_sprites.add(user)

    ############################# Стрельба ##############################
    def bullet_move(arrow, direction):
        if direction == 'right':
            if arrow.rect.right <= display_width - 50:
                arrow.rect.right += 1
        elif direction == 'left':
            if arrow.rect.left >= 50:
                arrow.rect.right += 1
        elif direction == 'top':
            if arrow.rect.top >= 50:
                arrow.rect.right += 1
        elif direction == 'bottom':
            if arrow.rect.bottom <= display_height - 50:
                arrow.rect.right += 1

    def shoot():
        can_we_shoot = False
        for item in user.items:
            if item == 'bow':
                can_we_shoot = True
        if can_we_shoot:
            arrow = Bullet()
            all_sprites.add(arrow)
            all_bullets.add(arrow)
            arrow.rect.center = user.rect.center
            if right:
                arrow.direction = 'right'
            elif left:
                arrow.direction = 'left'
            elif back:
                arrow.direction = 'top'
            elif front:
                arrow.direction = 'bottom'

        # bullet_move(arrow, direction)

    ############################# Предметы ##############################
    def generate_items():
        number_of_items = functions.chanse_to_spawn_the_enemy()

        for i in range(number_of_items):
            type = functions.check_for_item(['heal_bottle', 'bow'])
            if type == 'heal_bottle':
                item = Heal_bottle()
            elif type == 'bow':
                item = Bow()

            all_sprites.add(item)
            all_items_ont_the_ground.add(item)
            item.rect.center = functions.random_position_of_spawn(display_width, display_height)

    ############################# Противники ##############################
    def generate_ghosts():
        number_of_enemy = functions.chanse_to_spawn_the_enemy()
        for i in range(number_of_enemy):
            ghost = Enemy()
            all_sprites.add(ghost)
            all_enemy.add(ghost)
            ghost.rect.center = functions.random_position_of_spawn(display_width, display_height)

    ############################# Генерация противников ##############################
    generate_ghosts()
    ############################# Генерация предметов ##############################
    generate_items()
    ############################# Создаём стены ##############################
    wall_top_1 = Wall_Horizontal()
    all_sprites.add(wall_top_1)
    walls.add(wall_top_1)
    wall_top_1.rect.left = 0

    wall_top_2 = Wall_Horizontal()
    all_sprites.add(wall_top_2)
    walls.add(wall_top_2)
    wall_top_2.rect.left = 350

    wall_top_3 = Wall_Horizontal()
    all_sprites.add(wall_top_3)
    walls.add(wall_top_3)
    wall_top_3.rect.left = 1050

    wall_top_4 = Wall_Horizontal()
    all_sprites.add(wall_top_4)
    walls.add(wall_top_4)
    wall_top_4.rect.left = 0
    wall_top_4.rect.bottom = display_height

    wall_top_5 = Wall_Horizontal()
    all_sprites.add(wall_top_5)
    walls.add(wall_top_5)
    wall_top_5.rect.left = 750
    wall_top_5.rect.bottom = display_height

    wall_top_6 = Wall_Horizontal()
    all_sprites.add(wall_top_6)
    walls.add(wall_top_6)
    wall_top_6.rect.left = 1050
    wall_top_6.rect.bottom = display_height

    wall_top_7 = Wall_Vertical()
    all_sprites.add(wall_top_7)
    walls.add(wall_top_7)
    wall_top_7.rect.top = -150

    wall_top_8 = Wall_Vertical()
    all_sprites.add(wall_top_8)
    walls.add(wall_top_8)
    wall_top_8.rect.top = 500

    wall_top_9 = Wall_Vertical()
    all_sprites.add(wall_top_9)
    walls.add(wall_top_9)
    wall_top_9.rect.top = -150
    wall_top_9.rect.right = 1700

    wall_top_10 = Wall_Vertical()
    all_sprites.add(wall_top_10)
    walls.add(wall_top_10)
    wall_top_10.rect.right = 1700
    wall_top_10.rect.top = 500

    ############################# Бар-хп ##############################
    bar = Bar_HP()   # бар
    all_sprites.add(bar)
    index_of_room = 0
    count_of_room = 1

    ############################# Инвентарь ##############################
    inventory = Inventory()

    block_1 = Ceil_of_inventory()
    all_sprites.add(block_1)
    block_1.rect.center = (75,25)
    inventory.items.append(block_1)

    empty_1 = Place_for_item_in_ceil()
    all_sprites.add(empty_1)
    empty_1.rect.center = (75,25)


    block_2 = Ceil_of_inventory()
    all_sprites.add(block_2)
    block_2.rect.center = (125,25)
    inventory.items.append(block_2)

    empty_2 = Place_for_item_in_ceil()
    all_sprites.add(empty_2)
    empty_2.rect.center = (125, 25)


    block_3 = Ceil_of_inventory()
    all_sprites.add(block_3)
    block_3.rect.center = (175,25)
    inventory.items.append(block_3)

    empty_3 = Place_for_item_in_ceil()
    all_sprites.add(empty_3)
    empty_3.rect.center = (175, 25)


    block_4 = Ceil_of_inventory()
    all_sprites.add(block_4)
    block_4.rect.center = (225,25)
    inventory.items.append(block_4)

    empty_4 = Place_for_item_in_ceil()
    all_sprites.add(empty_4)
    empty_4.rect.center = (225, 25)


    block_5 = Ceil_of_inventory()
    all_sprites.add(block_5)
    block_5.rect.center = (275,25)
    inventory.items.append(block_5)

    empty_5 = Place_for_item_in_ceil()
    all_sprites.add(empty_5)
    empty_5.rect.center = (275, 25)

    while game:   # Пока сеанс игры запущен:
        for event in pygame.event.get():   # Считываем все события
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot()

        keys = pygame.key.get_pressed()   # Инициализируем клавиатуру
        ############################# Стрельба ##############################


        ############################# Движение игрока ##############################

        ghost_right = True   # Напривления, куда смотрит призрак
        ghost_left = False

        if first:
            back = False   # Направления, куда смотрит игрок
            front = True
            right = False
            left = False

            first = False

        if keys[pygame.K_w] and keys[pygame.K_a]:
            if user.rect.x <= 50 and 200 <= user.rect.y <= 205:
                pass
            elif user.rect.right >= display_width - 50 and 300 <= user.rect.bottom <= 500:
                pass
            elif 339 <= user.rect.left <= 350 and user.rect.bottom > 650:
                pass
            elif 700 <= user.rect.x <= 705 and user.rect.top < 50:
                pass
            elif user.rect.left <= -100 and 200 <= user.rect.y <= 400 and index_of_room == 1:
                pass
            elif user.rect.top <= -100 and 700 <= user.rect.x <= 975 and index_of_room == 4:
                pass
            else:
                user.rect.y -= 2
                user.rect.x -= 2
        elif keys[pygame.K_w]:
            if user.rect.x <= 50 and 200 <= user.rect.y <= 205:
                pass
            elif user.rect.right >= display_width - 50 and 200 <= user.rect.y <= 205:
                pass
            elif user.rect.top <= -100 and 700 <= user.rect.x <= 975 and index_of_room == 4:
                pass
            else:
                user.rect.y -= 4
                back = True
                front = False
                right = False
                left = False
        elif keys[pygame.K_a]:
            if 339 <= user.rect.left <= 350 and user.rect.bottom > 650:
                pass
            elif 700 <= user.rect.x <= 705 and user.rect.top < 50:
                pass
            elif user.rect.left <= -100 and 200 <= user.rect.y <= 400 and index_of_room == 1:
                pass
            else:
                user.rect.x -= 4
                back = False
                front = False
                right = False
                left = True

        if keys[pygame.K_w] and keys[pygame.K_d]:
            if user.rect.x <= 50 and 200 <= user.rect.y <= 205:
                pass
            elif user.rect.right >= display_width - 50 and 200 <= user.rect.y <= 205:
                pass
            elif 669 <= user.rect.x <= 675 and user.rect.bottom > 650:
                pass
            elif 970 <= user.rect.x <= 975 and user.rect.top < 50:
                pass
            elif user.rect.right > display_width + 100 and 200 <= user.rect.y <= 400 and index_of_room == 2:
                pass
            elif user.rect.top <= -100 and 700 <= user.rect.x <= 975 and index_of_room == 4:
                pass
            else:
                user.rect.y -= 2
                user.rect.x += 2
        elif keys[pygame.K_w]:
            if user.rect.x <= 50 and 200 <= user.rect.y <= 205:
                pass
            elif user.rect.right >= display_width - 50 and 200 <= user.rect.y <= 205:
                pass
            elif user.rect.top <= -100 and 700 <= user.rect.x <= 975 and index_of_room == 4:
                pass
            else:
                user.rect.y -= 4
                back = True
                front = False
                right = False
                left = False
        elif keys[pygame.K_d]:
            if 669 <= user.rect.x <= 675 and user.rect.bottom > 650:
                pass
            elif 970 <= user.rect.x <= 975 and user.rect.top < 50:
                pass
            elif user.rect.right > display_width + 100 and 200 <= user.rect.y <= 400 and index_of_room == 2:
                pass
            else:
                user.rect.x += 4
                back = False
                front = False
                right = True
                left = False

        if keys[pygame.K_d] and keys[pygame.K_s]:
            if user.rect.x <= 50 and 495 <= user.rect.bottom <= 500:
                pass
            elif user.rect.right >= display_width - 50 and 500 <= user.rect.bottom <= 505:
                pass
            elif 669 <= user.rect.x <= 675 and user.rect.bottom > 650:
                pass
            elif 970 <= user.rect.x <= 975 and user.rect.top < 50:
                pass
            elif user.rect.right > display_width + 100 and 200 <= user.rect.y <= 400 and index_of_room == 2:
                pass
            elif user.rect.bottom > display_height + 100 and 345 <= user.rect.x <= 675 and index_of_room == 3:
                pass
            else:
                user.rect.x += 2
                user.rect.y += 2
        elif keys[pygame.K_d]:
            if 669 <= user.rect.x <= 675 and user.rect.bottom > 650:
                pass
            elif 970 <= user.rect.x <= 975 and user.rect.top < 50:
                pass
            elif user.rect.right > display_width + 100 and 200 <= user.rect.y <= 400 and index_of_room == 2:
                pass
            else:
                user.rect.x += 4
                back = False
                front = False
                right = True
                left = False
        elif keys[pygame.K_s]:
            if user.rect.x <= 50 and 495 <= user.rect.bottom <= 500:
                pass
            elif user.rect.right >= display_width - 50 and 500 <= user.rect.bottom <= 505:
                pass
            elif user.rect.bottom > display_height + 100 and 345 <= user.rect.x <= 675 and index_of_room == 3:
                pass
            else:
                user.rect.y += 4
                back = False
                front = True
                right = False
                left = False
        if keys[pygame.K_s] and keys[pygame.K_a]:
            if user.rect.x <= 50 and 495 <= user.rect.bottom <= 500:
                pass
            elif user.rect.right >= display_width - 50 and 495 <= user.rect.bottom <= 501:
                pass
            elif 339 <= user.rect.left <= 350 and user.rect.bottom > 650:
                pass
            elif 700 <= user.rect.x <= 705 and user.rect.top < 50:
                pass
            elif user.rect.left <= -100 and 200 <= user.rect.y <= 400 and index_of_room == 1:
                pass
            elif user.rect.bottom > display_height + 100 and 345 <= user.rect.x <= 675 and index_of_room == 3:
                pass
            else:
                user.rect.y += 2
                user.rect.x -= 2
        elif keys[pygame.K_s]:
            if user.rect.x <= 50 and 490 <= user.rect.bottom <= 500:
                pass
            elif user.rect.right >= display_width - 50 and 500 <= user.rect.bottom <= 505:
                pass
            elif user.rect.bottom > display_height + 100 and 345 <= user.rect.x <= 675 and index_of_room == 3:
                pass
            else:
                user.rect.y += 4
                back = False
                front = True
                right = False
                left = False
        elif keys[pygame.K_a]:
            if 339 <= user.rect.left <= 350 and user.rect.bottom > 650:
                pass
            elif 700 <= user.rect.x <= 705 and user.rect.top < 50:
                pass
            elif user.rect.left <= -100 and 200 <= user.rect.y <= 400 and index_of_room == 1:
                pass
            else:
                user.rect.x -= 4
                back = False
                front = False
                right = False
                left = True

        ############################# Границы карты ##############################
        if user.rect.right > display_width - 50:
            if 200 <= user.rect.y <= 400:
                pass
            else:
                user.rect.right = display_width - 50
        if user.rect.left < 50:
            if 200 <= user.rect.y <= 400:
                pass
            else:
                user.rect.left = 50
        if user.rect.top < 50:
            if 700 <= user.rect.x <= 975:
                pass
            else:
                user.rect.top = 50
        if user.rect.bottom > display_height - 50:
            if 345 <= user.rect.x <= 675:
                pass
            else:
                user.rect.bottom = display_height - 50

        ############################# Смена уровня ##############################
        def pause():
            #pygame.time.delay(500)
            pass
        if user.rect.right >= display_width + 150:
            user.rect.left = -100
            index_of_room = 1
            pause()
            count_of_room += 1
            count_of_room %= 4
            background.change_the_room(count_of_room)
            for sprite in all_enemy:
                sprite.kill()
            for sprite in all_items_ont_the_ground:
                sprite.kill()
            for sprite in all_bullets:
                sprite.kill()
            generate_ghosts()
            generate_items()


        elif user.rect.left <= -150:
            user.rect.right = display_width + 100
            index_of_room = 2
            pause()
            count_of_room += 1
            count_of_room %= 4
            background.change_the_room(count_of_room)
            for sprite in all_enemy:
                sprite.kill()
            for sprite in all_items_ont_the_ground:
                sprite.kill()
            for sprite in all_bullets:
                sprite.kill()
            generate_ghosts()
            generate_items()

        elif user.rect.top <= -150:
            user.rect.bottom = display_height + 100
            user.rect.x = 500
            index_of_room = 3
            pause()
            count_of_room += 1
            count_of_room %= 4
            background.change_the_room(count_of_room)
            for sprite in all_enemy:
                sprite.kill()
            for sprite in all_items_ont_the_ground:
                sprite.kill()
            for sprite in all_bullets:
                sprite.kill()
            generate_ghosts()
            generate_items()

        elif user.rect.bottom >= display_height + 150:
            user.rect.top = -100
            user.rect.x = 835
            index_of_room = 4
            pause()
            count_of_room += 1
            count_of_room %= 4
            background.change_the_room(count_of_room)
            for sprite in all_enemy:
                sprite.kill()
            for sprite in all_items_ont_the_ground:
                sprite.kill()
            for sprite in all_bullets:
                sprite.kill()
            generate_ghosts()
            generate_items()

        for bullet in all_bullets:
            ### Направление движения ###
            if bullet.direction == 'right':
                if bullet.rect.right <= display_width - 50:
                    bullet.rect.right += 5
                else:
                    bullet.kill()
            elif bullet.direction == 'left':
                if bullet.rect.left >= 50:
                    bullet.rect.left -= 5
                else:
                    bullet.kill()
            elif bullet.direction == 'top':
                if bullet.rect.top >= 50:
                    bullet.rect.top -= 5
                else:
                    bullet.kill()
            elif bullet.direction == 'bottom':
                if bullet.rect.bottom <= display_height - 50:
                    bullet.rect.bottom += 5
                else:
                    bullet.kill()

            if pygame.sprite.spritecollide(bullet, all_enemy, True):
                #bullet.remove(all_bullets)
                bullet.kill()

        ############################# Движение Призрака ##############################
        for ghost in all_enemy:
            if math.fabs(user.rect.center[0] - ghost.rect.center[0]) >= 50 or math.fabs(user.rect.center[1] - ghost.rect.center[1]) >= 50:
                if user.rect.x - ghost.rect.x > 0:
                    ghost.rect.x = ghost.rect.x + ghost.speed
                    ghost_right = True
                    ghost_left = False
                if user.rect.x - ghost.rect.x < 0:
                    ghost_right = False
                    ghost_left = True
                    ghost.rect.x = ghost.rect.x - ghost.speed

                if user.rect.y - ghost.rect.y > 0:
                    ghost.rect.y = ghost.rect.y + ghost.speed
                if user.rect.y - ghost.rect.y < 0:
                    ghost.rect.y = ghost.rect.y - ghost.speed
            else:
                count_of_detected_colide = len(pygame.sprite.spritecollide(user, all_enemy, True))
                user.hp -= count_of_detected_colide


            ############################# Отрисовка призрака ##############################
            if ghost_right:
                ghost.image = pygame.image.load('resources\enemy\ghost_right.png')
            elif ghost_left:
                ghost.image = pygame.image.load('resources\enemy\ghost_left.png')

        ############################# Предметы и взаимодействие с ними ##############################
        def pick_up():
            if len(user.items) < 5:
                list = pygame.sprite.spritecollide(user, all_items_ont_the_ground, True)
                for i in range(len(list)):
                    if len(user.items) < 5:
                        user.items.append(list[i].name)
                print_items()

        if pygame.sprite.spritecollide(user, all_items_ont_the_ground, False):
            pick_up()

        ############################# Отрисовка предметов из инвентаря ##############################
        def print_items():
            for i in range(5):
                inventory.items[i].is_empty = True

            for item in user.items:
                if item == 'heal_bottle':

                    directory = 'resources\\inventory\\items\\heal_bottle.png'

                    if inventory.items[0].is_empty:
                        empty_1.image = pygame.image.load(directory)
                        inventory.items[0].is_empty = False
                    elif inventory.items[1].is_empty:
                        empty_2.image = pygame.image.load(directory)
                        inventory.items[1].is_empty = False
                    elif inventory.items[2].is_empty:
                        empty_3.image = pygame.image.load(directory)
                        inventory.items[2].is_empty = False
                    elif inventory.items[3].is_empty:
                        empty_4.image = pygame.image.load(directory)
                        inventory.items[3].is_empty = False
                    elif inventory.items[4].is_empty:
                        empty_5.image = pygame.image.load(directory)
                        inventory.items[4].is_empty = False

                elif item == 'bow':
                    directory = 'resources\\inventory\\items\\bow.png'

                    if inventory.items[0].is_empty:
                        empty_1.image = pygame.image.load(directory)
                        inventory.items[0].is_empty = False
                    elif inventory.items[1].is_empty:
                        empty_2.image = pygame.image.load(directory)
                        inventory.items[1].is_empty = False
                    elif inventory.items[2].is_empty:
                        empty_3.image = pygame.image.load(directory)
                        inventory.items[2].is_empty = False
                    elif inventory.items[3].is_empty:
                        empty_4.image = pygame.image.load(directory)
                        inventory.items[3].is_empty = False
                    elif inventory.items[4].is_empty:
                        empty_5.image = pygame.image.load(directory)
                        inventory.items[4].is_empty = False

        ############################# Отрисовка игрока ##############################
        if front:
            user.image = pygame.image.load('resources\knight\\front.png')  # Переменная-картинка игрока
        elif back:
            user.image = pygame.image.load('resources\knight\\back.png')  # Переменная-картинка игрока
        elif right:
            user.image = pygame.image.load('resources\knight\\right.png')  # Переменная-картинка игрока
        elif left:
            user.image = pygame.image.load('resources\knight\\left.png')  # Переменная-картинка игрока

        ############################# Отрисовка hp игрока ##############################
        if user.hp == 5:
            bar.image = pygame.image.load('resources\\health\\5.png')
        elif user.hp == 4:
            bar.image = pygame.image.load('resources\\health\\4.png')
        elif user.hp == 3:
            bar.image = pygame.image.load('resources\\health\\3.png')
        elif user.hp == 2:
            bar.image = pygame.image.load('resources\\health\\2.png')
        elif user.hp == 1:
            bar.image = pygame.image.load('resources\\health\\1.png')
        elif user.hp <= 0:
            bar.image = pygame.image.load('resources\\health\\0.png')
            exit()

        all_sprites.update()   # Обновление спрайтов
        all_sprites.draw(display)  # Прорисовка всех спрайтов
        pygame.display.flip()   # Переворчиваем экран
        clock.tick(60)   # FPS


run_game()
