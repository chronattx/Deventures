from classes import *


def example_strategy(enemy: Enemy):
    x, y = enemy.weapon_coords()
    length = enemy.weapon.length
    if enemy.health / enemy.max_health * 100 < 30:
        return enemy.run_away
    #elif Objects.hero is None:
       # return enemy.wait
    elif Objects.hero.is_in_hitbox((Objects.hero.coords[0] + 5, Objects.hero.coords[1] + 5)):
        print("can hitttu")
    #    return enemy.attack
    else:
        return enemy.go_to_hero
