from classes import Enemy, Objects


def example_strategy(enemy: Enemy):
    """
    Стратегия поведения врага: атаковать, если герой находится в зоне поражения, иначе преследовать его.
    :param enemy: Экземпляр врага.
    :return: Метод, который должен выполнить враг (атака, ожидание или преследование).
    """
    length = enemy.weapon.length  # Длина оружия (радиус атаки)

    # Если оружие уже вращается, враг атакует
    if enemy.weapon.rotation:
        return enemy.attack

    # Если герой отсутствует, враг остается на месте
    if Objects.hero is None:
        return enemy.wait

    # Проверка на попадание в зону поражения с разных направлений
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

    # Если герой в центре хитбокса врага, атаковать
    x, y = enemy.hitbox.center
    if Objects.hero.is_in_hitbox((x, y)):
        return enemy.attack

    # Если герой не в зоне атаки, враг преследует его
    return enemy.go_to_hero


def carusel_strategy(enemy: Enemy):
    """
    Стратегия "карусель": враг атакует, если герой находится в зоне поражения,
    с расширенным радиусом атаки (70% длины оружия).
    :param enemy: Экземпляр врага.
    :return: Метод, который должен выполнить враг (атака, ожидание или преследование).
    """
    length = enemy.weapon.length  # Длина оружия (радиус атаки)

    # Если оружие уже вращается, враг атакует
    if enemy.weapon.rotation:
        return enemy.attack

    # Если герой отсутствует, враг остается на месте
    if Objects.hero is None:
        return enemy.wait

    # Проверка на попадание в зону поражения с учетом дополнительного радиуса (70% длины оружия)
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
    if Objects.hero.is_in_hitbox((x, y - length)) or Objects.hero.is_in_hitbox((x, y)) or Objects.hero.is_in_hitbox(
            (x, y - length * 0.7)):
        return enemy.attack

    enemy.weapon.direction = "down"
    x, y = enemy.weapon_coords_check()
    if Objects.hero.is_in_hitbox((x, y + length)) or Objects.hero.is_in_hitbox((x, y + length * 0.7)):
        return enemy.attack

    # Если герой в центре хитбокса врага, атаковать
    x, y = enemy.hitbox.center
    if Objects.hero.is_in_hitbox((x, y)):
        return enemy.attack

    # Если герой не в зоне атаки, враг преследует его
    return enemy.go_to_hero

def stigoro_strategy(enemy: Enemy):
    enemy.weapon.direction = ["right", "left", "up", "down"][enemy.weapon.damage % 4]
    enemy.attack()
    if Objects.hero is None:
        return enemy.wait()
    return enemy.go_to_hero

def cycle_losandro_strategy(enemy: Enemy):
    enemy.cycle_attack()
    if Objects.hero is None:
        return enemy.wait()
    return enemy.go_to_hero

def friendly_strategy(enemy: Enemy):
    """
    Стратегия поведения врага: атаковать, если герой находится в зоне поражения, иначе преследовать его.
    :param enemy: Экземпляр врага.
    :return: Метод, который должен выполнить враг (атака, ожидание или преследование).
    """
    length = enemy.weapon.length  # Длина оружия (радиус атаки)

    # Если оружие уже вращается, враг атакует
    if enemy.weapon.rotation:
        return enemy.attack

    # Если герой отсутствует, враг остается на месте
    if Objects.hero is None:
        return enemy.wait

    # Проверка на попадание в зону поражения с разных направлений
    enemy.weapon.direction = "right"
    x, y = enemy.weapon_coords_check()
    if enemy.weapon.targets[0][0].is_in_hitbox((x + length, y)):
        return enemy.attack

    enemy.weapon.direction = "left"
    x, y = enemy.weapon_coords_check()
    if enemy.weapon.targets[0][0].is_in_hitbox((x - length, y)):
        return enemy.attack

    enemy.weapon.direction = "up"
    x, y = enemy.weapon_coords_check()
    if enemy.weapon.targets[0][0].is_in_hitbox((x, y - length)) or Objects.hero.is_in_hitbox((x, y)):
        return enemy.attack

    enemy.weapon.direction = "down"
    x, y = enemy.weapon_coords_check()
    if enemy.weapon.targets[0][0].is_in_hitbox((x, y + length)):
        return enemy.attack

    # Если герой в центре хитбокса врага, атаковать
    x, y = enemy.hitbox.center
    if enemy.weapon.targets[0][0].is_in_hitbox((x, y)):
        return enemy.attack

    # Если герой не в зоне атаки, враг преследует его
    return enemy.go_to_hero

def kamikadze_strategy(enemy: Enemy):
    x, y = enemy.hitbox.center
    if Objects.hero.is_in_hitbox((x, y)):
        enemy.health = -612
        Objects.hero.get_damage(23)
    if Objects.hero is None:
        return enemy.wait()
    return enemy.go_to_hero
