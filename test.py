import pygame
from pygame.locals import *
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
        rect.center = coords  # Позиция оружия привязана к персонажу
        screen.blit(im, rect)

    def update(self):
        if self.rotation:
            self.angle += 10  # Скорость вращения оружия
            if self.angle > 120:
                self.rotation = False
                self.angle = 0
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def start_rotation(self):
        if self.attack_cooldown == 0:
            self.rotation = True
            self.attack_cooldown = 30  # Задержка между атаками

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
        self.attack_cooldown = 0
        self.rect = pygame.Rect(coords[0], coords[1], hitbox[0], hitbox[1])

    def update(self, screen: pygame.surface.Surface, hero, *args, **kwargs):
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
        distance_to_hero = ((self.rect.centerx - hero.rect.centerx) ** 2 +
                            (self.rect.centery - hero.rect.centery) ** 2) ** 0.5
        if distance_to_hero < 100 and self.attack_cooldown == 0:  # Дистанция для атаки
            self.attack()
            self.attack_cooldown = 60  # Задержка между атаками

    def attack(self):
        if self.weapon:
            self.weapon.start_rotation()
            self.weapon.hit()  # Наносим урон игроку

    def weapon_coords(self) -> Coord:
        # Оружие появляется справа от врага
        return self.rect.centerx + 40, self.rect.centery

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

    def weapon_coords(self) -> Coord:
        # Оружие появляется справа от персонажа
        return self.rect.centerx + 40, self.rect.centery

    def attack(self):
        if self.weapon:
            self.weapon.start_rotation()

# Размеры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 600


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

# Камера для следования за игроком
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)


# Комната
class Room:
    def __init__(self, width, height, image_path, walls, transitions):
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.walls = walls
        self.transitions = transitions

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(pygame.Rect(0, 0, self.width, self.height)))
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 255, 0), camera.apply(wall))
        for transition in self.transitions:
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(transition["rect"]), 2)


# Функция создания комнат
def create_rooms():
    rooms = {}

    # Комната 1
    room1_width, room1_height = 1600, 800
    room1_walls = [
        pygame.Rect(0, 0, 1600, 10),
        pygame.Rect(0, 790, 1600, 10),
        pygame.Rect(0, 0, 10, 350),
        pygame.Rect(0, 450, 10, 350),
        pygame.Rect(1590, 0, 10, 800),
    ]
    room1_transitions = [
        {"rect": pygame.Rect(0, 350, 10, 100), "target": "room2", "player_start": (600, 400)}
    ]
    rooms["room1"] = Room(room1_width, room1_height, "assets/room1.png", room1_walls, room1_transitions)

    return rooms


# Основной цикл игры
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Инициализация игрока и комнат
    hero = Hero((70, 70, 50, 50), "assets/walk1.png", (1200, 600), 5, 100)
    hero.get_weapon(Weapon(10, 50, "assets/walk1.png"))

    rooms = create_rooms()
    current_room = "room1"
    camera = Camera(rooms[current_room].width, rooms[current_room].height)

    # Создаем НПС
    npc = NPC(1200, 600, "assets/walk1.png")
    dialog_box = DialogBox("Помоги мне победить монстров!")

    # Враги
    enemies = []
    enemy_spawn_points = [
        (100, 100),  # Левый верхний угол
        (1500, 100),  # Правый верхний угол
        (100, 700),  # Левый нижний угол
        (1500, 700),  # Правый нижний угол
    ]

    # Флаги
    game_over = False
    enemies_spawned = False

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:  # ЛКМ
                    hero.attack()
                elif event.button == 3:  # ПКМ
                    # Проверяем, находится ли игрок рядом с НПС
                    distance_to_npc = ((hero.rect.centerx - npc.rect.centerx) ** 2 +
                                       (hero.rect.centery - npc.rect.centery) ** 2) ** 0.5
                    if distance_to_npc < 100:  # Расстояние для взаимодействия
                        dialog_box.visible = True

            # Обработка диалогового окна
            if dialog_box.visible:
                result = dialog_box.handle_click(mouse_pos)
                if result == "yes":
                    enemies_spawned = True
                    for spawn_point in enemy_spawn_points:
                        enemy = Enemy((50, 50, 0, 0), "assets/walk1.png", spawn_point, 3, 50, "chase")
                        enemy.get_weapon(Weapon(5, 40, "assets/walk1.png"))
                        enemies.append(enemy)
                elif result == "no":
                    dialog_box.visible = False

        if not game_over:
            # Движение игрока
            hero.move(keys, rooms[current_room].walls)

            # Обновление врагов
            if enemies_spawned:
                for enemy in enemies:
                    enemy.update(screen, hero)
                    if enemy.health <= 0:
                        enemies.remove(enemy)

            # Проверка на смерть игрока
            if hero.health <= 0:
                game_over = True

            # Обновление камеры
            camera.update(hero)

        # Отрисовка
        screen.fill((0, 0, 0))
        rooms[current_room].draw(screen, camera)
        hero.draw(screen, camera)
        npc.draw(screen, camera)
        if enemies_spawned:
            for enemy in enemies:
                enemy.draw(screen)
        dialog_box.draw(screen)

        # Отрисовка экрана смерти
        if game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Вы погибли", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

            # Кнопка "Переиграть"
            restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50)
            pygame.draw.rect(screen, (0, 255, 0), restart_button)
            font = pygame.font.Font(None, 36)
            text = font.render("Переиграть", True, (0, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT // 2 + 65))

            # Обработка клика по кнопке "Переиграть"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    main()  # Перезапуск игры

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()