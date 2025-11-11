import pygame
import sys
import random
import json
import os
from datetime import datetime

# Инициализация pygame
pygame.init()
pygame.mixer.init()

# Константы
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()

# Шрифты
font_large = pygame.font.SysFont('Arial', 36)
font_medium = pygame.font.SysFont('Arial', 24)
font_small = pygame.font.SysFont('Arial', 18)

# Звуковые эффекты
try:
    eat_sound = pygame.mixer.Sound('temp 3/Lab 1/move.mp3')
    game_over_sound = pygame.mixer.Sound('game_over.wav')
except:
    # Заглушки если файлы не найдены
    eat_sound = pygame.mixer.Sound(buffer=bytes([128] * 8000))
    game_over_sound = pygame.mixer.Sound(buffer=bytes([128] * 16000))

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.grow_to = 3
        self.color = GREEN
        self.is_alive = True
        self.move_counter = 0
        self.move_delay = 10  # Задержка между движениями (в кадрах)
        
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        self.direction = point
    
    def move(self):
        if not self.is_alive:
            return
            
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
            
        self.move_counter = 0
        
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        if new_position in self.positions[1:]:
            self.is_alive = False
            game_over_sound.play()
            return
            
        self.positions.insert(0, new_position)
        
        if len(self.positions) > self.grow_to:
            self.positions.pop()
    
    def set_speed(self, speed_level):
        # speed_level: 1 - медленно, 2 - нормально, 3 - быстро
        speed_settings = {
            1: 15,  # easy
            2: 10,  # medium
            3: 6,   # hard
        }
        self.move_delay = speed_settings.get(speed_level, 10)
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            color = self.color
            # Градиент цвета для змейки
            if i == 0:  # Голова
                color = (0, 200, 0)
            elif i % 2 == 0:
                color = (0, 180, 0)
                
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (0, 100, 0), rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
        
    def randomize_position(self, snake_positions=None):
        if snake_positions is None:
            snake_positions = []
            
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.difficulty = 'medium'  # easy, medium, hard
        self.set_difficulty(self.difficulty)
        self.game_over = False
        self.paused = False
        self.player_name = "Player"
        self.records = self.load_records()
            
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == 'easy':
            self.snake.set_speed(1)
        elif difficulty == 'medium':
            self.snake.set_speed(2)
        elif difficulty == 'hard':
            self.snake.set_speed(3)
            
    def load_records(self):
        try:
            with open('snake_records.json', 'r') as f:
                return json.load(f)
        except:
            return []
            
    def save_records(self):
        with open('snake_records.json', 'w') as f:
            json.dump(self.records, f, indent=2)
            
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_m:
                        return 'menu'
                elif self.paused:
                    if event.key == pygame.K_p:
                        self.paused = False
                else:
                    if event.key == pygame.K_UP:
                        self.snake.turn((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.turn((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn((1, 0))
                    elif event.key == pygame.K_p:
                        self.paused = True
                        
        return None
    
    def update(self):
        if self.paused or self.game_over:
            return
            
        self.snake.move()
        
        # Проверка съедания еды
        if self.snake.get_head_position() == self.food.position:
            eat_sound.play()
            self.snake.grow_to += 1
            self.snake.score += 1
            self.food.randomize_position(self.snake.positions)
        
        if not self.snake.is_alive:
            self.game_over = True
            # Сохранение рекорда
            self.records.append({
                "name": self.player_name,
                "score": self.snake.score,
                "length": self.snake.length,
                "difficulty": self.difficulty,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            # Сортировка по очкам
            self.records.sort(key=lambda x: x["score"], reverse=True)
            # Оставляем топ-10
            self.records = self.records[:10]
            self.save_records()
    
    def draw(self, surface):
        surface.fill(BLACK)
        
        # Рисуем сетку
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(surface, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, (40, 40, 40), (0, y), (WIDTH, y))
        
        # Рисуем еду и змейку
        self.food.draw(surface)
        self.snake.draw(surface)
        
        # Интерфейс
        score_text = font_medium.render(f'Очки: {self.snake.score}', True, WHITE)
        length_text = font_medium.render(f'Длина: {self.snake.length}', True, WHITE)
        difficulty_text = font_medium.render(f'Сложность: {self.difficulty}', True, WHITE)
        
        surface.blit(score_text, (10, 10))
        surface.blit(length_text, (10, 40))
        surface.blit(difficulty_text, (10, 70))
        
        if self.paused:
            pause_text = font_large.render('ПАУЗА', True, YELLOW)
            surface.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 50))
            continue_text = font_medium.render('Нажмите P для продолжения', True, WHITE)
            surface.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2))
        
        if self.game_over:
            # Полупрозрачный фон
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            surface.blit(s, (0, 0))
            
            game_over_text = font_large.render('ИГРА ОКОНЧЕНА!', True, RED)
            score_text = font_medium.render(f'Ваш счет: {self.snake.score}', True, WHITE)
            restart_text = font_medium.render('Нажмите R для новой игры', True, WHITE)
            menu_text = font_medium.render('Нажмите M для меню', True, WHITE)
            
            surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
            surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
            surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
            surface.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 60))
    
    def reset_game(self):
        self.snake.reset()
        self.food.randomize_position(self.snake.positions)
        self.game_over = False
        self.paused = False
        self.set_difficulty(self.difficulty)

class Menu:
    def __init__(self, game):
        self.game = game
        self.current_screen = 'main'  # main, records
        self.selected_difficulty = game.difficulty
        
    def draw(self, surface):
        surface.fill(BLACK)
        
        if self.current_screen == 'main':
            self.draw_main_menu(surface)
        elif self.current_screen == 'records':
            self.draw_records(surface)
    
    def draw_main_menu(self, surface):
        title = font_large.render('ЗМЕЙКА', True, GREEN)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        # Кнопка начала игры
        start_rect = pygame.Rect(WIDTH // 2 - 100, 200, 200, 50)
        pygame.draw.rect(surface, BLUE, start_rect)
        start_text = font_medium.render('НАЧАТЬ ИГРУ', True, WHITE)
        surface.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 215))
        
        # Выбор сложности
        diff_text = font_medium.render('Сложность:', True, WHITE)
        surface.blit(diff_text, (WIDTH // 2 - 150, 280))
        
        difficulties = ['easy', 'medium', 'hard']
        colors = [GREEN, YELLOW, RED]
        
        for i, diff in enumerate(difficulties):
            diff_rect = pygame.Rect(WIDTH // 2 - 150 + i * 100, 320, 80, 40)
            color = colors[i] if diff == self.selected_difficulty else (100, 100, 100)
            pygame.draw.rect(surface, color, diff_rect)
            diff_text = font_small.render(diff.upper(), True, WHITE)
            surface.blit(diff_text, (diff_rect.centerx - diff_text.get_width() // 2, diff_rect.centery - diff_text.get_height() // 2))
        
        # Рекорды
        records_rect = pygame.Rect(WIDTH // 2 - 100, 380, 200, 50)
        pygame.draw.rect(surface, PURPLE, records_rect)
        records_text = font_medium.render('РЕКОРДЫ', True, WHITE)
        surface.blit(records_text, (WIDTH // 2 - records_text.get_width() // 2, 395))
        
        # Выход
        exit_rect = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)
        pygame.draw.rect(surface, RED, exit_rect)
        exit_text = font_medium.render('ВЫХОД', True, WHITE)
        surface.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 465))
    
    def draw_records(self, surface):
        title = font_large.render('ТАБЛИЦА РЕКОРДОВ', True, YELLOW)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
        if not self.game.records:
            no_records = font_medium.render('Рекордов пока нет!', True, WHITE)
            surface.blit(no_records, (WIDTH // 2 - no_records.get_width() // 2, 200))
        else:
            for i, record in enumerate(self.game.records[:10]):
                record_text = font_small.render(f"{i+1}. {record['name']} - {record['score']} очков ({record['difficulty']})", True, WHITE)
                surface.blit(record_text, (WIDTH // 2 - 200, 120 + i * 40))
        
        back_rect = pygame.Rect(WIDTH // 2 - 100, 500, 200, 50)
        pygame.draw.rect(surface, BLUE, back_rect)
        back_text = font_medium.render('НАЗАД', True, WHITE)
        surface.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, 515))
    
    def handle_click(self, pos):
        if self.current_screen == 'main':
            # Проверка кнопок главного меню
            buttons = [
                (pygame.Rect(WIDTH // 2 - 100, 200, 200, 50), 'start'),
                (pygame.Rect(WIDTH // 2 - 150, 320, 80, 40), 'easy'),
                (pygame.Rect(WIDTH // 2 - 50, 320, 80, 40), 'medium'),
                (pygame.Rect(WIDTH // 2 + 50, 320, 80, 40), 'hard'),
                (pygame.Rect(WIDTH // 2 - 100, 380, 200, 50), 'records'),
                (pygame.Rect(WIDTH // 2 - 100, 450, 200, 50), 'exit')
            ]
            
            for rect, action in buttons:
                if rect.collidepoint(pos):
                    if action == 'start':
                        self.game.set_difficulty(self.selected_difficulty)
                        self.game.reset_game()
                        return 'game'
                    elif action in ['easy', 'medium', 'hard']:
                        self.selected_difficulty = action
                    elif action == 'records':
                        self.current_screen = 'records'
                    elif action == 'exit':
                        pygame.quit()
                        sys.exit()
                        
        elif self.current_screen == 'records':
            back_rect = pygame.Rect(WIDTH // 2 - 100, 500, 200, 50)
            if back_rect.collidepoint(pos):
                self.current_screen = 'main'
                
        return None

def main():
    game = Game()
    menu = Menu(game)
    current_screen = 'menu'  # menu, game
    
    while True:
        if current_screen == 'menu':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    result = menu.handle_click(event.pos)
                    if result == 'game':
                        current_screen = 'game'
            
            menu.draw(screen)
            
        elif current_screen == 'game':
            result = game.handle_keys()
            if result == 'menu':
                current_screen = 'menu'
                continue
                
            game.update()
            game.draw(screen)
            
            # Автоматическое возвращение в меню после game over
            if game.game_over:
                pygame.display.flip()
                pygame.time.delay(2000)  # Задержка перед показом меню
                current_screen = 'menu'
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()