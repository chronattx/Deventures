from classes import *


def example_strategy(enemy: Enemy):
    x, y = enemy.weapon_coords()
    length = enemy.weapon.length
    if enemy.weapon.rotation:
        return enemy.attack
    elif enemy.health / enemy.max_health * 100 < 30:
        return enemy.run_away
    elif Objects.hero is None:
        return enemy.wait
    elif Objects.hero.is_in_hitbox((x + length, y)) :
        enemy.weapon.direction = "right"
        return enemy.attack
    elif Objects.hero.is_in_hitbox((x - length, y)) :
        enemy.weapon.direction = "left"
        return enemy.attack
    elif Objects.hero.is_in_hitbox((x, y - length)) or Objects.hero.is_in_hitbox((x, y)):
        enemy.weapon.direction = "up"
        return enemy.attack
    elif Objects.hero.is_in_hitbox((x, y + length)):
        enemy.weapon.direction = "down"
        return enemy.attack
    else:
        return enemy.go_to_hero
