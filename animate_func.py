import os
import pygame


def load_animation_frames(folder_path, frame_count):
    frames = []
    for i in range(1, frame_count + 1):
        frame_path = os.path.join(folder_path, f"MairouMotion{i}.png")  # Файлы называются: 1.png, 2.png, ...
        frame = pygame.image.load(frame_path).convert_alpha()
        frames.append(frame)
    return frames

def load_cura_animation_frames(folder_path, frame_count):
    frames = []
    for i in range(1, frame_count + 1):
        frame_path = os.path.join(folder_path, f"Cura{i}.png")  # Файлы называются: 1.png, 2.png, ...
        frame = pygame.image.load(frame_path).convert_alpha()
        frames.append(frame)
    return frames