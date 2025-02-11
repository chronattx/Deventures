import pygame
import sys

from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1080, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мини-игра: Реши примеры")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  # Цвет обводки активного поля
GRAY = (200, 200, 200)  # Цвет обводки неактивного поля

BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
back_button_rect = pygame.Rect(100, 400, BUTTON_WIDTH, BUTTON_HEIGHT)

# Шрифт
font = pygame.font.Font(None, 36)

# Примеры и ответы
examples = ["2 + 2 = ", "3 + 3 = ", "4 + 4 = "]
answers = ["4", "6", "8"]
user_answers = ["", "", ""]
results = [None, None, None]

# Переменные для курсора
cursor_visible = True
cursor_timer = 0
cursor_blink_interval = 500  # Интервал мигания курсора в миллисекундах

# Прямоугольники для полей ввода
input_boxes = [
    pygame.Rect(240, 95, 200, 40),  # Поле для первого примера
    pygame.Rect(240, 145, 200, 40),  # Поле для второго примера
    pygame.Rect(240, 195, 200, 40),  # Поле для третьего примера
]

# Функция для отрисовки текста
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Основной цикл игры
def minigame_main():
    global user_answers, results, cursor_visible, cursor_timer

    active_input = 0  # Индекс активного поля ввода
    running = True
    all_correct = False
    game_success = False

    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        # Отрисовка примеров и полей ввода
        for i in range(3):
            # Обводка поля
            border_color = BLUE if i == active_input else GRAY
            pygame.draw.rect(screen, border_color, input_boxes[i], 2)

            draw_text(examples[i], 100, 100 + i * 50, BLACK)
            draw_text(user_answers[i], 250, 100 + i * 50, BLACK)
            if results[i] is not None:
                color = GREEN if results[i] else RED
                draw_text("Верно" if results[i] else "Неверно", 350, 100 + i * 50, color)

            # Отрисовка курсора в активном поле ввода
            if i == active_input and cursor_visible:
                cursor_x = 250 + font.size(user_answers[i])[0]
                pygame.draw.line(screen, BLACK, (cursor_x, 100 + i * 50), (cursor_x, 130 + i * 50), 2)

        # Отрисовка сообщения о завершении
        if all_correct:
            pygame.draw.rect(screen, GREEN, (300, 350, 200, 50))
            draw_text("Комната 2 открыта!", 310, 360, BLACK)
            pygame.draw.rect(screen, BLUE, back_button_rect)
            draw_text("Назад", 110, 410, WHITE)
            game_success = True

        # Обработка событий
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Проверка клика по кнопке "Назад"
                    if back_button_rect.collidepoint(event.pos):
                        return game_success
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    # Проверка ответа
                    if user_answers[active_input] == answers[active_input]:
                        results[active_input] = True
                    else:
                        results[active_input] = False

                    # Переход к следующему полю ввода
                    active_input = (active_input + 1) % 3

                    # Проверка, все ли ответы верны
                    if all(result is not None and result for result in results):
                        all_correct = True
                elif event.key == K_BACKSPACE:
                    user_answers[active_input] = user_answers[active_input][:-1]
                else:
                    user_answers[active_input] += event.unicode
            if event.type == MOUSEBUTTONDOWN:  # Обработка клика мыши
                if event.button == 1:  # Левая кнопка мыши
                    for i, box in enumerate(input_boxes):
                        if box.collidepoint(event.pos):  # Если клик внутри поля
                            active_input = i

        # Обновление состояния курсора
        cursor_timer += clock.get_time()
        if cursor_timer >= cursor_blink_interval:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        pygame.display.flip()
        clock.tick(30)  # Ограничение FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    minigame_main()

