from classes import Enemy, Objects


def example_strategy(enemy: Enemy, objects: Objects):
    if -5 < enemy.coords[0] - objects.hero.coords[0] < 5:
        return enemy.mode1
    return enemy.mode2