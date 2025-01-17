import pygame

from data_types import Coord, Rect


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

    def move(self, delta: Coord):
        self.coords = self.coords[0] + delta[0], self.coords[1] + delta[1]
        self.update_hitbox(delta)

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

    def update(self, screen: pygame.surface.Surface):
        super().update(screen)
        if self.no_damage_time:
            self.no_damage_time -= 1
        if self.health <= 0:
            self.die()


class Hero(BaseCharacter):
    pass


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
        self.avatar_file = 'assets\haher.png'

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