from classes import *
from animate_func import load_animation_frames
from music import *
from Level0_minigame1 import minigame_main
import pygame
from strategy import example_strategy, carusel_strategy, stigoro_strategy, cycle_losandro_strategy

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
        pygame.Rect(-10, 0, 10, 800),  # Особая задняя левая стена (by ZuttoZutto)
        pygame.Rect(0, 450, 10, 350),  # Левая нижняя стена
        pygame.Rect(1590, 0, 10, 800)  # Правая стена
    ]
    room1_transitions = [
        {"rect": pygame.Rect(0, 350, 10, 100), "target": "room2", "player_start": (600, 400)}
    ]
    room1_objects = [
        GameObject('assets/decoration/Table.png', 800, 300),
        GameObject('assets/decoration/Surrodo.png', 891, 241),
        GameObject('assets/decoration/Surrodo.png', 949, 256),
        GameObject('assets/decoration/Surrodo.png', 1009, 274),
        GameObject('assets/decoration/Surrodo_inverted.png', 708, 248),
        GameObject('assets/decoration/Surrodo_inverted.png', 648, 264),
        GameObject('assets/decoration/Surrodo_inverted.png', 586, 280),
        GameObject('assets/decoration/Kachabamba.png', 595, 406),
        GameObject('assets/decoration/Kachabamba.png', 262, 483),
        GameObject('assets/decoration/Kachabamba.png', 251, 211),
        GameObject('assets/decoration/Kachabamba.png', 247, 266),
        GameObject('assets/decoration/Group1.png', 782, 718),
        GameObject('assets/decoration/Group2.png', 1297, 341),
        GameObject('assets/decoration/Poppu.png', 1440, 5),
        GameObject('assets/decoration/Poppu.png', 1500, 37),
        GameObject('assets/decoration/Poppu.png', 1508, -9)
    ]
    room1_npc = [
        NPC(800, 400, "assets/NPC_files/TheCG1.png")
    ]
    cura_idle_frames = load_animation_frames("assets/animate_enemy/Cura", 1, "Cura")  # 1 кадра для idle
    cura_run_frames = load_animation_frames("assets/animate_enemy/Cura", 24, "Cura")  # 24 кадра для run

    losandro_idle_frames = load_animation_frames("assets/animate_enemy/Losandro", 1, "Losandro")  # 1 кадра для idle
    losandro_run_frames = load_animation_frames("assets/animate_enemy/Losandro", 18, "Losandro")

    spitsa_idle_frames = load_animation_frames("assets/animate_enemy/Spitsa", 1, "Spitsa")  # 1 кадра для idle
    spitsa_run_frames = load_animation_frames("assets/animate_enemy/Spitsa", 1, "Spitsa")

    totemole_idle_frames = load_animation_frames("assets/animate_enemy/Totemole", 1, "Totemole")  # 1 кадра для idle
    totemole_run_frames = load_animation_frames("assets/animate_enemy/Totemole", 13, "Totemole")

    cura_animations = {
        "idle": cura_idle_frames,
        "run": cura_run_frames,
    }

    losandro_animations = {
        "idle": losandro_idle_frames,
        "run": losandro_run_frames,
    }

    spitsa_animations = {
        "idle": spitsa_idle_frames,
        "run": spitsa_run_frames,
    }

    totemole_animations = {
        "idle": totemole_idle_frames,
        "run": totemole_run_frames,
    }

    wave1_room1_cura = Enemy(pygame.Rect((800, 400, 0, 0)), "assets/animate_enemy/Cura/Cura1.png",
                  speed=3, health=8,
                 strategy=example_strategy,
                 animations=cura_animations, animation_speed=0.03)
    wave1_room1_cura_bata = Weapon(5, 74, "assets/weapons/Bata.png", 3)
    wave2_room1_cura = Enemy(pygame.Rect((695, 471, 77, 128)), "assets/animate_enemy/Cura/Cura1.png",
                  speed=2, health=12,
                  strategy=example_strategy,
                  animations=cura_animations, animation_speed=0.035)
    wave2_room1_cura_bata = Weapon(5, 70,
                                   "assets/weapons/Bata.png", 5)
    wave2_room1_spitsa = Enemy(pygame.Rect((927, 458, 0, 0)), "assets/animate_enemy/Spitsa/Spitsa1.png",
                  speed=8, health=5,
                  strategy=example_strategy,
                  animations=spitsa_animations, animation_speed=0.05)

    wave2_room1_spitsa_flowswordyellow = Weapon(6, 100,
                                                "assets/weapons/FlowSwordYellow.png", 10)
    wave3_room1_spitsa1 = Enemy(pygame.Rect((1252, 28, 45, 101)), "assets/animate_enemy/Spitsa/Spitsa1.png",
                               speed=7, health=4,
                               strategy=example_strategy,
                               animations=spitsa_animations, animation_speed=0.05)

    wave3_room1_spitsa1_bata = Weapon(5, 65,
                                                "assets/weapons/Bata.png", 13)
    wave3_room1_spitsa2 = Enemy(pygame.Rect((39, 30, 86, 189)), "assets/animate_enemy/Spitsa/Spitsa1.png",
                                speed=16, health=14,
                                strategy=example_strategy,
                                animations=spitsa_animations, animation_speed=0.05)

    wave3_room1_spitsa2_blobsword = Weapon(10, 116,
                                                 "assets/weapons/BlobsKneghtSword.png", 7)
    wave3_room1_spitsa3 = Enemy(pygame.Rect((1412, 630, 0, 0)), "assets/animate_enemy/Spitsa/Spitsa1.png",
                                speed=9, health=6,
                                strategy=example_strategy,
                                animations=spitsa_animations, animation_speed=0.05)

    wave3_room1_spitsa3_flowswordbrownie = Weapon(7, 103,
                                                 "assets/weapons/FlowSwordBrownie.png", 9)
    wave3_room1_cura = Enemy(pygame.Rect((78, 672, 26, 43)), "assets/animate_enemy/Cura/Cura1.png",
                  speed=3, health=10,
                  strategy=example_strategy,
                  animations=cura_animations, animation_speed=0.05)
    wave3_room1_cura_peruza = Weapon(25, 100,
                                   "assets/weapons/Peruza.png", 2)
    wave4_room1_totemole1 = Enemy(pygame.Rect((1460, 700, 126, 136)), "assets/animate_enemy/Totemole/Totemole1.png",
                             speed=13, health=25,
                             strategy=example_strategy,
                             animations=totemole_animations, animation_speed=0.05)
    wave4_room1_totemole1_washitte = Weapon(2, 20,
                                            "assets/weapons/Washitte.png", 20)
    wave4_room1_totemole2 = Enemy(pygame.Rect((1360, 700, 95, 102)), "assets/animate_enemy/Totemole/Totemole1.png",
                                  speed=12, health=5,
                                  strategy=example_strategy,
                                  animations=totemole_animations, animation_speed=0.05)
    wave4_room1_totemole2_washitte = Weapon(2, 20,
                                            "assets/weapons/Washitte.png", 20)
    wave4_room1_totemole3 = Enemy(pygame.Rect((1260, 700, 79, 85)), "assets/animate_enemy/Totemole/Totemole1.png",
                                  speed=11, health=5,
                                  strategy=example_strategy,
                                  animations=totemole_animations, animation_speed=0.05)
    wave4_room1_totemole3_washitte = Weapon(2, 20,
                                            "assets/weapons/Washitte.png", 20)
    wave4_room1_totemole4 = Enemy(pygame.Rect((1160, 700, 0, 0)), "assets/animate_enemy/Totemole/Totemole1.png",
                                  speed=10, health=5,
                                  strategy=example_strategy,
                                  animations=totemole_animations, animation_speed=0.05)
    wave4_room1_totemole4_washitte = Weapon(2, 20,
                                            "assets/weapons/Washitte.png", 20)
    wave4_room1_totemole5 = Enemy(pygame.Rect((1060, 700, 0, 0)), "assets/animate_enemy/Totemole/Totemole1.png",
                                  speed=9, health=5,
                                  strategy=example_strategy,
                                  animations=totemole_animations, animation_speed=0.05)
    wave4_room1_totemole5_washitte = Weapon(2, 20,
                                            "assets/weapons/Washitte.png", 20)
    wave4_room1_totemole6 = Enemy(pygame.Rect((960, 700, 0, 0)), "assets/animate_enemy/Totemole/Totemole1.png",
                                  speed=9, health=5,
                                  strategy=example_strategy,
                                  animations=totemole_animations, animation_speed=0.05)
    wave4_room1_totemole6_washitte = Weapon(2, 20,
                                            "assets/weapons/Washitte.png", 20)
    Objects.enemies.append(wave1_room1_cura)
    Objects.enemies.append(wave2_room1_cura)
    Objects.enemies.append(wave2_room1_spitsa)
    Objects.enemies.append(wave3_room1_spitsa1)
    Objects.enemies.append(wave3_room1_spitsa2)
    Objects.enemies.append(wave3_room1_spitsa3)
    Objects.enemies.append(wave3_room1_cura)
    Objects.enemies.append(wave4_room1_totemole1)
    Objects.enemies.append(wave4_room1_totemole2)
    Objects.enemies.append(wave4_room1_totemole3)
    Objects.enemies.append(wave4_room1_totemole4)
    Objects.enemies.append(wave4_room1_totemole5)
    Objects.enemies.append(wave4_room1_totemole6)
    wave1_room1_cura.get_weapon(wave1_room1_cura_bata)
    wave2_room1_cura.get_weapon(wave2_room1_cura_bata)
    wave2_room1_spitsa.get_weapon(wave2_room1_spitsa_flowswordyellow)
    wave3_room1_spitsa1.get_weapon(wave3_room1_spitsa1_bata)
    wave3_room1_spitsa2.get_weapon(wave3_room1_spitsa2_blobsword)
    wave3_room1_spitsa3.get_weapon(wave3_room1_spitsa3_flowswordbrownie)
    wave3_room1_cura.get_weapon(wave3_room1_cura_peruza)
    wave4_room1_totemole1.get_weapon(wave4_room1_totemole1_washitte)
    wave4_room1_totemole2.get_weapon(wave4_room1_totemole2_washitte)
    wave4_room1_totemole3.get_weapon(wave4_room1_totemole3_washitte)
    wave4_room1_totemole4.get_weapon(wave4_room1_totemole4_washitte)
    wave4_room1_totemole5.get_weapon(wave4_room1_totemole5_washitte)
    wave4_room1_totemole6.get_weapon(wave4_room1_totemole6_washitte)
    room1_enemies = [
        [[wave1_room1_cura, wave1_room1_cura_bata], False], [[wave2_room1_cura, wave2_room1_cura_bata], False],
        [[wave2_room1_spitsa, wave2_room1_spitsa_flowswordyellow], False],
        [[wave3_room1_spitsa1, wave3_room1_spitsa1_bata], False],
        [[wave3_room1_spitsa2, wave3_room1_spitsa2_blobsword], False],
        [[wave3_room1_spitsa3, wave3_room1_spitsa3_flowswordbrownie], False],
        [[wave3_room1_cura, wave3_room1_cura_peruza], False],
        [[wave4_room1_totemole1, wave4_room1_totemole1_washitte], False],
        [[wave4_room1_totemole2, wave4_room1_totemole2_washitte], False],
        [[wave4_room1_totemole3, wave4_room1_totemole3_washitte], False],
        [[wave4_room1_totemole4, wave4_room1_totemole4_washitte], False],
        [[wave4_room1_totemole5, wave4_room1_totemole5_washitte], False],
        [[wave4_room1_totemole6, wave4_room1_totemole6_washitte], False],
    ]
    room1_dialog = 'Привет игрок я хочу проверить умеешь ли ты ходить. Если готов начать проверку нажми да'
    rooms["room1"] = Room(room1_width, room1_height, "assets/rooms/room1.png", room1_walls,
                          room1_transitions, room1_objects, room1_npc, room1_enemies, room1_dialog)

    # Комната 2
    room2_width, room2_height = 800, 800
    room2_walls = [
        pygame.Rect(0, 0, 800, 10),  # Верхняя стена
        pygame.Rect(0, 790, 350, 10), # Нижняя стена вверх
        pygame.Rect(0, 800, 950, 10),
        pygame.Rect(450, 790, 350, 10), # Нижняя стена низ
        pygame.Rect(0, 0, 10, 800),  # Левая стена
        pygame.Rect(790, 0, 10, 350),  # Правая верхняя стена
        pygame.Rect(800, 0, 10, 1000),
        pygame.Rect(790, 450, 10, 350),  # Правая нижняя стена
    ]
    room2_transitions = [
        {"rect": pygame.Rect(790, 350, 10, 100), "target": "room1", "player_start": (50, 400)},  # Вход из комнаты 1
        {"rect": pygame.Rect(350, 790, 100, 10), "target": "room3", "player_start": (450, 50)},  # Выход вниз
    ]
    room2_objects = [
        GameObject('assets/decoration/Group4.png', 266, 253)
    ]
    room2_npc = [

    ]

    suura_idle_frames = load_animation_frames("assets/animate_enemy/Suura", 1, "Suura")  # 1 кадра для idle
    suura_run_frames = load_animation_frames("assets/animate_enemy/Suura", 11, "Suura")  # 24 кадра для run
    cutted_suura_run_frames = load_animation_frames("assets/animate_enemy/Suura", 1, "Suura")

    burryo_idle_frames = load_animation_frames("assets/animate_enemy/Burryo", 1, "Burryo")  # 1 кадра для idle
    burryo_run_frames = load_animation_frames("assets/animate_enemy/Burryo", 10, "Burryo")  # 24 кадра для run

    suura_animations = {
        "idle": suura_idle_frames,
        "run": cutted_suura_run_frames,
    }

    burryo_animations = {
        "idle": burryo_idle_frames,
        "run": burryo_run_frames,
    }

    carusel_animations = {
        "idle": [pygame.image.load("assets/decoration/Group4.png").convert_alpha()],
        "run": [pygame.image.load("assets/decoration/Group4.png").convert_alpha()]
    }

    wave1_room2_suurafat = Enemy(pygame.Rect((377, 360, 73, 73)), "assets/animate_enemy/Suura/Suura1.png",
                                  speed=10, health=7,
                                  strategy=carusel_strategy,
                                  animations=carusel_animations, animation_speed=0.09)
    wave1_room2_suurafat_oppaisword = Weapon(95, 240,
                                            "assets/weapons/OppaiSword.png", 2)
    wave1_room2_suura = Enemy(pygame.Rect((100, 100, 0, 0)), "assets/animate_enemy/Suura/Suura1.png",
                                 speed=2, health=5,
                                 strategy=example_strategy,
                                 animations=suura_animations, animation_speed=0.09)
    wave1_room2_suura_flowswordyellow = Weapon(7, 100,
                                             "assets/weapons/FlowSwordYellow.png", 33)
    wave1_room2_burryo = Enemy(pygame.Rect((600, 600, 0, 0)), "assets/animate_enemy/Suura/Suura1.png",
                              speed=8, health=10,
                              strategy=example_strategy,
                              animations=burryo_animations, animation_speed=0.01)
    wave1_room2_burryo_peruza = Weapon(66, 108,
                                               "assets/weapons/Peruza.png", 4)

    wave2_room2_losandro1 = Enemy(pygame.Rect((600, 600, 0, 0)), "assets/animate_enemy/Losandro/Losandro1.png",
                               speed=3, health=6,
                               strategy=example_strategy,
                               animations=losandro_animations, animation_speed=0.01)
    wave2_room2_losandro1_blobswordmode2 = Weapon(100, 150,
                                       "assets/weapons/Peruza.png", 1)
    wave2_room2_losandro2 = Enemy(pygame.Rect((600, 600, 0, 0)), "assets/animate_enemy/Losandro/Losandro1.png",
                                  speed=1, health=6,
                                  strategy=example_strategy,
                                  animations=losandro_animations, animation_speed=0.01)
    wave2_room2_losandro2_totemolebata = Weapon(200, 150,
                                                  "assets/weapons/TotemoleBata.png", 3)
    wave2_room2_susu = Enemy(pygame.Rect((377, 360, 73, 73)), "assets/animate_enemy/Suura/Suura1.png",
                                 speed=10, health=5,
                                 strategy=carusel_strategy,
                                 animations=carusel_animations, animation_speed=0.09)
    wave2_room2_susu_surrodo = Weapon(400, 312,
                                             "assets/weapons/SurrodoSurrodo.png", 1)

    wave1_room2_suurafat.get_weapon(wave1_room2_suurafat_oppaisword)
    wave1_room2_suura.get_weapon(wave1_room2_suura_flowswordyellow)
    wave1_room2_burryo.get_weapon(wave1_room2_burryo_peruza)
    wave2_room2_losandro1.get_weapon(wave2_room2_losandro1_blobswordmode2)
    wave2_room2_losandro2.get_weapon(wave2_room2_losandro2_totemolebata)
    wave2_room2_susu.get_weapon(wave2_room2_susu_surrodo)

    Objects.enemies.append(wave1_room2_suurafat)
    Objects.enemies.append(wave1_room2_suura)
    Objects.enemies.append(wave1_room2_burryo)
    Objects.enemies.append(wave2_room2_losandro1)
    Objects.enemies.append(wave2_room2_losandro2)
    Objects.enemies.append(wave2_room2_susu)

    room2_enemies = [
        [[wave1_room2_suurafat, wave1_room2_suurafat_oppaisword], False],
        [[wave1_room2_suura, wave1_room2_suura_flowswordyellow], False],
        [[wave1_room2_burryo, wave1_room2_burryo_peruza], False],
        [[wave2_room2_losandro1, wave2_room2_losandro1_blobswordmode2], False],
        [[wave2_room2_losandro2, wave2_room2_losandro2_totemolebata], False],
        [[wave2_room2_susu, wave2_room2_susu_surrodo], False]
    ]
    room2_npc = [
        NPC(200, 600, "assets/NPC_files/TheCG1.png")  # Добавляем NPC в центр комнаты
    ]
    room2_dialog = 'Не подходи ближе, пока не поговорим! Нажми "Да" чтобы начать битву.'
    rooms["room2"] = Room(room2_width, room2_height, "assets/rooms/room2.png", room2_walls, room2_transitions, room2_objects, room2_npc, room2_enemies, room2_dialog)


    # Комната 3
    room3_width, room3_height = 1000, 1000
    room3_walls = [
        pygame.Rect(0, 0, 450, 10),  # Верхняя стена вверх
        pygame.Rect(0, -10, 1450, 10),  # Верхняя стена вверх
        pygame.Rect(550, 0, 450, 10),  # Верхняя стена вверх
        pygame.Rect(0, 990, 450, 10),  # Нижняя стена
        pygame.Rect(0, 1000, 1450, 10),  # Нижняя стена
        pygame.Rect(550, 990, 450, 10),  # Нижняя стена
        pygame.Rect(0, 0, 10, 1000),  # Левая стена
        pygame.Rect(990, 0, 10, 1000),  # Правая стена
    ]
    room3_transitions = [
        {"rect": pygame.Rect(450, 0, 100, 10), "target": "room2", "player_start": (400, 700)}, # Вход сверху
        {"rect": pygame.Rect(450, 990, 100, 10), "target": "room4", "player_start": (550, 20)}  # Вход снизу
    ]
    room3_objects = [
        GameObject('assets/decoration/Firaplaces.png', 576, 0),
        GameObject('assets/decoration/Up4group.png', 224, 172),
        GameObject('assets/decoration/Shashlicku.png', 688, 336),
        GameObject('assets/decoration/upcel.png', 309, 449),
        GameObject('assets/decoration/upcel.png', 627, 638),
        GameObject('assets/decoration/upcel.png', 151, 715),
        GameObject('assets/decoration/upcel.png', 412, 892)
    ]
    room3_npc = [
        NPC(200, 50, "assets/NPC_files/TheCG1.png")
    ]

    stigoro_idle_frames = load_animation_frames("assets/animate_enemy/Stigoro", 1, "Stigoro")  # 1 кадра для idle
    stigoro_run_frames = load_animation_frames("assets/animate_enemy/Stigoro", 9, "Stigoro")  # 24 кадра для run

    stigoro_animations = {
        "idle": stigoro_idle_frames,
        "run": stigoro_run_frames,
    }

    wave1_room3_stigoro1 = Enemy(pygame.Rect((100, 100, 0, 0)), "assets/animate_enemy/Stigoro/Stigoro1.png",
                                 speed=2, health=6,
                                 strategy=stigoro_strategy,
                                 animations=stigoro_animations, animation_speed=0.02)
    wave1_room3_stigoro1_santalider = Weapon(12, 93,
                                             "assets/weapons/SantaliderSword.png", 7)

    wave1_room3_stigoro2 = Enemy(pygame.Rect((850, 850, 0, 0)),
                                 "assets/animate_enemy/Stigoro/Stigoro1.png",
                                 speed=3, health=7,
                                 strategy=stigoro_strategy,
                                 animations=stigoro_animations, animation_speed=0.01)
    wave1_room3_stigoro2_flowswordyellow = Weapon(
        13, 93, "assets/weapons/FlowSwordYellow.png", 7)

    wave1_room3_stigoro3 = Enemy(pygame.Rect((100, 850, 0, 0)), "assets/animate_enemy/Stigoro/Stigoro1.png",
                                 speed=4, health=11,
                                 strategy=stigoro_strategy,
                                 animations=stigoro_animations, animation_speed=0.03)
    wave1_room3_stigoro3_goldenkettlesword = Weapon(
        14, 90, "assets/weapons/GoldenKettleSword.png", 7)

    wave1_room3_stigoro4 = Enemy(pygame.Rect((850, 200, 0, 0)), "assets/animate_enemy/Stigoro/Stigoro1.png",
                                 speed=5, health=10,
                                 strategy=stigoro_strategy,
                                 animations=stigoro_animations, animation_speed=0.025)
    wave1_room3_stigoro4_cubirusword = Weapon(
        15, 120, "assets/weapons/CubiruSword.png", 7)

    wave2_room3_losandro1 = Enemy(pygame.Rect((850, 200, 0, 0)), "assets/animate_enemy/Losandro/Losandro1.png",
                                 speed=1, health=25,
                                 strategy=cycle_losandro_strategy,
                                 animations=losandro_animations, animation_speed=0.025)
    wave2_room3_losandro1_longsword = Weapon(
        100, 231, "assets/weapons/Symon'sLongSword.png", 1)

    wave2_room3_losandro2 = Enemy(pygame.Rect((200, 10, 0, 0)), "assets/animate_enemy/Losandro/Losandro1.png",
                                  speed=1, health=25,
                                  strategy=cycle_losandro_strategy,
                                  animations=losandro_animations, animation_speed=0.01)
    wave2_room3_losandro2_longsword = Weapon(
        100, 231, "assets/weapons/Symon'sLongSword.png", 1)

    wave2_room3_losandro3 = Enemy(pygame.Rect((800, 800, 0, 0)), "assets/animate_enemy/Losandro/Losandro1.png",
                                  speed=1, health=25,
                                  strategy=cycle_losandro_strategy,
                                  animations=losandro_animations, animation_speed=0.075)
    wave2_room3_losandro3_longsword = Weapon(
        100, 231, "assets/weapons/Symon'sLongSword.png", 1)

    wave1_room3_stigoro1.get_weapon(wave1_room3_stigoro1_santalider)
    wave1_room3_stigoro2.get_weapon(wave1_room3_stigoro2_flowswordyellow)
    wave1_room3_stigoro3.get_weapon(wave1_room3_stigoro3_goldenkettlesword)
    wave1_room3_stigoro4.get_weapon(wave1_room3_stigoro4_cubirusword)
    wave2_room3_losandro1.get_weapon(wave2_room3_losandro1_longsword)
    wave2_room3_losandro2.get_weapon(wave2_room3_losandro2_longsword)
    wave2_room3_losandro3.get_weapon(wave2_room3_losandro3_longsword)

    Objects.enemies.append(wave1_room3_stigoro1)
    Objects.enemies.append(wave1_room3_stigoro2)
    Objects.enemies.append(wave1_room3_stigoro3)
    Objects.enemies.append(wave1_room3_stigoro4)
    Objects.enemies.append(wave2_room3_losandro1)
    Objects.enemies.append(wave2_room3_losandro2)
    Objects.enemies.append(wave2_room3_losandro3)

    room3_enemies = [
        [[wave1_room3_stigoro1, wave1_room3_stigoro1_santalider], False],
        [[wave1_room3_stigoro2, wave1_room3_stigoro2_flowswordyellow], False],
        [[wave1_room3_stigoro3, wave1_room3_stigoro3_goldenkettlesword], False],
        [[wave1_room3_stigoro4, wave1_room3_stigoro4_cubirusword], False],
        [[wave2_room3_losandro1, wave2_room3_losandro1_longsword], False],
        [[wave2_room3_losandro2, wave2_room3_losandro2_longsword], False],
        [[wave2_room3_losandro3, wave2_room3_losandro3_longsword], False]
    ]
    room3_dialog = 'Ты поможешь мне защититься от врагов?(у вас нет выбора есть только видимость)'
    rooms["room3"] = Room(room3_width, room3_height, "assets/rooms/room3.png", room3_walls, room3_transitions, room3_objects, room3_npc, room3_enemies, room3_dialog)

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
    pygame.mixer.init()

    # Инициализация радио
    radio_ui = RadioUI("assets/decoration/Radio.png", 980, 50, 60, 40)  # Радио в левом верхнем углу

    # Инициализация игрока и комнат
    idle_frames = load_animation_frames("assets/animate_hero", 11, "MairouMotion")  # 3 кадра для idle
    run_frames = load_animation_frames("assets/animate_hero", 1, "MairouMotion")  # 4 кадра для run

    animations = {
        "idle": idle_frames,
        "run": run_frames,
    }

    hero_hitbox = pygame.Rect(700, 450, 92, 75)
    hero_image = "assets/animate_hero/MairouMotion1.png"
    hero_speed = 10
    hero_health = 390
    Objects.hero = Hero(hero_hitbox, hero_image, hero_speed, hero_health,
                        animations, 0.03)
    hero_weapon = Weapon(10, 93, "Weapons/SantaliderSword.png", 7)
    Objects.hero.get_weapon(hero_weapon)

    rooms = create_rooms()
    current_room = "room1"
    camera = Camera(rooms[current_room].width, rooms[current_room].height)

    Objects.hero.get_targets_to_weapon(rooms["room1"])

    # Создаем НПС
    dialog_box = DialogBox(rooms[current_room].text)

    running = True
    cooldown_font = pygame.font.Font(None, 32)

    #Волны
    wave1_room1 = False
    wave2_room1 = False
    wave3_room1 = False
    wave4_room1 = False
    room1_cleared = False

    give_room2_equipment = False

    room2_enemies_activated = False  # Флаг активации врагов
    room2_dialog_shown = False

    wave1_room2 = False
    wave2_room2 = False
    room2_cleared = False

    give_room3_equipment = False

    room3_dialog_shown = False

    room3_enemies_activated = False
    wave1_room3 = False
    wave2_room3 = False
    room3_cleared = False

    while running:
        check_music_status()
        # Обновление перезарядки
        delta_time = clock.get_time()
        Objects.hero.update_cooldowns(delta_time)

        # Обновление энергии игрока
        Objects.hero.regen_energy(delta_time)

        screen.fill((0, 0, 0))

        # Отрисовка интерфейса
        pygame.display.set_caption("Deventures")
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
                if radio_ui.check_click(mouse_pos):
                    toggle_music()
                # Проверяем, кликнули ли по НПС
                for npc in rooms[current_room].npc:
                    if npc.check_click(mouse_pos, camera):
                        dialog_box.visible = True
                        dialog_box.text = rooms[current_room].text
                        break
                    result = dialog_box.handle_click(mouse_pos)
                    if current_room == "room1" and (result == 'yes' or result == 'no'):
                        wave1_room1 = True
                        rooms[current_room].enemies[0][1] = True
                        Objects.hero.get_targets_to_weapon(rooms[current_room])

                    if current_room == "room1" and rooms[current_room].check_object_click(mouse_pos, camera, "Table.png"):
                        game_result = minigame_main()
                        if game_result:
                            pass
                    if current_room == "room2" and npc.check_click(mouse_pos, camera) and not room2_dialog_shown:
                        dialog_box.visible = True
                        dialog_box.text = rooms[current_room].dialog
                        room2_dialog_shown = True
                        break
                    if current_room == "room2" and (result == "yes" or "no"):
                        room2_enemies_activated = True
                        dialog_box.visible = False
                    if current_room == "room3" and npc.check_click(mouse_pos, camera) and not room3_dialog_shown:
                        dialog_box.visible = True
                        dialog_box.text = rooms[current_room].dialog
                        room3_dialog_shown = True
                        break
                    if current_room == "room3" and (result == "yes" or "no"):
                        room3_enemies_activated = True
                        dialog_box.visible = False


        if current_room == "room1":
            if wave1_room1 and not rooms[current_room].enemies[0][1]:
                wave2_room1 = True
                rooms[current_room].enemies[1][1] = True
                rooms[current_room].enemies[2][1] = True
                Objects.hero.get_targets_to_weapon(rooms[current_room])
                wave1_room1 = False
            if wave2_room1 and not rooms[current_room].enemies[1][1] and not rooms[current_room].enemies[2][1]:
                wave3_room1 = True
                rooms[current_room].enemies[3][1] = True
                rooms[current_room].enemies[4][1] = True
                rooms[current_room].enemies[5][1] = True
                rooms[current_room].enemies[6][1] = True
                Objects.hero.get_targets_to_weapon(rooms[current_room])
                wave2_room1 = False
            if (wave3_room1 and not rooms[current_room].enemies[3][1] and result == 'yes'
                    and not rooms[current_room].enemies[4][1]
                    and not rooms[current_room].enemies[5][1]
                    and not rooms[current_room].enemies[6][1]):
                room1_cleared = True
                wave3_room1 = False
            elif (wave3_room1 and not rooms[current_room].enemies[3][1]
                    and not rooms[current_room].enemies[4][1]
                    and not rooms[current_room].enemies[5][1]
                    and not rooms[current_room].enemies[6][1]):
                wave4_room1 = True
                wave3_room1 = False
                rooms[current_room].enemies[7][1] = True
                rooms[current_room].enemies[8][1] = True
                rooms[current_room].enemies[9][1] = True
                rooms[current_room].enemies[10][1] = True
                rooms[current_room].enemies[11][1] = True
                rooms[current_room].enemies[12][1] = True
                Objects.hero.get_targets_to_weapon(rooms[current_room])
            if (wave4_room1 and not rooms[current_room].enemies[7][1]
                    and not rooms[current_room].enemies[8][1]
                    and not rooms[current_room].enemies[9][1]
                    and not rooms[current_room].enemies[10][1]
                    and not rooms[current_room].enemies[11][1]
                    and not rooms[current_room].enemies[12][1]):
                room1_cleared = True
        elif current_room == "room2":
            if room2_enemies_activated:
                if not give_room2_equipment:
                    Objects.hero.health = 39000000
                    room2_hero_weapon = Weapon(150, 150,
                                                   "assets/weapons/BlobsKneghtSwordMode2.png", 3)
                    Objects.hero.get_weapon(room2_hero_weapon)
                    give_room2_equipment = True

                room2_enemies_activated = False
                wave1_room2 = True
                rooms[current_room].enemies[0][1] = True
                rooms[current_room].enemies[1][1] = True
                rooms[current_room].enemies[2][1] = True
                Objects.hero.get_targets_to_weapon(rooms[current_room])
            elif wave1_room2 and not rooms[current_room].enemies[0][1] and not rooms[current_room].enemies[1][1] and not rooms[current_room].enemies[2][1]:
                wave1_room2 = False
                rooms[current_room].enemies[3][1] = True
                rooms[current_room].enemies[4][1] = True
                rooms[current_room].enemies[5][1] = True
                Objects.hero.get_targets_to_weapon(rooms[current_room])
                wave2_room2 = True
            elif (wave2_room2 and not rooms[current_room].enemies[3][1]
                  and not rooms[current_room].enemies[4][1]
                  and not rooms[current_room].enemies[5][1]):
                room2_cleared = True
                wave2_room2 = False
        elif current_room == "room3":
            if not give_room3_equipment:
                Objects.hero.health = 390
                room3_hero_weapon = Weapon(1, 49,
                                            "assets/weapons/BulberBata.png", 10)
                Objects.hero.get_weapon(room3_hero_weapon)
                give_room3_equipment = True
            if room3_enemies_activated:
                wave1_room3 = True
                rooms[current_room].enemies[0][1] = True
                rooms[current_room].enemies[1][1] = True
                rooms[current_room].enemies[2][1] = True
                rooms[current_room].enemies[3][1] = True
                Objects.hero.get_targets_to_weapon(rooms[current_room])
                room3_enemies_activated = False
            elif (wave1_room3 and not rooms[current_room].enemies[0][1]
                    and not rooms[current_room].enemies[1][1]
                    and not rooms[current_room].enemies[2][1]
                    and not rooms[current_room].enemies[3][1]):
                wave1_room3 = False
                rooms[current_room].enemies[4][1] = True
                rooms[current_room].enemies[5][1] = True
                rooms[current_room].enemies[6][1] = True
                Objects.hero.get_targets_to_weapon(rooms[current_room])
                wave2_room3 = True
            elif (wave2_room3 and not rooms[current_room].enemies[4][1]
                    and not rooms[current_room].enemies[5][1]
                    and not rooms[current_room].enemies[6][1]):
                del rooms[current_room].objects[6]
                wave2_room3 = False
                room3_cleared = True





        # Движение игрока
        Objects.hero.move(keys, rooms[current_room].walls, rooms[current_room].objects, 0.15)
        Objects.hero.attack(keys)


        # Проверка переходов между комнатами
        if (current_room == "room1" and room1_cleared) or (current_room == "room2" and room2_cleared) or (current_room == "room3" and room3_cleared):
            for transition in rooms[current_room].transitions:
                if transition["rect"].colliderect(Objects.hero.rect):
                    current_room = transition["target"]
                    Objects.hero.get_targets_to_weapon(rooms[current_room])
                    Objects.hero.rect.topleft = transition["player_start"]
                    Objects.hero.hitbox = (transition["player_start"][0], transition["player_start"][1],
                                           Objects.hero.hitbox[2], Objects.hero.hitbox[3])
                    camera = Camera(rooms[current_room].width, rooms[current_room].height)
                    dialog_box.text = rooms[current_room].text
                    dialog_box.visible = False
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
                enemy.update(screen=screen, camera=camera, current_room=rooms[current_room],
                             target_pos=Objects.hero.hitbox.center, walls_list=rooms[current_room].walls,
                             objects_list=rooms[current_room].objects, delta_time=clock.get_time() / 1000)

        Objects.hero.update(clock.get_time() / 1000, screen, camera)

        if Objects.hero is None:
            break

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

        radio_ui.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()

