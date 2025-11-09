import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 300, 350  # sedikit lebih tinggi untuk teks hasil
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // 3
CIRCLE_RADIUS = 40
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = 30

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
TEXT_COLOR = (255, 255, 255)

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe - Minimax AI')
screen.fill(BG_COLOR)

# Fonts
font = pygame.font.SysFont(None, 40)

# Board
board = [['' for _ in range(3)] for _ in range(3)]

# Draw lines
def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, WIDTH), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, WIDTH), LINE_WIDTH)

draw_lines()

# Draw figures
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                          int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)

# Check winner
def check_winner(player):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Check empty cells
def empty_cells():
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == '']

# Minimax algorithm
def minimax(is_maximizing):
    if check_winner('O'):
        return 1
    if check_winner('X'):
        return -1
    if not empty_cells():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for (r, c) in empty_cells():
            board[r][c] = 'O'
            score = minimax(False)
            board[r][c] = ''
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for (r, c) in empty_cells():
            board[r][c] = 'X'
            score = minimax(True)
            board[r][c] = ''
            best_score = min(best_score, score)
        return best_score

# Best move for AI
def ai_move():
    best_score = -math.inf
    move = None
    for (r, c) in empty_cells():
        board[r][c] = 'O'
        score = minimax(False)
        board[r][c] = ''
        if score > best_score:
            best_score = score
            move = (r, c)
    if move:
        board[move[0]][move[1]] = 'O'

# Display result text
def show_result(text):
    label = font.render(text, True, TEXT_COLOR)
    text_rect = label.get_rect(center=(WIDTH/2, HEIGHT - 25))
    screen.blit(label, text_rect)

# Game loop
player_turn = True
game_over = False
result_text = ''

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if player_turn and not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                if mouseY < WIDTH:
                    clicked_row = int(mouseY // SQUARE_SIZE)
                    clicked_col = int(mouseX // SQUARE_SIZE)

                    if board[clicked_row][clicked_col] == '':
                        board[clicked_row][clicked_col] = 'X'
                        if check_winner('X'):
                            result_text = 'YOU WIN!'
                            game_over = True
                        elif not empty_cells():
                            result_text = 'DRAW!'
                            game_over = True
                        player_turn = False

        if not player_turn and not game_over:
            ai_move()
            if check_winner('O'):
                result_text = 'AI WINS!'
                game_over = True
            elif not empty_cells():
                result_text = 'DRAW!'
                game_over = True
            player_turn = True

    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    if game_over:
        show_result(result_text)
    pygame.display.update()
