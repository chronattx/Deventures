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
        pass

    def move(self, delta: Coord) -> None:
        pass

