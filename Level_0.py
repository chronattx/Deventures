from Classes import *
import pygame

# Размеры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 600
# Размер игрока
PLAYER_SIZE = 5000


# Камера для следования за игроком
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)  # Прямоугольник, определяющий видимую область
        self.width = width
        self.height = height

    def apply(self, rect):
        # Смещает переданный прямоугольник в соответствии с положением камеры
        return rect.move(self.camera.topleft)

    def update(self, target):
        # Центрирует камеру на игроке
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2

        # Ограничение камеры в пределах уровня
        x = min(0, x)  # Ограничение слева
        y = min(0, y)  # Ограничение сверху
        x = max(-(self.width - SCREEN_WIDTH), x)  # Ограничение справа
        y = max(-(self.height - SCREEN_HEIGHT), y)  # Ограничение снизу

        # Обновление позиции камеры
        self.camera = pygame.Rect(x, y, self.width, self.height)



# Комната
class Room:
    def __init__(self, width, height, image_path, walls, transitions):
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path).convert()  # Фон комнаты
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Масштабирование
        self.walls = walls  # Список стен
        self.transitions = transitions  # Список переходов в другие комнаты

    def draw(self, screen, camera):
        # Отображение фона
        screen.blit(self.image, camera.apply(pygame.Rect(0, 0, self.width, self.height)))

        # Отображение стен (зелёные прямоугольники)
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 255, 0), camera.apply(wall))

        # Отображение зон переходов (красные прямоугольники)
        for transition in self.transitions:
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(transition["rect"]), 2)


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
        pygame.Rect(1590, 0, 10, 800),  # Правая стена
    ]
    room1_transitions = [
        {"rect": pygame.Rect(0, 350, 10, 100), "target": "room2", "player_start": (600, 400)}
    ]
    rooms["room1"] = Room(room1_width, room1_height, "assets/room1.png", room1_walls, room1_transitions)

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
    rooms["room2"] = Room(room2_width, room2_height, "assets/room2.png", room2_walls, room2_transitions)

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
    rooms["room3"] = Room(room3_width, room3_height, "assets/room3.png", room3_walls, room3_transitions)

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
    rooms["room4"] = Room(room4_width, room4_height, "assets/room4.png", room4_walls, room4_transitions)

    # Комната 5
    room5_width, room5_height = 2000, 1200
    room5_walls = [
        pygame.Rect(0, 0, 2000, 10),  # Верхняя стена вверх
        pygame.Rect(0, 1190, 2000, 10),  # Нижняя стена
        pygame.Rect(0, 0, 10, 550),
        pygame.Rect(0, 650, 10, 550),
        pygame.Rect(1990, 0, 10, 1200)
    ]
    room5_transitions = [{"rect": pygame.Rect(0, 550, 10, 100), "target": "room4", "player_start": (1000, 500)}
                         ]
    rooms["room5"] = Room(room5_width, room5_height, "assets/room5.png", room5_walls, room5_transitions)
    return rooms


# Основной цикл игры
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Инициализация игрока и комнат
    hero_hitbox = (70, 70, 0, 0)  # Устанавливаем новые размеры хитбокса
    hero_image = "assets/FON.png"
    hero_speed = 5
    hero_health = 100
    player = Hero(hero_hitbox, hero_image, (1200, 800), hero_speed, hero_health)

    # Применяем изменение размера хитбокса (если необходимо)


    rooms = create_rooms()
    current_room = "room1"
    camera = Camera(rooms[current_room].width, rooms[current_room].height)

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Движение игрока
        player.move(keys, rooms[current_room].walls)

        # Проверка переходов между комнатами
        for transition in rooms[current_room].transitions:
            if transition["rect"].colliderect(player.rect):
                current_room = transition["target"]
                player.rect.topleft = transition["player_start"]  # Перемещение игрока в новую комнату
                camera = Camera(rooms[current_room].width, rooms[current_room].height)  # Обновление камеры
                break

        # Обновление камеры
        camera.update(player)

        # Отрисовка
        screen.fill((0, 0, 0))  # Очистка экрана
        rooms[current_room].draw(screen, camera)
        player.draw(screen, camera)

        pygame.display.flip()
        clock.tick(60)  # Ограничение FPS

    pygame.quit()


if __name__ == "__main__":
    main()