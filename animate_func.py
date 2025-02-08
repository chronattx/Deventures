import os
import pygame


def load_animation_frames(folder_path, frame_count, framesname):
    """
    Загружает последовательность кадров анимации из указанной папки.
    :param folder_path: Путь к папке, где находятся файлы кадров.
    :param frame_count: Количество кадров в анимации.
    :param framesname: Общая часть имени файлов (например, 'frame' для файлов 'frame1.png', 'frame2.png' и т.д.).
    :return: Список загруженных изображений (кадров анимации).
    """
    frames = []
    for i in range(1, frame_count + 1):
        # Формируем путь к файлу кадра, добавляя номер кадра и расширение .png
        frame_path = os.path.join(folder_path, f"{framesname}{i}.png")

        # Загружаем изображение, сохраняя прозрачность (convert_alpha)
        frame = pygame.image.load(frame_path).convert_alpha()

        # Добавляем загруженный кадр в список
        frames.append(frame)

    return frames  # Возвращаем список кадров
