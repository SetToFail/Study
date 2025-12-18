import pygame
import sys

pygame.init()
pygame.mixer.init()  # Инициализируем звук

screen = pygame.display.set_mode((400, 300))

# Загружаем звуки (нужно создать wav файлы или использовать готовые)
# Для теста создадим простые звуки
beep_sound = pygame.mixer.Sound(buffer=bytes([128] * 8000))  # Простой бип
# Или загрузи из файла:
# beep_sound = pygame.mixer.Sound('beep.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                beep_sound.play()  # Воспроизводим звук!
    
    screen.fill((255, 255, 255))
    
    font = pygame.font.Font(None, 36)
    text = font.render("Нажми ПРОБЕЛ для звука", True, (0, 0, 0))
    screen.blit(text, (50, 130))
    
    pygame.display.flip()