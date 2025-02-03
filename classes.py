import pygame
from typing import Callable
from BSoD import draw_bsod
from data_types import Coord
import math


SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 600


class GameObject:
    def __init__(self, image_path, x, y):
        self.image_path = image_path  # Сохраняем путь к изображению
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))



class Weapon:
    def __init__(self, damage: int, length: int, image_file: str, angle_per_frame: str, character=None):
        self.damage = damage
        self.length = length
        self.image_file = image_file
        self.character = character
        self.angle = 0
        self.rotation = False
        self.direction = "right"
        self.angle_per_frame = angle_per_frame
        self.targets = [[]]

    def show(self, coords: Coord, screen: pygame.surface.Surface, camera):
        im = pygame.image.load(self.image_file)
        if self.rotation:
            if self.direction == "right" or self.direction == "up":
                im = pygame.transform.flip(im, True, False)
        else:
            if self.character.facing_right:
                im = pygame.transform.flip(im, True, False)
        im = pygame.transform.rotate(im, self.angle)
        rect = im.get_rect()
        rect.center = (coords[0], coords[1])
        screen.blit(im, camera.apply(rect))

    def update(self, coords):
        for i in range(len(self.targets)):
            character = self.targets[i]
            if character[1]:
                for multiplier in [0, 0.5, 1]:
                    x_proection = coords[0] + int(self.length * multiplier * math.sin(self.angle))
                    y_proection = coords[1] + int(self.length * multiplier * math.cos(self.angle))
                    if character[0].is_in_hitbox((x_proection, y_proection)):
                        character[0].get_damage(self.damage)
                        character[1] = False
                        break
        if self.rotation:
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
            else:
                self.angle += self.angle_per_frame
                if self.angle > 240:
                    self.rotation = False
                    self.angle = 0

    def start_rotation(self):
        self.rotation = True
        for character in self.targets:
            character[1] = True
        if self.direction == "right":
            self.angle = 330
        elif self.direction == "left":
            self.angle = 30
        elif self.direction == "up":
            self.angle = 60
            self.up_attack_bool = False
        else:
            self.angle = 120


class BaseObject:
    def __init__(self, hitbox: pygame.Rect, image_file: str, animations, animation_speed):
        self.image_file = image_file
        self.original_image = pygame.image.load(image_file)
        self.image = self.original_image

        self.facing_right = True
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
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.hitbox), 2)
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
        self.weapon.targets = [[enemy_combo[0][0], enemy_combo[1]] for enemy_combo in current_room.enemies]

    def attack(self):
        if self.weapon is not None:
            if not self.weapon.rotation:
                self.weapon.start_rotation()
            self.weapon.update(self.weapon_coords())

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

    def get_damage(self, damage: int):
        self.health -= damage


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



    def move(self, keys, walls: list[pygame.Rect], objects: list[pygame.Rect], delta_time):
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
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.rect), 2)
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
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
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
            self.die()
        else:
            self.update_animation(delta_time)
            self.draw(screen, camera)
            self.draw_energy_bar(screen)

    def die(self):
        draw_bsod()
        Objects.hero = None


class Enemy(BaseCharacter):
    def __init__(self, hitbox: pygame.Rect, image_file: str, speed: int, health: int, strategy: Callable, animations, animation_speed):
        super().__init__(hitbox, image_file, speed, health, animations, animation_speed)
        self.strategy = strategy

    def move(self, delta: Coord):
        self.coords = (self.hitbox[0] + delta[0], self.hitbox[1] + delta[1])
        self.update_hitbox(delta)
        if delta[0] >= 0:
            self.facing_right = True
        else:
            self.facing_right = False

    def update(self, screen: pygame.surface.Surface, camera, current_room, *args, **kwargs):
        if self.health <= 0:
            self.die(current_room)
        else:
            mode = self.strategy(self, *args, **kwargs)
            mode()
            self.draw(screen, camera)

    def go_to_hero(self):
        x1, y1 = self.hitbox.center
        x2, y2 = Objects.hero.coords
        k = self.speed / (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 + 0.0000001)
        distance = (int(k * (x2 - x1)), int(k * (y2 - y1)))
        self.move(distance)

    def run_away(self):
        pass

    def wait(self):
        pass

    def die(self, current_room):
        for i in range(len(current_room.enemies)):
            enemy = current_room.enemies[i]
            if enemy[0][0] == self:
                current_room.enemies[i][1] = False
                break


class Peaceful(BaseCharacter):
    def __init__(self, hitbox: pygame.Rect, image_file: str, speed: int, health: int, animations):
        super().__init__(hitbox, image_file, speed, health, animations)
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
            pygame.draw.rect(screen, (0, 255, 0), camera.apply(wall))

        # Отображение зон переходов (красные прямоугольники)
        for transition in self.transitions:
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(transition["rect"]), 2)

        # Отображение объектов
        for obj in self.objects:
            obj.draw(screen, camera)

        for npc in self.npc:
            npc.draw(screen, camera)

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
