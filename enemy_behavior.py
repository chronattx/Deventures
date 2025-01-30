import pygame

from classes import Enemy, Hero, Objects, Weapon
from strategy import example_strategy


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((510, 510))
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    pygame.display.flip()

    hero = Hero((0, 0, 70, 120), "assets/hero.png", (35, 60), 5, 100)
    enemy = Enemy((400, 400, 70, 120), "assets/hero.png", (435, 435), 5, 100,
                  example_strategy)
    weapon = Weapon(20, 10, "assets/weapon.png")
    enemy.get_weapon(weapon)
    Objects.hero = hero
    Objects.enemies.append(enemy)
    hero.draw(screen)
    enemy.draw(screen)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        if Objects.hero is not None:
            hero.update(screen)
        else:
            running = False

        enemy.update(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
