import pygame
from typing import Callable, List
from data_types import Coord, Rect


SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 600


class GameObject:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))


class Weapon:
    def __init__(self, damage: int, length: int, image_file: str, character=None):
        self.damage = damage
        self.length = length
        self.image_file = image_file
        self.character = character
        self.angle = 0
        self.rotation = False

    def show(self, coords: Coord, screen: pygame.surface.Surface):
        im = pygame.image.load(self.image_file)
        im = pygame.transform.rotate(im, self.angle)
        rect = im.get_rect()
        rect.center = (coords[0], coords[1] + 30)
        screen.blit(im, rect)

    def update(self):
        if self.rotation:
            self.angle += 5
            if self.angle > 120:
                self.rotation = False
                self.hit()
                self.angle = 0

    def start_rotation(self):
        self.rotation = True

    def hit(self):
        if type(self.character) == Hero:
            for enemy in Objects.enemies:
                x, y = self.character.weapon_coords()
                for a in range(x - self.length, x + 1):
                    if enemy.is_in_hitbox((a, y)):
                        enemy.get_damage(self.damage)
                        break
        else:
            x, y = self.character.weapon_coords()
            for a in range(x - self.length, x + 1):
                if Objects.hero.is_in_hitbox((a, y)):
                    Objects.hero.get_damage(self.damage)
                    break


class BaseObject:
    def __init__(self, hitbox: Rect, image_file: str, coords: Coord):
        self.hitbox = hitbox
        self.image_file = image_file
        self.coords = coords
        self.sprite = pygame.image.load(self.image_file)

    def is_in_hitbox(self, coord: Coord) -> bool:
        if (self.hitbox[0] <= coord[0] <= self.hitbox[2] + self.hitbox[0] and
            self.hitbox[1] <= coord[1] <= self.hitbox[3] + self.hitbox[1]):
            return True
        return False

    def update_hitbox(self, delta: Coord):
        self.hitbox = (self.hitbox[0] + delta[0], self.hitbox[1] + delta[1], self.hitbox[2], self.hitbox[3])

    def draw(self, screen: pygame.surface.Surface):
        sprite = pygame.sprite.Sprite()
        sprite.image = self.sprite
        sprite.rect = sprite.image.get_rect()

        sprite.rect.x = int(self.coords[0] - sprite.rect.width / 2)
        sprite.rect.y = int(self.coords[1] - sprite.rect.height / 2)

        sprites = pygame.sprite.Group()
        sprites.add(sprite)

        sprites.draw(screen)


class BaseCharacter(BaseObject):
    def __init__(self, hitbox: Rect, image_file: str, coords: Coord, speed: int, health: int):
        super().__init__(hitbox, image_file, coords)
        self.speed = speed
        self.health = self.max_health = health
        self.weapon = None
        self.melee_active = False
        self.no_damage_time = 0

    def get_weapon(self, weapon: Weapon):
        self.weapon = weapon
        self.weapon.character = self

    def attack(self):
        self.melee_active = True
        if self.weapon is not None:
            self.weapon.start_rotation()
            self.weapon.update()

    def stop_attack(self):
        self.melee_active = False

    def action(self):
        pass

    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        if self.weapon is not None:
            self.weapon.show(self.weapon_coords(), screen)

    def weapon_coords(self) -> Coord:
        return self.hitbox[0] + 5, self.hitbox[1]

    def get_damage(self, damage: int):
        if self.no_damage_time == 0:
            self.health -= damage


class Hero(BaseCharacter):
    def __init__(self, hitbox, image_file, coords, speed, health, animations):
        """
        :param hitbox: Кортеж с размерами хитбокса и изображения.
        :param image_file: Файл изображения персонажа (для статического состояния).
        :param coords: Начальные координаты персонажа.
        :param speed: Скорость персонажа.
        :param health: Здоровье персонажа.
        :param animations: Словарь с анимациями. Ключи: "idle", "run". Значения: списки кадров (pygame.Surface).
        """
        image_width, image_height = hitbox[0], hitbox[1]
        hitbox_width, hitbox_height = hitbox[2], hitbox[3]

        if hitbox_width == 0 or hitbox_height == 0:
            hitbox_width, hitbox_height = image_width, image_height

        super().__init__((hitbox_width, hitbox_height, hitbox_width, hitbox_height), image_file, coords, speed, health)

        # Статическое изображение для состояния "idle"
        self.original_image = pygame.image.load(image_file)
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=coords)
        self.rect.center = coords

        self.facing_right = True  # Направление персонажа
        self.animations = animations  # Анимации персонажа
        self.current_animation = "idle"  # Текущая анимация
        self.current_frame = 0  # Текущий кадр анимации
        self.animation_speed = 0.30  # Скорость смены кадров
        self.time_since_last_frame = 0  # Таймер для анимации

        self.resize_image(image_width, image_height)
        self.resize_hitbox(hitbox_width, hitbox_height)

    def move(self, keys, walls: List[Rect], objects: List[Rect], delta_time):
        dx, dy = 0, 0

        # Обработка нажатий клавиш
        if keys[pygame.K_w]:  # Вверх
            dy -= self.speed
        if keys[pygame.K_s]:  # Вниз
            dy += self.speed
        if keys[pygame.K_a]:  # Влево
            dx -= self.speed
            if self.facing_right:
                self.facing_right = False
                self.image = pygame.transform.flip(self.image, True, False)
        if keys[pygame.K_d]:  # Вправо
            dx += self.speed
            if not self.facing_right:
                self.facing_right = True
                self.image = pygame.transform.flip(self.image, True, False)

        # Выбор анимации
        if dx != 0 or dy != 0:
            self.current_animation = "idle"
        else:
            self.current_animation = "run"

        # Проверка коллизий и обновление позиции
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                # Если есть коллизия, отменяем перемещение по X
                self.rect.x -= dx
                break

        # Проверка коллизий с объектами по оси X
        for obj in objects:
            if self.rect.colliderect(obj):
                # Если есть коллизия, отменяем перемещение по X
                self.rect.x -= dx
                break

        # Проверка коллизий по оси Y
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                # Если есть коллизия, отменяем перемещение по Y
                self.rect.y -= dy
                break

        # Проверка коллизий с объектами по оси Y
        for obj in objects:
            if self.rect.colliderect(obj):
                # Если есть коллизия, отменяем перемещение по Y
                self.rect.y -= dy
                break

        # Обновляем координаты центра

        self.coords = self.rect.center
        self.update_animation(delta_time)

    def update_animation(self, delta_time):
        """Обновляет текущий кадр анимации."""
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame >= self.animation_speed:
            self.time_since_last_frame = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.current_frame]

            # Отзеркаливание, если персонаж смотрит влево
            if self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, screen: pygame.surface.Surface, camera=None):
        if camera is not None:
            screen.blit(self.image, camera.apply(self.rect))
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.rect), 2)
        else:
            screen.blit(self.image, self.rect)

    def resize_image(self, new_width, new_height):
        for key in self.animations:
            self.animations[key] = [
                pygame.transform.scale(frame, (new_width, new_height)) for frame in self.animations[key]
            ]
        self.rect.width = new_width
        self.rect.height = new_height

    def resize_hitbox(self, new_width, new_height):
        self.rect.width = new_width
        self.rect.height = new_height
        self.rect.center = (self.rect.centerx, self.rect.centery)

    def update(self, screen: pygame.surface.Surface, camera, delta_time):
        if self.health <= 0:
            self.die()
        else:
            self.update_animation(delta_time)
            self.draw(screen, camera)

    def die(self):
        Objects.hero = None






class Enemy(BaseCharacter):
    def __init__(self, hitbox: Rect, image_file: str, coords: Coord, speed: int, health: int, strategy: Callable):
        super().__init__(hitbox, image_file, coords, speed, health)
        self.strategy = strategy

    def move(self, delta: Coord):
        self.coords = (self.coords[0] + delta[0], self.coords[1] + delta[1])
        self.update_hitbox(delta)

    def update(self, screen: pygame.surface.Surface, *args, **kwargs):
        if self.health <= 0:
            self.die()
        else:
            mode = self.strategy(self, *args, **kwargs)  # Получаем метод из стратегии
            mode()  # Вызываем метод
            self.draw(screen)

    def go_to_hero(self):
        x1, y1 = self.coords
        x2, y2 = Objects.hero.coords
        k = self.speed / ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        distance = (int(k * (x2 - x1)), int(k * (y2 - y1)))
        self.move(distance)

    def run_away(self):
        pass

    def wait(self):
        pass

    def die(self):
        Objects.enemies.remove(self)


class Peaceful(BaseCharacter):
    def __init__(self, hitbox: Rect, image_file: str, coords: Coord, speed: int, health: int):
        super().__init__(hitbox, image_file, coords, speed, health)
        self.dialogs = ['']
        self.current = 0
        self.avatar = 'assets/haher.png'

    def current_dialog(self):
        d = self.dialogs[self.current]
        self.current += 1
        self.current %= len(self.dialogs)
        return d


class Objects:
    hero: Hero = None
    enemies: list[Enemy] = []
    peaceful: list[Peaceful] = []
    universal_weapons: dict[str, Weapon] = {}


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
    def __init__(self, width, height, image_path, walls, transitions, objects=None, npc=None, text=None):
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path).convert()  # Фон комнаты
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Масштабирование
        self.walls = walls  # Список стен
        self.transitions = transitions  # Список переходов в другие комнаты
        self.objects = objects if objects is not None else []
        self.npc = npc if npc is not None else []
        self.text = text if text is not None else []

    def draw(self, screen, camera):
        # Отображение фона
        screen.blit(self.image, camera.apply(pygame.Rect(0, 0, self.width, self.height)))

        # Отображение стен (зелёные прямоугольники)
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 255, 0), camera.apply(wall))

        # Отображение зон переходов (красные прямоугольники)
        for transition in self.transitions:
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(transition["rect"]), 2)

        # Отображение объектов
        for obj in self.objects:
            obj.draw(screen, camera)

        for npc in self.npc:
            npc.draw(screen, camera)


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
        self.dialog_rect = pygame.Rect(200, 400, 600, 200)
        self.line_spacing = 10  # Отступ между строками

    def split_text(self):
        """Разбивает текст на строки, чтобы он помещался в диалоговом прямоугольнике."""
        words = self.text.split()
        lines = []
        current_line = ""

        for word in words:
            # Проверяем, помещается ли текущая строка с добавленным словом в ширину прямоугольника
            test_line = current_line + (word + " ")
            text_width, _ = self.font.size(test_line)
            if text_width <= self.dialog_rect.width - 40:  # Учтём отступы
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines

    def draw(self, screen):
        if self.visible:
            # Рисуем диалоговый прямоугольник
            pygame.draw.rect(screen, (200, 200, 200), self.dialog_rect)

            # Рисуем текст построчно
            lines = self.split_text()
            y_offset = 420  # Начальная позиция для текста
            for line in lines:
                text_surface = self.font.render(line, True, (0, 0, 0))
                screen.blit(text_surface, (self.dialog_rect.x + 20, y_offset))
                y_offset += self.font.get_height() + self.line_spacing

            # Рисуем кнопки
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

