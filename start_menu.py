import pygame
import pygame_light2d as pl2d
import time

from Level_0 import main
from pygame_light2d import LightingEngine, PointLight


# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()
screen_res = (1080, 600)
lights_engine = LightingEngine(
    screen_res=screen_res,
    native_res=screen_res,
    lightmap_res=(int(screen_res[0] / 2.5), int(screen_res[1] / 2.5))
)

clock = pygame.time.Clock()

# Полная темнота или чуть ambient
lights_engine.set_ambient(0, 0, 0, 128)

# Загрузка фона
tex_background = lights_engine.load_texture("assets/FON.png")

# Создаём источник света
light = PointLight(position=(100, 100), power=1.0, radius=600)
light.set_color(255, 255, 255, 255)
lights_engine.lights.append(light)

# --- ЗАГРУЗКА «КНОПКИ» КАК ГОТОВОГО PNG ---
btn_texture = lights_engine.load_texture("assets/buttons/startbtn.png")

# Параметры кнопки
button_w, button_h = 600, 150

# Вычисляем координаты, чтобы центрировать кнопку по окну 1280x720
button_x = (screen_res[0] - button_w) // 2
button_y = (screen_res[1] - button_h) // 2

running = True
while running:
    clock.tick(60)
    t1 = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # Проверяем попадание по кнопке
            if button_x <= mx <= button_x + button_w and button_y <= my <= button_y + button_h:
                main()
                running = False
                break
    else:

        # Двигаем фонарик за мышкой
        light.position = pygame.mouse.get_pos()

        # Очищаем, рисуем фон
        lights_engine.clear(0, 0, 0)
        lights_engine.render_texture(
            tex_background,
            pl2d.BACKGROUND,
            pygame.Rect(0, 0, screen_res[0], screen_res[1]),
            pygame.Rect(0, 0, tex_background.width, tex_background.height)
        )

        # Рендерим кнопку (освещаемый объект)
        lights_engine.render_texture(
            btn_texture,
            pl2d.BACKGROUND,  # освещаемый слой (если отсутствует — замените на число 1)
            pygame.Rect(button_x, button_y, button_w, button_h),
            pygame.Rect(0, 0, button_w, button_h)
        )

        # Накладываем освещение
        lights_engine.render()

        # Flip
        pygame.display.flip()

        # Для отладки
        t2 = time.time()
        mspt = (t2 - t1) * 1000
        pygame.display.set_caption(f"{mspt:.2f} mspt; {clock.get_fps():.2f} fps")

pygame.quit()
