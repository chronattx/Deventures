import pygame
from typing import Callable
from BSoD import draw_bsod
from music import *
from data_types import Coord, Rect
import math


SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 600


class RadioUI:
    def __init__(self, image_path, x, y, width=None, height=None):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image

        # Масштабирование изображения если указаны размеры
        if width and height:
            self.image = pygame.transform.smoothscale(self.original_image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.width = width or self.original_image.get_width()
        self.height = height or self.original_image.get_height()

    def resize(self, new_width, new_height):
        """Изменяет размер изображения радио"""
        self.image = pygame.transform.smoothscale(self.original_image, (new_width, new_height))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.width = new_width
        self.height = new_height

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class GameObject:
    def __init__(self, image_path, x, y, objects=None):
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.objects = objects if objects is not None else []

        # Используем self.rect как хитбокс для коллизий
        self.collision_rect = self.rect

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))


class Weapon:
    def __init__(self, damage: int, length: int, image_file: str, angle_per_frame: int, character=None):
        """
        Инициализация оружия.
        :param damage: Урон оружия.
        :param length: Длина оружия.
        :param image_file: Путь к изображению оружия.
        :param angle_per_frame: Угол поворота оружия за кадр.
        :param character: Персонаж, владеющий оружием.
        """
        self.damage = damage
        self.length = length
        self.image_file = image_file
        self.character = character
        self.angle = 0  # Текущий угол наклона оружия
        self.rotation = False  # Флаг вращения
        self.direction = "right"  # Направление атаки
        self.angle_per_frame = angle_per_frame  # Скорость вращения оружия
        self.targets = []  # Список целей в зоне атаки
        self.up_attack_bool = False  # Флаг атаки вверх

    def show(self, coords: Coord, screen: pygame.surface.Surface, camera):
        """
        Отображение оружия на экране.
        :param coords: Координаты оружия.
        :param screen: Поверхность экрана для отрисовки.
        :param camera: Камера для преобразования координат.
        """
        im = pygame.image.load(self.image_file)  # Загрузка изображения
        if self.rotation:
            if self.direction == "right" or self.direction == "up":
                im = pygame.transform.flip(im, True, False)  # Отражение при атаке вправо/вверх
        else:
            if self.character.facing_right:
                im = pygame.transform.flip(im, True, False)  # Отражение при движении вправо

        im = pygame.transform.rotate(im, self.angle)  # Вращение изображения
        rect = im.get_rect()
        rect.center = (coords[0], coords[1])
        screen.blit(im, camera.apply(rect))  # Отрисовка оружия на экране

    def update(self, coords):
        """
        Обновление состояния оружия (вращение, проверка попаданий).
        :param coords: Координаты оружия.
        """
        for character in self.targets:
            if character[1]:  # Если цель может быть поражена
                for multiplier in [0, 0.5, 1]:  # Проверка трех точек вдоль оружия
                    x_proection = coords[0] + int(
                        self.length * multiplier * math.sin(self.angle * -1 * (math.pi / 180)))
                    y_proection = coords[1] + int(
                        self.length * multiplier * -1 * math.cos(self.angle * (math.pi / 180)))
                    if character[0].is_in_hitbox((x_proection, y_proection)):
                        character[0].get_damage(self.damage)  # Нанесение урона
                        character[1] = False  # Цель больше неуязвима в этом ударе
                        break

        if self.rotation:
            # Логика вращения оружия в зависимости от направления
            if self.direction == "right":
                self.angle -= self.angle_per_frame
                if self.angle < 210:
                    self.rotation = False
                    self.angle = 0
            elif self.direction == "left":
                self.angle += self.angle_per_frame
                if self.angle > 150:
                    self.rotation = False
                    self.angle = 0
            elif self.direction == "up":
                self.angle -= self.angle_per_frame
                if self.angle <= 0:
                    self.angle = 360
                    self.up_attack_bool = True
                if self.up_attack_bool and self.angle < 300:
                    self.rotation = False
                    self.up_attack_bool = False
                    self.angle = 0
            else:  # Атака вниз
                self.angle += self.angle_per_frame
                if self.angle > 240:
                    self.rotation = False
                    self.angle = 0

    def cycle_update(self, coords):
        for i in range(len(self.targets)):
            character = self.targets[i]
            if character[1]:
                for multiplier in [0, 0.5, 1]:
                    x_proection = coords[0] + int(self.length * multiplier * math.sin(self.angle * -1 * (math.pi / 180)))
                    y_proection = coords[1] + int(self.length * multiplier * -1 * math.cos(self.angle * (math.pi / 180)))
                    if character[0].is_in_hitbox((x_proection, y_proection)):
                        character[0].get_damage(self.damage)
                        character[1] = False
                        break
        if self.rotation:
            self.angle -= self.angle_per_frame
            if self.angle < 0:
                self.rotation = False
                self.angle = 0

    def start_rotation(self):
        """
        Начало вращения оружия.
        """
        self.rotation = True
        for character in self.targets:
            character[1] = True  # Делаем цели уязвимыми

        # Устанавливаем начальный угол вращения в зависимости от направления атаки
        if self.direction == "right":
            self.angle = 330
        elif self.direction == "left":
            self.angle = 30
        elif self.direction == "up":
            self.angle = 60
            self.up_attack_bool = False
        else:  # Вниз
            self.angle = 120

    def cycle_start_rotation(self):
        self.rotation = True
        if self.targets != [[]]:
            for character in self.targets:
                character[1] = True
            self.angle = 360


class BaseObject:
    def __init__(self, hitbox: pygame.Rect, image_file: str, animations, animation_speed):
        self.image_file = image_file
        self.original_image = pygame.image.load(image_file)
        self.image = self.original_image

        self.facing_right = False
        self.animations = {}
        for key in animations:
            self.animations[key] = []
            for frame in animations[key]:
                self.animations[key].append(frame.copy())


        self.rect = self.image.get_rect(topleft=(hitbox[0], hitbox[1]))

        image_width, image_height = hitbox[2], hitbox[3]

        if hitbox[2] == 0 or hitbox[3] == 0:
            image_width, image_height = self.rect.width, self.rect.height

        self.image = pygame.transform.scale(self.image, (image_width, image_height))
        self.resize_image(image_width, image_height)

        self.hitbox = pygame.Rect(hitbox[0], hitbox[1], self.rect.width, self.rect.height)

        self.current_animation = "run"  # Текущая анимация
        self.current_frame = 0  # Текущий кадр анимации
        self.animation_speed = animation_speed  # Скорость смены кадров
        self.time_since_last_frame = 0  # Таймер для анимации

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

    def is_in_hitbox(self, coord: Coord) -> bool:
        if (self.hitbox[0] <= coord[0] <= self.hitbox[2] + self.hitbox[0] and
            self.hitbox[1] <= coord[1] <= self.hitbox[3] + self.hitbox[1]):
            return True
        return False

    def update_hitbox(self, delta: Coord):
        self.hitbox = pygame.Rect(self.hitbox[0] + delta[0], self.hitbox[1] + delta[1], self.hitbox[2], self.hitbox[3])

    def draw(self, screen: pygame.surface.Surface, camera):
        rect = self.image.get_rect(topleft=(self.hitbox[0], self.hitbox[1]))
        #pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.hitbox), 2)
        screen.blit(self.image, camera.apply(rect))

    def resize_image(self, new_width, new_height):
        for key in self.animations:
            self.animations[key] = [
                pygame.transform.scale(frame, (new_width, new_height)) for frame in self.animations[key]
            ]
        self.rect.width = new_width
        self.rect.height = new_height


class BaseCharacter(BaseObject):
    def __init__(self, hitbox: pygame.Rect, image_file: str, speed: int, health: int, animations, animation_speed):
        super().__init__(hitbox, image_file, animations, animation_speed)
        self.speed = speed
        self.health = self.max_health = health
        self.weapon = None

    def get_weapon(self, weapon: Weapon):
        self.weapon = weapon
        self.weapon.character = self
        if self != Objects.hero:
            self.weapon.targets = [[Objects.hero, False]]

    def get_targets_to_weapon(self, current_room):
        self.weapon.targets = [[enemy_combo[0][0], False] for enemy_combo in current_room.enemies if enemy_combo[1]]

    def attack(self, *args):
        if self.weapon is not None:
            if not self.weapon.rotation:
                self.weapon.start_rotation()
            self.weapon.update(self.weapon_coords())

    def cycle_attack(self):
        if self.weapon is not None:
            if not self.weapon.rotation:
                self.weapon.cycle_start_rotation()
            self.weapon.cycle_update(self.weapon_coords())

    def draw(self, screen: pygame.surface.Surface, camera):
        super().draw(screen, camera)
        if self.weapon is not None:
            self.weapon.show(self.weapon_coords(), screen, camera)

    def weapon_coords(self) -> Coord:
        if self.weapon.rotation:
            direction = self.weapon.direction
            if direction == "right":
                if self.facing_right:
                    x = self.hitbox[0] + int(self.hitbox[2] * 0.7)
                else:
                    x = self.hitbox[0] + int(self.hitbox[2] * 0.4)
                y = self.hitbox[1] + int(self.hitbox[3] * 0.5)
            elif direction == "left":
                if self.facing_right:
                    x = self.hitbox[0] + int(self.hitbox[2] * 0.6)
                else:
                    x = self.hitbox[0] + int(self.hitbox[2] * 0.3)
                y = self.hitbox[1] + int(self.hitbox[3] * 0.5)
            elif direction == "up":
                if self.facing_right:
                    x = self.hitbox[0] + int(self.hitbox[2] * 0.6)
                else:
                    x = self.hitbox[0] + int(self.hitbox[2] * 0.4)
                y = self.hitbox[1] + int(self.hitbox[3] * 0.4)
            else:
                if self.facing_right:
                    x = self.hitbox[0] + int(self.hitbox[2] * 0.6)
                else:
                    x = self.hitbox[0] + int(self.hitbox[2] * 0.4)
                y = self.hitbox[1] + int(self.hitbox[3] * 0.6)
            return x, y
        else:
            if self.facing_right:
                x = self.hitbox[0] + int(self.hitbox[2] * 0.6)
            else:
                x = self.hitbox[0] + int(self.hitbox[2] * 0.4)
            y = self.hitbox[1] + int(self.hitbox[3] * 0.9)
            return x, y

    def weapon_coords_check(self):
        direction = self.weapon.direction
        if direction == "right":
            if self.facing_right:
                x = self.hitbox[0] + int(self.hitbox[2] * 0.7)
            else:
                x = self.hitbox[0] + int(self.hitbox[2] * 0.4)
            y = self.hitbox[1] + int(self.hitbox[3] * 0.5)
        elif direction == "left":
            if self.facing_right:
                x = self.hitbox[0] + int(self.hitbox[2] * 0.6)
            else:
                x = self.hitbox[0] + int(self.hitbox[2] * 0.3)
            y = self.hitbox[1] + int(self.hitbox[3] * 0.5)
        elif direction == "up":
            if self.facing_right:
                x = self.hitbox[0] + int(self.hitbox[2] * 0.6)
            else:
                x = self.hitbox[0] + int(self.hitbox[2] * 0.4)
            y = self.hitbox[1] + int(self.hitbox[3] * 0.4)
        else:
            if self.facing_right:
                x = self.hitbox[0] + int(self.hitbox[2] * 0.6)
            else:
                x = self.hitbox[0] + int(self.hitbox[2] * 0.4)
            y = self.hitbox[1] + int(self.hitbox[3] * 0.6)
        return x, y

    def get_damage(self, damage: int):
        self.health -= damage


def die():
    draw_bsod()
    mega_stop()
    Objects.hero = None


class Hero(BaseCharacter):
    def __init__(self, hitbox, image_file, speed, health, animations, animation_speed):
        """
        :param hitbox: Кортеж с размерами хитбокса и изображения.
        :param image_file: Файл изображения персонажа (для статического состояния).
        :param speed: Скорость персонажа.
        :param health: Здоровье персонажа.
        :param animations: Словарь с анимациями. Ключи: "idle", "run". Значения: списки кадров (pygame. Surface).
        """

        super().__init__(hitbox, image_file, speed, health, animations, animation_speed)

        self.coords = None
        self.last_dx = 0  # Последнее направление по X
        self.last_dy = 0  # Последнее направление по Y

        # Энергетическая система
        self.max_energy = 25
        self.current_energy = self.max_energy
        self.energy_regen_timer = 0  # Таймер восстановления энергии
        self.energy_regen_interval = 3000  # 3 секунды в миллисекундах

        self.dash_history = []  # Временные метки последних рывков
        self.dash_cooldown = 0  # Оставшееся время перезарядки
        self.max_dashes = 2  # Максимум рывков за период
        self.dash_window = 3000  # 3 секунды в миллисекундах
        self.cooldown_duration = 10000  # 10 секунд

    def attack(self, keys):
        if self.weapon is not None:
            if not self.weapon.rotation:
                attack = True
                if keys[pygame.K_RIGHT]:  #
                    self.weapon.direction = "right"
                elif keys[pygame.K_LEFT]:  #
                    self.weapon.direction = "left"
                elif keys[pygame.K_UP]:  # Вверх
                    self.weapon.direction = "up"
                elif keys[pygame.K_DOWN]:  # Вниз
                    self.weapon.direction = "down"
                else:
                    attack = False

                if attack:
                    self.weapon.start_rotation()
            else:
                self.weapon.update(self.weapon_coords())

    def move(self, keys, walls: list[Rect], objects: list[Rect], delta_time):
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
        dx_not_cancelled = True
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                # Если есть коллизия, отменяем перемещение по X
                self.rect.x -= dx
                dx_not_cancelled = False
                break

        # Проверка коллизий с объектами по оси X
        for obj in objects:
            if self.rect.colliderect(obj):
                # Если есть коллизия, отменяем перемещение по X
                self.rect.x -= dx
                dx_not_cancelled = False
                break

        if dx_not_cancelled:
            self.update_hitbox((dx, 0))

        # Проверка коллизий по оси Y
        dy_not_cancelled = True
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                # Если есть коллизия, отменяем перемещение по Y
                self.rect.y -= dy
                dy_not_cancelled = False
                break

        # Проверка коллизий с объектами по оси Y
        for obj in objects:
            if self.rect.colliderect(obj):
                # Если есть коллизия, отменяем перемещение по Y
                self.rect.y -= dy
                dy_not_cancelled = False
                break

        if dy_not_cancelled:
            self.update_hitbox((0, dy))

        # Обновляем координаты центра
        self.coords = self.rect.topleft
        self.update_animation(delta_time)
        self.last_dx = dx
        self.last_dy = dy

    def dash(self, walls, objects):
        """Рывок с проверкой ограничений"""
        if self.dash_cooldown > 0:
            return  # Рывок на перезарядке

        current_time = pygame.time.get_ticks()

        # Удаляем старые рывки из истории
        self.dash_history = [t for t in self.dash_history
                             if current_time - t < self.dash_window]

        if len(self.dash_history) >= self.max_dashes:
            # Активируем перезарядку
            self.dash_cooldown = self.cooldown_duration
            self.dash_history = []
            return

        # Выполняем рывок
        if self.last_dx == 0 and self.last_dy == 0:
            return

        # Рассчитываем вектор направления
        length = (self.last_dx ** 2 + self.last_dy ** 2) ** 0.5
        dir_x = self.last_dx / length
        dir_y = self.last_dy / length

        # Вычисляем смещение
        dash_x = int(dir_x * 50)
        dash_y = int(dir_y * 25)

        # Сохраняем исходную позицию
        original = self.rect.topleft

        # Применяем смещение
        self.rect.move_ip(dash_x, dash_y)
        self.dash_history.append(current_time)

        # Проверяем коллизии
        if self.check_collisions(walls, objects):
            self.rect.topleft = original  # Откат при столкновении

    def update_cooldowns(self, delta_time):
        """Обновление таймеров перезарядки"""
        if self.dash_cooldown > 0:
            self.dash_cooldown -= delta_time


    def check_collisions(self, walls, objects):
        """Проверка коллизий с окружением"""
        for wall in walls:
            if self.rect.colliderect(wall):
                return True
        for obj in objects:
            if self.rect.colliderect(obj):
                return True
        return False

    def draw(self, screen: pygame.surface.Surface, camera=None):
        if camera is not None:
            screen.blit(self.image, camera.apply(self.rect))
            # Отрисовка хитбокса
            #pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.rect), 2)
            # Отрисовка полоски здоровья
            health_bar_width = 50
            health_bar_height = 5
            health_bar_x = self.rect.centerx - health_bar_width // 2
            health_bar_y = self.rect.top - 10
            health_bar_rect = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(health_bar_rect))
            current_health_width = (self.health / self.max_health) * health_bar_width
            current_health_rect = pygame.Rect(health_bar_x, health_bar_y, current_health_width, health_bar_height)
            pygame.draw.rect(screen, (0, 255, 0), camera.apply(current_health_rect))
            if self.weapon is not None:
                self.weapon.show(self.weapon_coords(), screen, camera)
        else:
            screen.blit(self.image, self.rect)
            # Отрисовка хитбокса
            #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
            # Отрисовка полоски здоровья
            health_bar_width = 50
            health_bar_height = 5
            health_bar_x = self.rect.centerx - health_bar_width // 2
            health_bar_y = self.rect.top - 10
            health_bar_rect = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
            pygame.draw.rect(screen, (255, 0, 0), health_bar_rect)
            current_health_width = (self.health / self.max_health) * health_bar_width
            current_health_rect = pygame.Rect(health_bar_x, health_bar_y, current_health_width, health_bar_height)
            pygame.draw.rect(screen, (0, 255, 0), current_health_rect)
            if self.weapon is not None:
                self.weapon.show(self.weapon_coords(), screen, camera)

    def use_energy(self, amount):
        """Использует энергию и возвращает True, если энергии достаточно"""
        if self.current_energy >= amount:
            self.current_energy -= amount
            return True
        return False

    def regen_energy(self, delta_time):
        """Восстанавливает энергию со временем"""
        self.energy_regen_timer += delta_time
        if self.energy_regen_timer >= self.energy_regen_interval:
            self.current_energy = min(self.current_energy + 1, self.max_energy)
            self.energy_regen_timer = 0

    def draw_energy_bar(self, screen):
        bar_width = 200
        bar_height = 20
        bar_x = 1080 - bar_width - 20  # SCREEN_WIDTH = 1080
        bar_y = 20

        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        energy_width = (self.current_energy / self.max_energy) * bar_width
        pygame.draw.rect(screen, (0, 200, 255), (bar_x, bar_y, energy_width, bar_height))

        font = pygame.font.Font(None, 24)
        text = font.render(f"{self.current_energy}/{self.max_energy}", True, (0, 0, 0))
        screen.blit(text, (bar_x, bar_y + bar_height + 5))

    def update(self, delta_time, screen, camera):
        if self.health <= 0:
            die()
        else:
            self.update_animation(delta_time)
            self.draw(screen, camera)
            self.draw_energy_bar(screen)


class Enemy(BaseCharacter):
    def __init__(self, hitbox: pygame.Rect, image_file: str, speed: int, health: int, strategy: Callable, animations, animation_speed):
        super().__init__(hitbox, image_file, speed, health, animations, animation_speed)
        self.strategy = strategy
        self.current_path = []
        self.search_radius = 300
        self.stuck_timer = 0
        self.last_direction = pygame.Vector2(0, 0)
        self.target_angle = 0

    def move(self, delta: tuple, walls: list, objects: list):
        dx, dy = delta
        original_pos = self.hitbox.topleft

        # Движение по X
        self.hitbox.x += dx
        collision = False
        for wall in walls:
            if self.hitbox.colliderect(wall):
                collision = True
                break
        for obj in objects:
            if self.hitbox.colliderect(obj.collision_rect):
                collision = True
                break
        if collision:
            self.hitbox.x = original_pos[0]
            dx = 0

        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False

        # Движение по Y
        self.hitbox.y += dy
        collision = False
        for wall in walls:
            if self.hitbox.colliderect(wall):
                collision = True
                break
        for obj in objects:
            if self.hitbox.colliderect(obj.collision_rect):
                collision = True
                break
        if collision:
            self.hitbox.y = original_pos[1]
            dy = 0

        self.last_direction = pygame.Vector2(dx, dy).normalize() if (dx, dy) != (0, 0) else self.last_direction
        self.update_rotation(dx, dy)

    def update_rotation(self, dx, dy):
        target_angle = math.degrees(math.atan2(-dy, dx)) % 360
        angle_diff = (target_angle - self.target_angle + 180) % 360 - 180
        self.target_angle += angle_diff * 0.1

    def go_to_hero(self, target_pos: tuple, walls: list, objects: list):
        if pygame.time.get_ticks() - self.stuck_timer < 1000:
            return

        if pygame.time.get_ticks() % 500 < 50:
            self.current_path = self.find_simple_path(
                self.hitbox.center,
                target_pos,
                walls,
                objects
            )

        if self.current_path:
            self.follow_path(walls, objects)
        else:
            self.basic_ai_movement(target_pos, walls, objects)

    def find_simple_path(self, start, end, walls, objects, max_steps=50):
        class Node:
            def __init__(self, pos, parent=None):
                self.pos = pos
                self.parent = parent
                self.g = 0
                self.h = ((int(end[0]) - int(pos[0])) ** 2 + (int(end[1]) - int(pos[1])) ** 2) ** 0.5
                self.f = self.g + self.h

        open_set = [Node(start)]
        closed_list = []

        for _ in range(max_steps):
            if not open_set: break

            current = min(open_set, key=lambda x: x.f)
            if current.h < 50:
                path = []
                while current:
                    path.append(current.pos)
                    current = current.parent
                return path[::-1]

            closed_list.append(current)
            open_set.remove(current)

            for dx, dy in [(50, 0), (-50, 0), (0, 50), (0, -50)]:
                neighbor = (current.pos[0] + dx, current.pos[1] + dy)
                if any(n.pos == neighbor for n in closed_list):
                    continue

                if not self.check_collision(neighbor, walls, objects):
                    new_node = Node(neighbor, current)
                    new_node.g = current.g + 50
                    if not any(n.pos == neighbor and n.f <= new_node.f for n in open_set):
                        open_set.append(new_node)

        return []

    def check_collision(self, pos, walls, objects):
        temp_rect = pygame.Rect(
            pos[0] - self.hitbox.width // 2,
            pos[1] - self.hitbox.height // 2,
            self.hitbox.width,
            self.hitbox.height
        )
        return any(temp_rect.colliderect(obj) for obj in walls) or \
            any(temp_rect.colliderect(obj.collision_rect) for obj in objects)

    def follow_path(self, walls, objects):
        if len(self.current_path) < 2:
            self.current_path = []
            return

        target_point = self.current_path[0]
        if self.hitbox.collidepoint(target_point):
            self.current_path.pop(0)
            return

        direction = pygame.Vector2(target_point) - pygame.Vector2(self.hitbox.center)
        if direction.length() > 0:
            self.move(direction.normalize() * self.speed, walls, objects)

    def basic_ai_movement(self, target_pos, walls, objects):
        to_target = pygame.Vector2(target_pos) - pygame.Vector2(self.hitbox.center)
        if to_target.length() == 0:
            return

        avoidance = pygame.Vector2(0, 0)
        for obj in objects + walls:
            obstacle_rect = obj.collision_rect if hasattr(obj, "collision_rect") else obj
            vec_to_obj = pygame.Vector2(obstacle_rect.center) - self.hitbox.center
            distance = vec_to_obj.length()

            if 0 < distance < self.search_radius:
                avoidance += vec_to_obj.normalize() * (1 - distance / self.search_radius) * -1

        direction = (to_target.normalize() + avoidance)
        if direction.length() > 0:
            self.move(direction.normalize() * self.speed, walls, objects)

    def update(self, screen: pygame.surface.Surface, camera, current_room,
               target_pos, walls_list, objects_list, delta_time):
        if self.health <= 0:
            self.die(current_room)
        else:
            mode = self.strategy(self)
            mode(target_pos, walls_list, objects_list)
            self.update_animation(delta_time)
            self.draw(screen, camera)

    def run_away(self, *args):
        pass

    def wait(self, *args):
        pass

    def die(self, current_room):
        for i in range(len(current_room.enemies)):
            enemy = current_room.enemies[i]
            if enemy[0][0] == self:
                current_room.enemies[i][1] = False
                break


class Objects:
    hero: Hero = None
    enemies: list[Enemy] = []
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
    def __init__(self, width, height, image_path, walls, transitions, objects=None, npc=None, enemies=None, text=None):
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path).convert()  # Фон комнаты
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Масштабирование
        self.walls = walls  # Список стен
        self.transitions = transitions  # Список переходов в другие комнаты
        self.objects = objects if objects is not None else []
        self.npc = npc if npc is not None else []
        self.enemies = enemies if enemies is not None else []
        self.text = text if text is not None else []

    def draw(self, screen, camera):
        # Отображение фона
        screen.blit(self.image, camera.apply(pygame.Rect(0, 0, self.width, self.height)))

        # Отображение стен (зелёные прямоугольники)
        for wall in self.walls:
            pygame.draw.rect(screen, (227, 218, 100), camera.apply(wall))

        # Отображение зон переходов (красные прямоугольники)
        for transition in self.transitions:
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(transition["rect"]), 2)

        # Отрисовка NPC
        for npc in self.npc:
            npc.draw(screen, camera)

        for object in self.objects:
            object.draw(screen, camera)

    def check_object_click(self, mouse_pos, camera, target_object="Table.png"):
        """ Проверяет, кликнули ли по объекту с заданным изображением, учитывая смещение камеры. """
        adjusted_mouse_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)

        for obj in self.objects:
            if obj.rect.collidepoint(adjusted_mouse_pos):
                if obj.image_path.endswith(target_object):
                    return True
        return False


class NPC:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
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
        self.dialog_rect = pygame.Rect(100, 200, 880, 600)
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
            y_offset = 230  # Начальная позиция для текста
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
