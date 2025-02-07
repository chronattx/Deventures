from classes import *


def example_strategy(enemy: Enemy):
    length = enemy.weapon.length
    if enemy.weapon.rotation:
        return enemy.attack
    elif Objects.hero is None:
        return enemy.wait
    else:
        enemy.weapon.direction = "right"
        x, y = enemy.weapon_coords_check()
        if Objects.hero.is_in_hitbox((x + length, y)):
            return enemy.attack
        enemy.weapon.direction = "left"
        x, y = enemy.weapon_coords_check()
        if Objects.hero.is_in_hitbox((x - length, y)):
            return enemy.attack
        enemy.weapon.direction = "up"
        x, y = enemy.weapon_coords_check()
        if Objects.hero.is_in_hitbox((x, y - length)) or Objects.hero.is_in_hitbox((x, y)):
            return enemy.attack
        enemy.weapon.direction = "down"
        x, y = enemy.weapon_coords_check()
        if Objects.hero.is_in_hitbox((x, y + length)):
            return enemy.attack
        x, y = enemy.hitbox.center
        if Objects.hero.is_in_hitbox((x, y)):
            return enemy.attack
    return enemy.go_to_hero


def carusel_strategy(enemy: Enemy):
    length = enemy.weapon.length
    if enemy.weapon.rotation:
        return enemy.attack
    elif Objects.hero is None:
        return enemy.wait
    else:
        enemy.weapon.direction = "right"
        x, y = enemy.weapon_coords_check()
        if Objects.hero.is_in_hitbox((x + length, y)) or Objects.hero.is_in_hitbox((x + length * 0.7, y)):
            return enemy.attack
        enemy.weapon.direction = "left"
        x, y = enemy.weapon_coords_check()
        if Objects.hero.is_in_hitbox((x - length, y)) or Objects.hero.is_in_hitbox((x - length * 0.7, y)):
            return enemy.attack
        enemy.weapon.direction = "up"
        x, y = enemy.weapon_coords_check()
        if Objects.hero.is_in_hitbox((x, y - length)) or Objects.hero.is_in_hitbox((x, y)) or Objects.hero.is_in_hitbox((x, y - length * 0.7)):
            return enemy.attack
        enemy.weapon.direction = "down"
        x, y = enemy.weapon_coords_check()
        if Objects.hero.is_in_hitbox((x, y + length)) or Objects.hero.is_in_hitbox((x, y +length * 0.7)):
            return enemy.attack
        x, y = enemy.hitbox.center
        if Objects.hero.is_in_hitbox((x, y)):
            return enemy.attack
    return enemy.go_to_hero
