from classes import Dialog, Peaceful
import pygame


pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

texts = ['hahahehe', 'hehehaha']

haher = Peaceful((100, 100, 164, 164), 'assets/minihaher.png', (132, 132), 0, 10)
haher.avatar = 'assets/haher.png'
haher.dialogs = texts

dialog = Dialog()
dialog.text = haher.current_dialog()
dialog.title = 'haher'
dialog.avatar_file = haher.avatar

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            dialog.text = haher.current_dialog()

    screen.fill(pygame.color.Color('WHITE'))
    dialog.draw(screen)
    haher.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()