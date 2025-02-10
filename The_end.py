from music import *
import pygame


def show_credits(screen):
    # Инициализация параметров внутри функции
    screen_width, screen_height = screen.get_size()
    clock = pygame.time.Clock()

    # Загрузка ресурсов
    try:
        background = pygame.image.load('assets/FON.png').convert()
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except Exception as e:
        print(f"Error loading background: {e}")
        background = pygame.Surface((screen_width, screen_height))
        background.fill((0, 0, 0))

    font = pygame.font.SysFont('Monotype Corsiva', 40)

    # Текст титров
    credits_text = [
        "«Что ж... Ты смог победить меня...»",
        "Кашель переходит в хриплый смех",
        "«Кх-кх... Наверное, думаешь: 'Вот оно — счастье?'»",
        "«Этот кошмар кончился?»",
        "«Но... ха...»",
        "«Он только начинается.»",
        "«Видишь ли, во вселенной должен царить баланс.»",
        "«Вечное танго чёрного и белого.»",
        "«Яда и противоядия.»",
        "«Ты никогда не задумывался — кто эти монстры,",
        "что пали от твоей руки?»",
        "«Все они... несчастные души, затянутые в эту бездну, как и ты.»",
        "«Но им не досталось твоей силы...»",
        "«Они погибли здесь навеки, став частью механизма.»",
        "«Но ты, первый за 1000 лет, кто смог дойти до конца.»",
        "«И теперь займёшь моё место.»",
        "«Пока не явится новый 'спаситель' который покончит с тобой...»",
        "«Пойми: выхода нет. Не было. И не будет.»",
        "«Arrivederci, мой дорогой @@$#^&)(^%$#@»",
        "Эхо последнего слова растворяется в тишине",
        "",
        "",
        "Над игрой работали: ",
        "Николаев Дмитрий ",
        "Карташов Лёша",
        "Максимычев Степан",
        "",
        "Отдельное спасибо за то что были с нами:",
        "Молодых Юля",
        "Масяченко Денис"
    ]

    # Настройки анимации
    config = {
        'scroll_speed': 27,
        'line_spacing': 80,
        'fade_range': 150,
        'button_color': (200, 0, 0),
        'text_color': (255, 255, 255)
    }

    # Основная логика
    start_y = screen_height + 50
    button = pygame.Rect(screen_width // 2 - 100, screen_height - 100, 200, 50)
    all_text_height = len(credits_text) * config['line_spacing']
    running = True
    button_visible = False

    while running:
        delta = clock.tick(60) / 1000

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and button_visible:
                if button.collidepoint(event.pos):
                    running = False

        # Обновление позиции
        start_y -= config['scroll_speed'] * delta

        # Проверка завершения
        if start_y + all_text_height < -50:
            button_visible = True
            start_y = -all_text_height - 50

        # Отрисовка
        screen.blit(background, (0, 0))

        # Рендер текста
        for i, line in enumerate(credits_text):
            y_pos = start_y + i * config['line_spacing']
            text = font.render(line, True, config['text_color'])

            # Расчет прозрачности
            alpha = 255
            if y_pos < screen_height:
                fade = (screen_height - y_pos) / config['fade_range']
                alpha = min(255, int(255 * fade))
            if y_pos + config['line_spacing'] < 0:
                fade = abs(y_pos + config['line_spacing']) / config['fade_range']
                alpha = min(255, int(255 * fade))

            text.set_alpha(max(0, min(255, alpha)))
            screen.blit(text, text.get_rect(centerx=screen_width // 2, y=int(y_pos)))

        # Отрисовка кнопки
        if button_visible:
            pygame.draw.rect(screen, config['button_color'], button)
            btn_text = font.render("Закончить", True, config['text_color'])
            screen.blit(btn_text, btn_text.get_rect(center=button.center))

        pygame.display.flip()

    return False
