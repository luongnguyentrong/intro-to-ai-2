import pygame
import welcome
import const
from minimax import move

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


def setup():
    pygame.display.set_caption("Bài tập lớn 2 - Game Playing")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    return screen


def draw_board(screen: pygame.Surface, board: list):
    BOARD_SIZE = 400
    border_thick = 5

    board_left = const.SCREEN_WIDTH / 2 - BOARD_SIZE / 2
    board_top = 165

    # draw border
    border_left, border_top = board_left - border_thick, board_top - border_thick
    border_size = BOARD_SIZE + 2 * border_thick

    border = pygame.Rect(border_left, border_top, border_size, border_size)
    pygame.draw.rect(screen, const.TEXT_COLOR, border)

    # draw inner board
    board_inner = pygame.Rect(
        board_left, board_top, BOARD_SIZE, BOARD_SIZE)
    pygame.draw.rect(screen, const.BACKGROUND_COLOR, board_inner)

    # draw crosses
    pygame.draw.line(screen, const.TEXT_COLOR, (board_left, board_top),
                     (board_left + BOARD_SIZE, board_top + BOARD_SIZE), border_thick)
    pygame.draw.line(screen, const.TEXT_COLOR, (board_left, board_top +
                                                BOARD_SIZE), (board_left + BOARD_SIZE, board_top), border_thick)
    pygame.draw.line(screen, const.TEXT_COLOR, (int(board_left + BOARD_SIZE / 2), board_top),
                     (board_left + BOARD_SIZE, board_top + BOARD_SIZE / 2), border_thick)
    pygame.draw.line(screen, const.TEXT_COLOR, (board_left, board_top + BOARD_SIZE / 2),
                     (int(board_left + BOARD_SIZE / 2), board_top), border_thick)
    pygame.draw.line(screen, const.TEXT_COLOR, (board_left, board_top + BOARD_SIZE / 2),
                     (int(board_left + BOARD_SIZE / 2), board_top + BOARD_SIZE), border_thick)
    pygame.draw.line(screen, const.TEXT_COLOR, (int(board_left + BOARD_SIZE / 2), board_top + BOARD_SIZE),
                     (board_left + BOARD_SIZE, board_top + BOARD_SIZE / 2), border_thick)

    # draw straight lines
    board_gap = BOARD_SIZE / 4
    for i in range(1, 4):
        pygame.draw.line(screen, const.TEXT_COLOR, (board_left + board_gap*i, board_top),
                         (board_left + board_gap*i, board_top + BOARD_SIZE), int(border_thick / 2))
        pygame.draw.line(screen, const.TEXT_COLOR, (board_left,
                                                    board_top + board_gap * i), (board_left + BOARD_SIZE, board_top + board_gap * i), int(border_thick / 2))

    RED_CHESS_COLOR = pygame.Color("#9A3B3B")
    BLUE_CHESS_COLOR = pygame.Color("#793FDF")
    CHESS_SIZE = 15

    for i in range(5):
        for j in range(5):
            left = board_left + j * board_gap
            top = board_top + i * board_gap
            if (board[i][j] == 1):
                pygame.draw.circle(screen, BLUE_CHESS_COLOR, (left, top), CHESS_SIZE)
            elif (board[i][j] == -1):
                pygame.draw.circle(screen, RED_CHESS_COLOR, (left, top), CHESS_SIZE)


def main(board):
    pygame.init()

    screen = setup()

    running = True
    clock = pygame.time.Clock()

    screen.fill(const.BACKGROUND_COLOR)

    # Board
    draw_board(screen=screen, board=board)
    # goFirst,level,mode = welcome.welcome(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        # flip() the display to put your work on screen
        pygame.display.update()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


def test():
    board = [[1, 1, 1, -1, -1],
             [1, 0, 0, 0, -1],
             [1, 0, 0, 0, -1],
             [1, 0, 0, 0, -1],
             [1, 1, -1, -1, -1]]

    print(move(None, board, 1, 100, 100))


if __name__ == "__main__":
    board = [[1, 1, 1, -1, -1],
             [1, 0, 0, 0, -1],
             [1, 0, 0, 0, -1],
             [1, 0, 0, 0, -1],
             [1, 1, -1, -1, -1]]

    main(board=board)
