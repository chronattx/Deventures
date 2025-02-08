import pygame


def draw_bsod():
    # Устанавливаем экран в полноэкранный режим
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Создаем объект для отслеживания времени (для контроля частоты обновлений)
    clock = pygame.time.Clock()

    # Загружаем шрифт для текста с размером 35
    font = pygame.font.SysFont("Consolas", 35)

    # Переменная для управления циклом
    running = True
    n = k = 0  # Счетчики строк и задержек

    try:
        # Пытаемся открыть файл error.txt и читаем его содержимое
        with open("error.txt", "r") as file:
            rows = list(file.readlines())
    except FileNotFoundError:
        # Если файл не найден, останавливаем цикл
        running = False

    while running:
        if n != len(rows):
            # Если не все строки из файла были отображены, увеличиваем счетчик
            n += 1
            # Закрашиваем экран темно-синим цветом (цвет "синий экран смерти")
            screen.fill((0, 0, 130))

            # Отображаем строки с текста из файла на экране
            for i in range(n):
                row = font.render(rows[i].strip(), False, (255, 255, 255))  # Создаем изображение строки
                screen.blit(row, (5, 10 + 31 * i))  # Отображаем строку с небольшим смещением по вертикали

            pygame.display.flip()  # Обновляем экран
            clock.tick(10)  # Ожидаем 10 кадров в секунду, чтобы контролировать скорость вывода текста
        elif k == 3:
            # Если прошло 3 цикла, завершаем выполнение
            running = False
        else:
            # Если строк еще нет, увеличиваем счетчик задержек
            k += 1
            clock.tick(1)  # Ожидаем 1 кадр в секунду, чтобы сделать паузу между циклами


if __name__ == "__main__":
    pygame.init()  # Инициализируем Pygame
    draw_bsod()  # Запускаем функцию для отображения "синего экрана смерти"
    pygame.quit()  # Завершаем работу с Pygame
