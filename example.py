from classes import Dialog, BaseCharacter
import pygame


pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
dialog = Dialog()
texts = ('hahahehe', 'hehehaha')
now = 0
dialog.text = 'hahahehe'
dialog.title = 'haher'
dialog.avatar_file = 'assets/haher.png'
haher = BaseCharacter((100, 100, 164, 164), 'assets/minihaher.png', (132, 132), 0, 10)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            now = (now + 1) % 2
            dialog.text = texts[now]

    screen.fill(pygame.color.Color('WHITE'))
    dialog.draw(screen)
    haher.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()