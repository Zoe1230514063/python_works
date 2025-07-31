import pygame
import sys
import os

# 初始化Pygame
pygame.init()

# 常量定义
BLACK = (0, 0, 0)  # 黑子颜色
WHITE = (255, 255, 255)  # 白子颜色
BOARD_COLOR = (188, 122, 66)  # 棋盘颜色
TEXT_COLOR = (255, 0, 0)  # 文字颜色
BOARD_SIZE = 15  # 棋盘大小
CELL_SIZE = 40  # 格子大小
MARGIN = 30  # 棋盘边缘留白
WIDTH = HEIGHT = MARGIN * 2 + (BOARD_SIZE - 1) * CELL_SIZE  # 窗口的宽、高
VALID_RADIUS = 15  # 有效点击半径

# 字体定义
FONT_PATH = 'C:/Windows/Fonts/simhei.ttf'
if not os.path.exists(FONT_PATH):
    print(f"错误：请将中文文件放到：{FONT_PATH}中！")
    sys.exit()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("五子棋小游戏")

# 字体
menu_font = pygame.font.Font(FONT_PATH, 50)
btn_font = pygame.font.Font(FONT_PATH, 36)
game_font = pygame.font.Font(FONT_PATH, 22)

# 菜单
MENU_BG = (60, 60, 60)
BTN_START_RECT = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 60)
BTN_QUIT_RECT  = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 60)

# 游戏数据结构
board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
record_black = []  # 记录黑子位置编号
record_white = []  # 记录白子位置编号
current_player = 'black'
game_over = False


def get_chinese_player(player):
    return "黑棋" if player == 'black' else "白棋"


def position_to_index(row, col):
    return row * BOARD_SIZE + col + 1


def index_to_position(index):
    index -= 1
    row = index // BOARD_SIZE
    col = index % BOARD_SIZE
    return row, col


def check_win(row, col, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 5:
            return True
    return False


def draw_board():
    screen.fill(BOARD_COLOR)
    # 绘制棋盘网格
    for i in range(BOARD_SIZE):
        start = MARGIN + i * CELL_SIZE
        pygame.draw.line(screen, BLACK, (MARGIN, start), (WIDTH - MARGIN, start))
        pygame.draw.line(screen, BLACK, (start, MARGIN), (start, HEIGHT - MARGIN))
    # 绘制棋子
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] is not None:
                color = BLACK if board[row][col] == 'black' else WHITE
                pos = (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE)
                pygame.draw.circle(screen, color, pos, CELL_SIZE // 2 - 2)


def show_status(text):
    text_surface = game_font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (MARGIN, 5))


def show_winner_popup(winner):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    popup_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 75, 300, 150)
    pygame.draw.rect(screen, WHITE, popup_rect)

    big = pygame.font.Font(FONT_PATH, 40)
    screen.blit(big.render(f"{winner} 胜利！", True, TEXT_COLOR),
                big.render(f"{winner} 胜利！", True, TEXT_COLOR).get_rect(center=(WIDTH // 2, HEIGHT // 2 - 15)))

    small = pygame.font.Font(FONT_PATH, 25)
    screen.blit(small.render("按任意键返回主菜单", True, BLACK),
                small.render("按任意键返回主菜单", True, BLACK).get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))

def menu_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_START_RECT.collidepoint(event.pos):
                    reset_game()
                    game_loop()
                    return
                elif BTN_QUIT_RECT.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill(MENU_BG)
        title = menu_font.render("五子棋小游戏", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 3)))

        # 绘制 Start / Quit 按钮
        pygame.draw.rect(screen, WHITE, BTN_START_RECT, border_radius=8)
        pygame.draw.rect(screen, WHITE, BTN_QUIT_RECT,  border_radius=8)

        start_txt = btn_font.render("Start", True, BLACK)
        quit_txt  = btn_font.render("Quit",  True, BLACK)
        screen.blit(start_txt, start_txt.get_rect(center=BTN_START_RECT.center))
        screen.blit(quit_txt,  quit_txt.get_rect(center=BTN_QUIT_RECT.center))

        pygame.display.flip()

def reset_game():
    global board, record_black, record_white, current_player, game_over
    board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    record_black = []
    record_white = []
    current_player = 'black'
    game_over = False


def game_loop():
    global current_player, game_over
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                col = round((x - MARGIN) / CELL_SIZE)
                row = round((y - MARGIN) / CELL_SIZE)
                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] is None:
                    if event.button == 1:   # 左键黑
                        board[row][col] = 'black'
                        record_black.append(position_to_index(row, col))
                        if check_win(row, col, 'black'):
                            game_over = True
                        else:
                            current_player = 'white'
                    elif event.button == 3: # 右键白
                        board[row][col] = 'white'
                        record_white.append(position_to_index(row, col))
                        if check_win(row, col, 'white'):
                            game_over = True
                        else:
                            current_player = 'black'
            # 按任意键返回主菜单
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN) and game_over:
                reset_game()        # 重置棋盘
                menu_loop()         # 重新进入主菜单
                return              # 退出当前 game_loop

        draw_board()
        chinese_player = get_chinese_player(current_player)
        if game_over:
            show_status(f"游戏结束 - {chinese_player} 获胜！")
            show_winner_popup(chinese_player)
        else:
            show_status(f"当前玩家：{chinese_player}")
        pygame.display.flip()


if __name__ == "__main__":
    menu_loop()