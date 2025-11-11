import pygame
import sys
import numpy as np
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_SIZE = 3
SQUARE_SIZE = WIDTH // BOARD_SIZE
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

BG_COLOR = (0, 0, 0)
LINE_COLOR = (0, 0, 255)
CIRCLE_COLOR = (0, 255, 0)
CROSS_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Крестики-нолики с ИИ')

font = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 24)

try:
    move_sound = pygame.mixer.Sound('term 3/Lab 1/move.mp3')
except:
    move_sound = pygame.mixer.Sound(buffer=bytes([128] * 4000))
    move_sound.set_volume(0.3)

try:
    win_sound = pygame.mixer.Sound('term 3/Lab 1/levelcomplete.mp3')
except:
    win_sound = pygame.mixer.Sound(buffer=bytes([128] * 8000))
    win_sound.set_volume(0.5)

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.current_player = 1  # 1 - игрок (X), 2 - ИИ (O)
        self.game_over = False
        self.winner = None

    def draw_board(self):
        """Отрисовка игрового поля"""
        screen.fill(BG_COLOR)
        
        for i in range(1, BOARD_SIZE):
            y = i * SQUARE_SIZE
            pygame.draw.line(screen, LINE_COLOR, (0, y), (WIDTH, y), LINE_WIDTH)
        
        for i in range(1, BOARD_SIZE):
            x = i * SQUARE_SIZE
            pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, HEIGHT), LINE_WIDTH)

    def draw_figures(self):
        """Отрисовка крестиков и ноликов"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == 1:  # Крестик
                    self.draw_x(row, col)
                elif self.board[row][col] == 2:  # Нолик
                    self.draw_o(row, col)

    def draw_x(self, row, col):
        """Отрисовка крестика"""
        x_pos = col * SQUARE_SIZE
        y_pos = row * SQUARE_SIZE
        
        pygame.draw.line(screen, CROSS_COLOR,
                        (x_pos + SPACE, y_pos + SPACE),
                        (x_pos + SQUARE_SIZE - SPACE, y_pos + SQUARE_SIZE - SPACE),
                        CROSS_WIDTH)
        pygame.draw.line(screen, CROSS_COLOR,
                        (x_pos + SQUARE_SIZE - SPACE, y_pos + SPACE),
                        (x_pos + SPACE, y_pos + SQUARE_SIZE - SPACE),
                        CROSS_WIDTH)

    def draw_o(self, row, col):
        """Отрисовка нолика"""
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)

    def make_move(self, row, col, player):
        """Сделать ход"""
        self.board[row][col] = player
        move_sound.play()

    def is_cell_empty(self, row, col):
        """Проверка, свободна ли клетка"""
        return self.board[row][col] == 0

    def is_board_full(self):
        """Проверка, заполнена ли доска"""
        return np.all(self.board != 0)

    def check_winner(self, player):
        """Проверка победы игрока"""
        for row in range(BOARD_SIZE):
            if all(self.board[row] == player):
                return True
        
        for col in range(BOARD_SIZE):
            if all(self.board[:, col] == player):
                return True
        
        if all(self.board.diagonal() == player):
            return True
        if all(np.fliplr(self.board).diagonal() == player):
            return True
        
        return False

    def minimax(self, board, depth, is_maximizing):
        """Алгоритм minimax для ИИ"""
        if self.check_winner(2):  
            return 1
        elif self.check_winner(1):  
            return -1
        elif self.is_board_full():  
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if board[row][col] == 0:
                        board[row][col] = 2
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if board[row][col] == 0:
                        board[row][col] = 1
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = 0
                        best_score = min(score, best_score)
            return best_score

    def find_best_move(self):
        """Найти лучший ход для ИИ с помощью minimax"""
        best_score = -float('inf')
        best_move = None
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_cell_empty(row, col):
                    self.board[row][col] = 2
                    score = self.minimax(self.board, 0, False)
                    self.board[row][col] = 0
                    
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        return best_move

    def ai_turn(self):
        """Ход ИИ"""
        best_move = self.find_best_move()
        if best_move:
            row, col = best_move
            self.make_move(row, col, 2)
            return True
        return False

    def draw_game_over_screen(self):
        """Отрисовка экрана окончания игры"""
        if self.winner == 1:
            text = "Вы выиграли!"
            color = CROSS_COLOR
        elif self.winner == 2:
            text = "ИИ выиграл!"
            color = CIRCLE_COLOR
        else:
            text = "Ничья!"
            color = TEXT_COLOR
        
        overlay = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, HEIGHT // 2 - 50))
        
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        
        restart_text = font_small.render("Нажмите R для новой игры", True, TEXT_COLOR)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(restart_text, restart_rect)

    def reset_game(self):
        """Сброс игры"""
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.current_player = 1
        self.game_over = False
        self.winner = None

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                if event.key == pygame.K_ESCAPE:
                    return False
            
            if (event.type == pygame.MOUSEBUTTONDOWN and 
                not self.game_over and 
                self.current_player == 1):
                
                mouse_x, mouse_y = event.pos
                col = mouse_x // SQUARE_SIZE
                row = mouse_y // SQUARE_SIZE
                
                if (0 <= row < BOARD_SIZE and 
                    0 <= col < BOARD_SIZE and 
                    self.is_cell_empty(row, col)):
                    
                    self.make_move(row, col, self.current_player)
                    
                    if self.check_winner(self.current_player):
                        self.game_over = True
                        self.winner = self.current_player
                        win_sound.play()
                    elif self.is_board_full():
                        self.game_over = True
                        self.winner = 0
                    else:
                        self.current_player = 2
        
        return True

    def run(self):
        """Основной игровой цикл"""
        running = True
        
        while running:
            running = self.handle_events()
            
            if not self.game_over and self.current_player == 2:
                pygame.time.delay(500)
                if self.ai_turn():
                    if self.check_winner(2):
                        self.game_over = True
                        self.winner = 2
                        win_sound.play()
                    elif self.is_board_full():
                        self.game_over = True
                        self.winner = 0
                    else:
                        self.current_player = 1
            
            self.draw_board()
            self.draw_figures()
            
            if self.game_over:
                self.draw_game_over_screen()
            
            pygame.display.update()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()