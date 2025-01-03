from data_types import Coord, Rect


class BaseObject:
    def __init__(self, hitbox: Rect, image_file: str, coords: Coord):
        self.hitbox = hitbox
        self.image_file = image_file
        self.coords = coords

    def is_in_hitbox(self, coord: Coord) -> bool:
        pass

    def current_coordinates(self) -> tuple:
        pass

    def sprite_image(self) -> str:
        return self.image_file

    def move(self, delta: Coord) -> None:
        pass

    def update_hitbox(self) -> None:
        pass

    def draw(self, screen):
        pass


class BaseCharacter(BaseObject):
    def __init__(self, hitbox: Rect, image_file: str, coords: Coord, speed: int, health: int):
        super().__init__(hitbox, image_file, coords)
        self.speed = speed
        self.health = health
        self.weapon = None
        self.melee_active = False

    def get_weapon(self, weapon):
        self.weapon = weapon

    def attack(self):
        self.melee_active = True

    def stop_attack(self):
        self.melee_active = False

    def action(self):  # эта функция должна вызывать каждый цикл нужные методы типа move или attack
        pass


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


class Weapon:
    def __init__(self, damage: int, range: int, sprite):  # спрайт чисто чтобы не забыть
        self.damage = damage
        self.range = range
        self.sprite = sprite


hero = Hero((1, 1, 1, 1), 'a.png', (1, 1), 1, 10)
entities = {'enemies': [], 'npcs': []}


def example_strategy(enemy: Enemy):
    if -5 < enemy.coords[0] - hero.coords[0] < 5:
        return enemy.mode1
    return enemy.mode2()
