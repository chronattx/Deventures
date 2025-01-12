from data_types import Coord, Rect
import pygame


class Weapon:
    def __init__(self, damage: int, range: int, sprite: str):
        self.damage = damage
        self.range = range
        self.sprite = sprite
        self.angle = 0
        self.rotation = False

    def show(self, coords: Coord):
        im = pygame.image.load(self.sprite)

        im = pygame.transform.rotate(im, self.angle)
        rect = im.get_rect()
        rect.center = (coords[0], coords[1])
        screen.blit(im, rect)

    def update(self):
        if self.rotation:
            self.angle += 5
            if self.angle > 120:
                self.rotation = False
                self.angle = 0

    def start_rotation(self):
        self.rotation = True