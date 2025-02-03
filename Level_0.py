from classes import *
from animate_func import load_animation_frames
from animate_func import load_cura_animation_frames
from Level0_minigame1 import minigame_main
import pygame
from strategy import example_strategy


# Размеры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 600


# Функция создания комнат
def create_rooms():
    rooms = {}

    # Комната 1
    room1_width, room1_height = 1600, 800
    room1_walls = [
        pygame.Rect(0, 0, 1600, 10),  # Верхняя стена
        pygame.Rect(0, 790, 1600, 10),  # Нижняя стена
        pygame.Rect(0, 0, 10, 350),  # Левая верхняя стена
        pygame.Rect(0, 450, 10, 350),  # Левая нижняя стена
        pygame.Rect(1590, 0, 10, 800)  # Правая стена
    ]
    room1_transitions = [
        {"rect": pygame.Rect(0, 350, 10, 100), "target": "room2", "player_start": (600, 400)}
    ]
    room1_objects = [
        GameObject('assets/decoration/Table.png', 800, 300)

    ]
    room1_npc = [
        NPC(800, 400, "assets/NPC_files/walk1.png")
    ]
    cura_idle_frames = load_cura_animation_frames("Cura", 1)  # 1 кадра для idle
    cura_run_frames = load_cura_animation_frames("Cura", 24)  # 24 кадра для run

    cura_animations = {
        "idle": cura_idle_frames,
        "run": cura_run_frames,
    }
    cura1 = Enemy(pygame.Rect((800, 400, 40, 40)), "Cura/Cura1.png", speed=3, health=50,
                 strategy=example_strategy,
                 animations=cura_animations)
    start_weapon1 = Weapon(5, 79, "Weapons/Bata.png", 5)
    cura2 = Enemy(pygame.Rect((700, 400, 40, 40)), "Cura/Cura1.png", speed=4, health=50,
                  strategy=example_strategy,
                  animations=cura_animations)
    start_weapon2 = Weapon(5, 79, "Weapons/Bata.png", 2)
    cura3 = Enemy(pygame.Rect((600, 400, 40, 40)), "Cura/Cura1.png", speed=2, health=50,
                  strategy=example_strategy,
                  animations=cura_animations)
    start_weapon3 = Weapon(5, 79, "Weapons/Bata.png", 10)
    Objects.enemies.append(cura1)
    Objects.enemies.append(cura2)
    Objects.enemies.append(cura3)
    cura1.get_weapon(start_weapon1)
    cura2.get_weapon(start_weapon2)
    cura3.get_weapon(start_weapon3)
    room1_enemies = [
        [[cura1, start_weapon1], False], [[cura2, start_weapon2], False], [[cura3, start_weapon3], False]
    ]
    room1_dialog = 'Привет игрок я хочу проверить умеешь ли ты ходить. Если готов начать проверку нажми да'
    rooms["room1"] = Room(room1_width, room1_height, "assets/rooms/room1.png", room1_walls,
                          room1_transitions, room1_objects, room1_npc, room1_enemies, room1_dialog)

    # Комната 2
    room2_width, room2_height = 800, 800
    room2_walls = [
        pygame.Rect(0, 0, 800, 10),  # Верхняя стена
        pygame.Rect(0, 790, 350, 10), # Нижняя стена вверх
        pygame.Rect(450, 790, 350, 10), # Нижняя стена низ
        pygame.Rect(0, 0, 10, 800),  # Левая стена
        pygame.Rect(790, 0, 10, 350),  # Правая верхняя стена
        pygame.Rect(790, 450, 10, 350),  # Правая нижняя стена
    ]
    room2_transitions = [
        {"rect": pygame.Rect(790, 350, 10, 100), "target": "room1", "player_start": (50, 400)},  # Вход из комнаты 1
        {"rect": pygame.Rect(350, 790, 100, 10), "target": "room3", "player_start": (500, 50)},  # Выход вниз
    ]
    rooms["room2"] = Room(room2_width, room2_height, "assets/rooms/room2.png", room2_walls, room2_transitions)

    # Комната 3
    room3_width, room3_height = 1000, 1000
    room3_walls = [
        pygame.Rect(0, 0, 450, 10),  # Верхняя стена вверх
        pygame.Rect(550, 0, 450, 10),  # Верхняя стена вверх
        pygame.Rect(0, 990, 450, 10),  # Нижняя стена
        pygame.Rect(550, 990, 450, 10),  # Нижняя стена
        pygame.Rect(0, 0, 10, 1000),  # Левая стена
        pygame.Rect(990, 0, 10, 1000),  # Правая стена
    ]
    room3_transitions = [
        {"rect": pygame.Rect(450, 0, 100, 10), "target": "room2", "player_start": (400, 700)}, # Вход сверху
        {"rect": pygame.Rect(450, 990, 100, 10), "target": "room4", "player_start": (550, 20)}  # Вход снизу
    ]
    rooms["room3"] = Room(room3_width, room3_height, "assets/rooms/room3.png", room3_walls, room3_transitions)

    # Комната 4
    room4_width, room4_height = 1100, 1000
    room4_walls = [
        pygame.Rect(0, 0, 500, 10), # Верхняя стена вверх
        pygame.Rect(600, 0, 500, 10), # Верхняя стена низ
        pygame.Rect(0, 990, 1100, 10), # Нижняя стена
        pygame.Rect(0, 0, 10, 1000),
        pygame.Rect(1090, 0, 10, 450),
        pygame.Rect(1090, 550, 10, 500)
    ]
    room4_transitions = [{"rect": pygame.Rect(1090, 450, 10, 100), "target": "room5", "player_start": (30, 600)},
                         {"rect": pygame.Rect(500, 0, 100, 10), "target": "room3", "player_start": (500, 900)}
                         ]
    rooms["room4"] = Room(room4_width, room4_height, "assets/rooms/room4.png", room4_walls, room4_transitions)

    # Комната 5
    room5_width, room5_height = 2000, 1200
    room5_walls = [
        pygame.Rect(0, 0, 2000, 10),  # Верхняя стена вверх
        pygame.Rect(0, 1190, 2000, 10),  # Нижняя стена
        pygame.Rect(0, 0, 10, 550),
        pygame.Rect(0, 650, 10, 550),
        pygame.Rect(1990, 0, 10, 1200),
        ((0, 790), (1600, 790))
    ]
    room5_transitions = [{"rect": pygame.Rect(0, 550, 10, 100), "target": "room4", "player_start": (1000, 500)}
                         ]
    rooms["room5"] = Room(room5_width, room5_height, "assets/rooms/room5.png", room5_walls, room5_transitions)
    return rooms


# Основной цикл игры
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Инициализация игрока и комнат
    idle_frames = load_animation_frames("assets/animate_hero", 11)  # 3 кадра для idle
    run_frames = load_animation_frames("assets/animate_hero", 1)  # 4 кадра для run

    animations = {
        "idle": idle_frames,
        "run": run_frames,
    }
    hero_hitbox = pygame.Rect(600, 400, 92, 75)
    hero_image = "assets/animate_hero/MairouMotion1.png"
    hero_speed = 10
    hero_health = 100
    Objects.hero = Hero(hero_hitbox, hero_image, hero_speed, hero_health, animations)
    hero_weapon = Weapon(5, 93, "Weapons/SantaliderSword.png", 3)
    Objects.hero.get_weapon(hero_weapon)

    rooms = create_rooms()
    current_room = "room1"

    Objects.hero.get_targets_to_weapon(rooms["room1"])
    camera = Camera(rooms[current_room].width, rooms[current_room].height)

    # Создаем НПС
    dialog_box = DialogBox(rooms[current_room].text)

    running = True
    cura_summoned = False
    cooldown_font = pygame.font.Font(None, 32)

    while running:
        # Обновление перезарядки
        delta_time = clock.get_time()
        Objects.hero.update_cooldowns(delta_time)

        # Обновление энергии игрока
        Objects.hero.regen_energy(delta_time)

        screen.fill((0, 0, 0))

        # Отрисовка интерфейса
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.display.set_caption("GoodGame")
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Рывок по Alt
                if event.key in (pygame.K_LALT, pygame.K_RALT):
                    # Проверяем возможность рывка
                    if Objects.hero.dash_cooldown <= 0:
                        Objects.hero.dash(rooms[current_room].walls, rooms[current_room].objects)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Проверяем, кликнули ли по НПС
                for npc in rooms[current_room].npc:
                    if npc.check_click(mouse_pos, camera):
                        dialog_box.visible = True
                        break
                    result = dialog_box.handle_click(mouse_pos)
                    if current_room == "room1" and result == 'yes':
                        npc.following = True
                        rooms[current_room].enemies[0][1] = True
                        rooms[current_room].enemies[1][1] = True
                        rooms[current_room].enemies[2][1] = True
                    if current_room == "room1" and rooms[current_room].check_object_click(mouse_pos, camera, "Table.png") and npc.following == True:
                        game_result = minigame_main()
                        if game_result:
                            pass

        # Движение игрока
        Objects.hero.move(keys, rooms[current_room].walls, rooms[current_room].objects, 0.15)
        Objects.hero.attack(keys)

        # Если НПС следует за игроком
        for npcs in rooms[current_room].npc:
            if npcs.following:
                npcs.rect.center = Objects.hero.rect.center

        # Проверка переходов между комнатами
        for transition in rooms[current_room].transitions:
            if transition["rect"].colliderect(Objects.hero.rect):
                current_room = transition["target"]
                Objects.hero.get_targets_to_weapon(rooms[current_room])
                Objects.hero.rect.topleft = transition["player_start"]
                Objects.hero.hitbox = (transition["player_start"][0], transition["player_start"][1],
                                       Objects.hero.hitbox[2], Objects.hero.hitbox[3])
                camera = Camera(rooms[current_room].width, rooms[current_room].height)
                break

        # Обновление камеры
        camera.update(Objects.hero)

        # Отрисовка
        screen.fill((0, 0, 0))
        rooms[current_room].draw(screen, camera)

        # Отрисовка врагов в комнате
        for enemy_combo in rooms[current_room].enemies:
            if enemy_combo[1] and Objects.hero is not None:
                enemy = enemy_combo[0][0]
                enemy.update_animation(clock.get_time() / 1000)
                enemy.go_to_hero(
                    Objects.hero.hitbox.center,
                    rooms[current_room].walls,
                    rooms[current_room].objects
                )
                enemy.draw(screen, camera)

        Objects.hero.update(0, screen, camera)

        if Objects.hero is None:
            break

        for dec in rooms[current_room].objects:
            dec.draw(screen, camera)

        for npcs in rooms[current_room].npc:
            npcs.draw(screen, camera)  # Отрисовка НПС
        dialog_box.draw(screen)   # Отрисовка диалогового окна

        if Objects.hero.dash_cooldown > 0:
            cooldown_seconds = max(0, int(Objects.hero.dash_cooldown // 1000))
            cooldown_text = cooldown_font.render(
                f"Рывок доступен через: {cooldown_seconds} сек",
                True,
                (255, 0, 0)
            )
            # Позиционируем текст в верхнем левом углу
            screen.blit(cooldown_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
