import pygame
from Classes import *


class Weapon:
    def __init__(self, damage: int, range: int, sprite: str, character=None):
        self.damage = damage
        self.range = range
        self.sprite = sprite
        self.angle = 0
        self.rotation = False
        self.character = character
        self.attack_cooldown = 0  # Задержка между атаками

    def show(self, coords: Coord, screen: pygame.surface.Surface):
        im = pygame.image.load(self.sprite)
        im = pygame.transform.rotate(im, self.angle)
        rect = im.get_rect()
        rect.center = (coords[0], coords[1] + 30)
        screen.blit(im, rect)

    def update(self):
        if self.rotation:
            self.angle += 10  # Увеличим скорость вращения для анимации
            if self.angle > 120:
                self.rotation = False
                self.angle = 0
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def start_rotation(self):
        if self.attack_cooldown == 0:  # Проверяем задержку
            self.rotation = True
            self.attack_cooldown = 30  # Устанавливаем задержку между атаками

    def hit(self):
        if self.rotation and self.angle >= 60:  # Наносим урон только в середине анимации
            if isinstance(self.character, Hero):
                for enemy in Objects.enemies:
                    if self.is_in_range(enemy):
                        enemy.get_damage(self.damage)
            elif isinstance(self.character, Enemy):
                if self.is_in_range(Objects.hero):
                    Objects.hero.get_damage(self.damage)

    def is_in_range(self, target):
        x, y = self.character.weapon_coords()
        target_x, target_y = target.rect.center
        distance = ((x - target_x) ** 2 + (y - target_y) ** 2) ** 0.5
        return distance <= self.range


class Enemy(BaseCharacter):
    def __init__(self, hitbox: Rect, image_file: str, coords: Coord, speed: int, health: int, strategy="chase"):
        super().__init__(hitbox, image_file, coords, speed, health)
        self.strategy = strategy
        self.attack_cooldown = 0  # Задержка между атаками

    def update(self, screen: pygame.surface.Surface, hero):
        super().update(screen)
        if self.strategy == "chase":
            self.chase(hero)
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        self.draw(screen)

    def chase(self, hero):
        # Преследование игрока
        dx, dy = 0, 0
        if self.rect.centerx < hero.rect.centerx:
            dx = self.speed
        elif self.rect.centerx > hero.rect.centerx:
            dx = -self.speed
        if self.rect.centery < hero.rect.centery:
            dy = self.speed
        elif self.rect.centery > hero.rect.centery:
            dy = -self.speed

        self.rect.x += dx
        self.rect.y += dy

        # Атака, если близко к игроку
        if self.weapon and self.weapon.is_in_range(hero) and self.attack_cooldown == 0:
            self.attack()
            self.attack_cooldown = 60  # Задержка между атаками

    def attack(self):
        if self.weapon:
            self.weapon.start_rotation()


class Hero(BaseCharacter):
    def __init__(self, hitbox, image_file, coords, speed, health):
        super().__init__(hitbox, image_file, coords, speed, health)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect(topleft=coords)
        self.rect.center = coords

    def move(self, keys, walls):
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_s]:
            dy = self.speed
        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed

        self.rect.x += dx
        if any(self.rect.colliderect(wall) for wall in walls):
            self.rect.x -= dx

        self.rect.y += dy
        if any(self.rect.colliderect(wall) for wall in walls):
            self.rect.y -= dy

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
        if self.weapon:
            self.weapon.show(self.weapon_coords(), screen)

    def attack(self):
        if self.weapon:
            self.weapon.start_rotation()


from Classes import *
import pygame

# Размеры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 600


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


class NPC:
    def __init__(self, x, y, image_path):
        self.rect = pygame.Rect(x, y, 200, 200)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.following = False

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))

    def check_click(self, mouse_pos, camera):
        return camera.apply(self.rect).collidepoint(mouse_pos)


class DialogBox:
    def __init__(self, text):
        self.text = text
        self.visible = False
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 28)
        self.yes_button = pygame.Rect(300, 500, 100, 40)
        self.no_button = pygame.Rect(450, 500, 100, 40)

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, (200, 200, 200), (200, 400, 600, 200))
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            screen.blit(text_surface, (220, 420))
            pygame.draw.rect(screen, (0, 255, 0), self.yes_button)
            pygame.draw.rect(screen, (255, 0, 0), self.no_button)
            yes_text = self.button_font.render("Да", True, (0, 0, 0))
            no_text = self.button_font.render("Нет", True, (0, 0, 0))
            screen.blit(yes_text, (self.yes_button.x + 30, self.yes_button.y + 10))
            screen.blit(no_text, (self.no_button.x + 30, self.no_button.y + 10))

    def handle_click(self, mouse_pos):
        if self.visible:
            if self.yes_button.collidepoint(mouse_pos):
                self.visible = False
                return "yes"
            elif self.no_button.collidepoint(mouse_pos):
                self.visible = False
                return "no"
        return None


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
    hero = Hero((70, 70, 0, 0), "FON.png", (1200, 800), 5, 100)
    hero.get_weapon(Weapon(10, 50, "assets/weapeon.png"))

    rooms = create_rooms()
    current_room = "room1"
    camera = Camera(rooms[current_room].width, rooms[current_room].height)

    # Создаем врагов
    enemies = [
        Enemy((50, 50, 0, 0), "assets/walk1.png", (800, 400), 3, 50, "chase"),
        Enemy((50, 50, 0, 0), "assets/walk1.png", (1000, 600), 3, 50, "chase")
    ]
    for enemy in enemies:
        enemy.get_weapon(Weapon(5, 40, "assets/exitbtn.png"))

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Атака по нажатию пробела
                    hero.attack()

        # Движение игрока
        hero.move(keys, rooms[current_room].walls)

        # Обновление врагов
        for enemy in enemies:
            enemy.update(screen, hero)

        # Обновление камеры
        camera.update(hero)

        # Отрисовка
        screen.fill((0, 0, 0))
        rooms[current_room].draw(screen, camera)
        hero.draw(screen, camera)
        for enemy in enemies:
            enemy.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()