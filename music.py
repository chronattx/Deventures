import pygame.mixer
import time

# Список музыкальных треков
MUSIC_TRACKS = [
    "assets/music_traks/Track1(tw).mp3",
    "assets/music_traks/Track2.mp3",
    "assets/music_traks/Track3.mp3",
    "assets/music_traks/Track4.mp3"
]


# Индекс текущего трека
current_track_index = 0

# Флаг состояния воспроизведения
is_music_playing = False

# Позиция воспроизведения (в миллисекундах), используется при паузе
music_position = 0

# Переменные для обработки двойного клика
last_click_time = 0  # Время последнего клика
click_count = 0  # Количество кликов
DOUBLE_CLICK_DELAY = 1  # Максимальная задержка между кликами (в секундах)


def play_music():
    """
    Запускает воспроизведение текущего трека с последней сохраненной позиции.
    """
    global is_music_playing, music_position
    if not is_music_playing:
        pygame.mixer.music.load(MUSIC_TRACKS[current_track_index])  # Загружаем трек
        pygame.mixer.music.play(start=music_position // 1000)  # Воспроизводим с позиции (в секундах)
        is_music_playing = True  # Отмечаем, что музыка играет


def stop_music():
    """
    Останавливает воспроизведение, запоминая текущую позицию.
    """
    global is_music_playing, music_position
    if is_music_playing:
        music_position += pygame.mixer.music.get_pos()  # Запоминаем текущую позицию
        pygame.mixer.music.stop()  # Останавливаем воспроизведение
        is_music_playing = False  # Отмечаем, что музыка не играет


def mega_stop():
    """Полная остановка музыки со сбросом состояния"""
    global is_music_playing, music_position
    pygame.mixer.music.stop()
    is_music_playing = False
    music_position = 0  # Сбрасываем позицию


def next_track():
    """
    Переключает на следующий трек в списке и начинает его воспроизведение.
    """
    global current_track_index, music_position, is_music_playing
    if is_music_playing:
        pygame.mixer.music.stop()  # Останавливаем текущий трек

    # Переход к следующему треку (по кругу)
    current_track_index = (current_track_index + 1) % len(MUSIC_TRACKS)

    # Сбрасываем позицию воспроизведения
    music_position = 0

    # Загружаем и запускаем новый трек
    pygame.mixer.music.load(MUSIC_TRACKS[current_track_index])
    pygame.mixer.music.play()
    is_music_playing = True  # Отмечаем, что музыка играет


def toggle_music():
    """
    Обрабатывает одиночный и двойной клик:
    - Одиночный клик: пауза/воспроизведение.
    - Двойной клик: переключение на следующий трек.
    """
    global last_click_time, click_count
    current_time = time.time()

    if current_time - last_click_time < DOUBLE_CLICK_DELAY:
        click_count += 1
        if click_count == 2:
            next_track()  # Переключаем на следующий трек
            click_count = 0  # Сбрасываем счетчик кликов
    else:
        click_count = 1  # Первый клик
        if is_music_playing:
            stop_music()  # Ставим на паузу
        else:
            play_music()  # Включаем музыку

    last_click_time = current_time  # Запоминаем время последнего клика


def check_music_status():
    """
    Проверяет, закончился ли текущий трек, и автоматически переключает на следующий.
    """
    global current_track_index, is_music_playing
    if is_music_playing and not pygame.mixer.music.get_busy():
        is_music_playing = False  # Отмечаем, что музыка остановилась
        current_track_index = (current_track_index + 1) % len(MUSIC_TRACKS)  # Следующий трек
        play_music()  # Запускаем новый трек


def play_credits_music(pers_music):
    """
    Останавливает текущую музыку (если она играет) и запускает музыку для титров.
    """
    global is_music_playing, music_position

    # Останавливаем текущую музыку
    if is_music_playing:
        stop_music()

    # Загружаем и запускаем музыку для титров
    pygame.mixer.music.load(pers_music)
    pygame.mixer.music.play(-1)  # -1 означает бесконечное воспроизведение
    is_music_playing = True
    music_position = 0  # Сбрасываем позицию воспроизведения
