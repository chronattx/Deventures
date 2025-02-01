import pygame
from pywt.data import camera

from classes import Enemy, Hero, Objects, Weapon
from strategy import example_strategy
from classes import *
from animate_func import load_animation_frames
from Level0_minigame1 import minigame_main
import pygame


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((510, 510))
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    pygame.display.flip()

    idle_frames = load_animation_frames("assets/animate_hero", 11)  # 3 кадра для idle
    run_frames = load_animation_frames("assets/animate_hero", 1)  # 4 кадра для run

    animations = {
        "idle": idle_frames,
        "run": run_frames,
    }
    hero_hitbox = (70, 70, 0, 0)
    hero_image = "assets/animate_hero/MairouMotion1.png"
    hero_speed = 1
    hero_health = 100
    hero = Hero(hero_hitbox, hero_image, (600, 400), hero_speed, hero_health, animations)
    enemy = Enemy((400, 400, 70, 120), "assets/hero.png", (435, 435), 5, 100,
                  example_strategy)
    weapon = Weapon(20, 10, "assets/weapon.png")
    enemy.get_weapon(weapon)
    Objects.hero = hero
    Objects.enemies.append(enemy)
    hero.draw(screen)
    camera = Camera(510, 510)
    enemy.draw(screen, camera)

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
