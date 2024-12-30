class BaseObject:
    def __init__(self, hitbox: tuple[int, int], image_file: str, coords: tuple[int, int]):
        self.hitbox = hitbox
        self.image_file = image_file
        self.coords = coords

    def is_in_hitbox(self, coord: tuple[int, int]) -> bool:
        pass

    def current_coordinates(self) -> tuple:
        pass

    def sprite_image(self) -> str:
        pass

    def move(self, delta: tuple[int, int]) -> None:
        pass