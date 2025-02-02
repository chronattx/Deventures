import pygame


def draw_bsod():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Consolas", 35)
    running = True
    n = 0

    try:
        with open("error.txt", "r") as file:
            rows = list(file.readlines())
    except FileNotFoundError:
        running = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if n != len(rows):
            n += 1
            screen.fill((0, 0, 130))

            for i in range(n):
                row = font.render(rows[i].strip(), False, (255, 255, 255))
                screen.blit(row, (5, 10 + 31 * i))

            pygame.display.flip()
            clock.tick(10)


if __name__ == '__main__':
    pygame.init()
    draw_bsod()
    pygame.quit()
