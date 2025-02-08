import pygame.mixer
import time


MUSIC_TRACKS = [
    "assets/music_traks/Track1(tw).mp3",
    "assets/music_traks/Track2.mp3",
    "assets/music_traks/Track3.mp3",
    "assets/music_traks/Track4.mp3"
]
current_track_index = 0
is_music_playing = False
music_position = 0  # Позиция воспроизведения в миллисекундах

# Добавляем переменные для отслеживания двойного клика
last_click_time = 0
click_count = 0
DOUBLE_CLICK_DELAY = 1  # 1.5 секунды для двойного клика


def play_music():
    global is_music_playing, music_position
    if not is_music_playing:
        pygame.mixer.music.load(MUSIC_TRACKS[current_track_index])
        pygame.mixer.music.play(start=music_position // 1000)
        is_music_playing = True


def stop_music():
    global is_music_playing, music_position
    if is_music_playing:
        music_position += pygame.mixer.music.get_pos()
        pygame.mixer.music.stop()
        is_music_playing = False


def next_track():
    global current_track_index, music_position, is_music_playing
    if is_music_playing:
        pygame.mixer.music.stop()
    current_track_index = (current_track_index + 1) % len(MUSIC_TRACKS)
    music_position = 0
    pygame.mixer.music.load(MUSIC_TRACKS[current_track_index])
    pygame.mixer.music.play()
    is_music_playing = True  # Принудительно включаем статус


def toggle_music():
    global last_click_time, click_count
    current_time = time.time()

    if current_time - last_click_time < DOUBLE_CLICK_DELAY:
        click_count += 1
        if click_count == 2:
            next_track()  # Всегда запускает следующий трек
            click_count = 0
    else:
        click_count = 1
        if is_music_playing:
            stop_music()
        else:
            play_music()
    last_click_time = current_time


def check_music_status():
    global current_track_index, is_music_playing
    if is_music_playing and not pygame.mixer.music.get_busy():
        is_music_playing = False
        current_track_index = (current_track_index + 1) % len(MUSIC_TRACKS)
        play_music()  # Автопереход к следующему треку