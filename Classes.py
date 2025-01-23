import pygame

from data_types import Coord, Rect


class Weapon:
    def __init__(self, damage: int, range: int, sprite: str, character=None):
        self.damage = damage
        self.range = range # мб переименовать? всё-таки range - функция
        self.sprite = sprite
        self.angle = 0
        self.rotation = False
        self.character = character

    def show(self, coords: Coord, screen: pygame.surface.Surface):
        im = pygame.image.load(self.sprite)

        im = pygame.transform.rotate(im, self.angle)
        rect = im.get_rect()
        rect.center = (coords[0], coords[1] + 30)
        screen.blit(im, rect)

    def update(self):
        if self.rotation:
            self.angle += 5
            if self.angle > 120:
                self.rotation = False
                self.angle = 0

    def start_rotation(self):
        self.rotation = True

    def hit(self):
        if type(self.character) == Hero:
            for enemy in Objects.enemies:
                x, y = self.character.weapon_coords()
                for a in range(x - self.range, x + 1):
                    if enemy.is_in_hitbox((a, y)):
                        enemy.get_damage(self.damage)
                        break
        else:
            x, y = self.character.weapon_coords()
            for a in range(x - self.range, x + 1):
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

    def move(self, keys, walls):
        # Скорость перемещения
        dx, dy = 0, 0
        speed = 5

        # Управление с помощью клавиш
        if keys[pygame.K_UP]:
            dy -= speed
        if keys[pygame.K_DOWN]:
            dy += speed
        if keys[pygame.K_LEFT]:
            dx -= speed
        if keys[pygame.K_RIGHT]:
            dx += speed

        # Перемещение по X
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                # Если столкновение, откатываем перемещение
                self.rect.x -= dx

        # Перемещение по Y
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                # Если столкновение, откатываем перемещение
                self.rect.y -= dy

    def update_hitbox(self, delta: Coord):
        self.hitbox = (self.hitbox[0] + delta[0], self.hitbox[1] + delta[1],
                       self.hitbox[2] + delta[0], self.hitbox[3] + delta[1])

    def draw(self, screen: pygame.surface.Surface):
        sprites = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()

        sprite.image = self.sprite
        sprite.rect = sprite.image.get_rect()
        sprite.size = sprite.image.get_size()

        sprite.rect.x = int(self.coords[0] - sprite.size[0] / 2)
        sprite.rect.y = int(self.coords[1] - sprite.size[1] / 2)

        sprites.add(sprite)
        sprites.draw(screen)

    def update(self, screen: pygame.surface.Surface):
        pass


class BaseCharacter(BaseObject):
    def __init__(self, hitbox: Rect, image_file: str, coords: Coord, speed: int, health: int):
        super().__init__(hitbox, image_file, coords)
        self.speed = speed
        self.health = health
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

    def stop_attack(self):
        self.melee_active = False

    def action(self):  # эта функция должна вызывать каждый цикл нужные методы типа move или attack
        pass

    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        if self.weapon is not None:
            self.weapon.show(self.weapon_coords(), screen)

    def weapon_coords(self) -> Coord:
        return self.hitbox[0] - 5, (self.hitbox[1] + self.hitbox[3]) // 2

    def get_damage(self, damage: int):
        if self.no_damage_time == 0:
            self.health -= damage

    def update(self, screen: pygame.surface.Surface, *args, **kwargs):
        super().update(screen)
        if self.no_damage_time:
            self.no_damage_time -= 1
        if self.health <= 0:
            self.die()
        self.draw(screen)


class Hero(BaseCharacter):
    def __init__(self, hitbox, image_file, coords, speed, health):
        image_width, image_height = hitbox[0], hitbox[1]
        hitbox_width, hitbox_height = hitbox[2], hitbox[3]


        if hitbox_width == 0 or hitbox_height == 0:
            hitbox_width, hitbox_height = image_width, image_height

        super().__init__((hitbox_width, hitbox_height, hitbox_width, hitbox_height), image_file, coords, speed, health)

        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect(topleft=coords)
        self.rect.center = coords

        self.resize_image(image_width, image_height)
        self.resize_hitbox(hitbox_width, hitbox_height)

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
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.rect), 2)

    def resize_image(self, new_width, new_height):
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect.width = new_width
        self.rect.height = new_height

    def resize_hitbox(self, new_width, new_height):
        self.rect.width = new_width
        self.rect.height = new_height

        self.rect.center = (self.rect.centerx, self.rect.centery)


class Enemy(BaseCharacter):
    def __init__(self, hitbox: Rect, image_file: str, coords: Coord, speed: int, health: int, strategy):
        super().__init__(hitbox, image_file, coords, speed, health)
        self.strategy = strategy

    def mode1(self):
        pass

    def mode2(self):
        pass


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
    enemies: list = []


class Dialog:
    def __init__(self):
        self.text = ''
        self.title = ''
        self.avatar_file = ''

    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.rect(screen, (200, 150, 0), (0, 350, 500, 200))
        font = pygame.font.SysFont(None, 32)
        img = font.render(self.title, True, (0, 0, 0))
        screen.blit(img, (100, 370))
        font = pygame.font.SysFont(None, 24)
        img = font.render(self.text, True, (0, 0, 0))
        screen.blit(img, (100, 410))
        img = pygame.image.load(self.avatar_file)
        screen.blit(img, (10, 370))