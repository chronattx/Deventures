from classes import Hero, Weapon
import pygame

weapon = Weapon(10, 58, 'assets\MainHeroSword.png')
hero = Hero((100, 100, 20, 50), 'wwfw', (110, 110), 5, 50)
hero.get_weapon(weapon)
pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            weapon.start_rotation()

    screen.fill(pygame.color.Color('WHITE'))
    weapon.update()
    hero.update()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()