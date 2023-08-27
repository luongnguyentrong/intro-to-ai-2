import pygame
import minimax
import const
import random

BOARD_SIZE = 400
board_left = const.SCREEN_WIDTH / 2 - BOARD_SIZE / 2
board_top = 165
board_gap = BOARD_SIZE / 4

CHESS_SIZE = 16

def draw_board(screen: pygame.Surface, board_state: list, show_moves=None):
    border_thick = 5

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
    for i in range(1, 4):
        pygame.draw.line(screen, const.TEXT_COLOR, (board_left + board_gap*i, board_top),
                         (board_left + board_gap*i, board_top + BOARD_SIZE), int(border_thick / 2))
        pygame.draw.line(screen, const.TEXT_COLOR, (board_left,
                                                    board_top + board_gap * i), (board_left + BOARD_SIZE, board_top + board_gap * i), int(border_thick / 2))

    RED_CHESS_COLOR = pygame.Color("#9A3B3B")
    BLUE_CHESS_COLOR = pygame.Color("#793FDF")

    chess_blocks = []
    for i in range(5):
        for j in range(5):
            left = board_left + j * board_gap
            top = board_top + i * board_gap

            if (show_moves is not None and board_state[i][j] == show_moves):
                chess_block = pygame.Rect(
                    left - CHESS_SIZE, top - CHESS_SIZE, CHESS_SIZE * 2, CHESS_SIZE * 2)

                pygame.draw.rect(screen, pygame.Color("#F4EEEE"), chess_block)

                chess_blocks.append((chess_block, (i, j)))

            if (board_state[i][j] == 1):
                pygame.draw.circle(screen, BLUE_CHESS_COLOR,
                                   (left, top), CHESS_SIZE)
            elif (board_state[i][j] == -1):
                pygame.draw.circle(screen, RED_CHESS_COLOR,
                                   (left, top), CHESS_SIZE)

    return chess_blocks

def draw_current_step(screen: pygame.Surface, current_step: int):
    container_width, container_height = 400, 80

    left = const.SCREEN_WIDTH / 2 - container_width / 2
    container = pygame.Rect(left, 50, container_width, container_height)
    pygame.draw.rect(screen, pygame.Color("#CEDEBD"), container)

    fontTitle = pygame.font.Font("fonts/static/Montserrat-Bold.ttf", 30)
    textTitle = fontTitle.render(f"Bước {current_step}", True, const.TEXT_COLOR)

    text_rect = textTitle.get_rect()

    text_left = const.SCREEN_WIDTH / 2 - text_rect.width / 2
    text_top = container.top + container.height / 2 - text_rect.height / 2
    screen.blit(textTitle, (text_left, text_top))

def apply_move(board_state: list, move: tuple, player):
    # save current state
    next_state = minimax.copy_board(current_board=board_state)
    prev_board = board_state

    # apply bot move
    minimax.change_board(current_board=next_state, move=move, player=player)

    # update current state
    current_board = next_state

    return prev_board, current_board

def draw_winner(screen: pygame.Surface, board_state: list, first_turn: int):
    # get winner code
    winner_code = None
    for row in board_state:
        for cell in row:
            if cell != 0:
                winner_code = cell
                break

    if first_turn == 1 and winner_code == -1:
        winner = "Người chơi"
    else:
        winner = "Bot"

    # draw outside container
    container_width, container_height = 400, 80

    container_top = board_top + BOARD_SIZE + 50

    left = const.SCREEN_WIDTH / 2 - container_width / 2
    container = pygame.Rect(left, container_top, container_width, container_height)
    pygame.draw.rect(screen, pygame.Color("#FF6969"), container, border_radius=int(container_height / 2))

    fontTitle = pygame.font.Font("fonts/static/Montserrat-Bold.ttf", 30)

    textTitle = fontTitle.render(f"{winner} thắng !", True, const.TEXT_COLOR)

    text_rect = textTitle.get_rect()

    text_left = const.SCREEN_WIDTH / 2 - text_rect.width / 2
    text_top = container.top + container.height / 2 - text_rect.height / 2
    screen.blit(textTitle, (text_left, text_top))
    

def render(screen: pygame.Surface, board_state: list, first_turn: int, mode: int, level):
    current_turn = 1

    if (first_turn == 1):
        human = -1
    else:
        human = 1

    chess_blocks = []
    next_move_blocks = []

    # save board state
    prev_board = minimax.copy_board(board_state)
    current_board = minimax.copy_board(board_state)

    current_step = 1

    running = True
    while running:
        for event in pygame.event.get():
            # quite game
            if event.type == pygame.QUIT:
                running = False


        if not minimax.is_finished(current_board=current_board):
            screen.fill(const.BACKGROUND_COLOR)

            draw_current_step(screen=screen, current_step=current_step)

            # draw current board state
            if current_turn == human:
                if mode == 0:
                    # Human
                    chess_blocks = draw_board(screen=screen, board_state=current_board,
                                            show_moves=current_turn)
                    # draw next possible moves
                    for block, _ in next_move_blocks:
                        pygame.draw.rect(screen, pygame.Color("#FF6969"), block)

                else:
                    # Random Agent
                    moves = minimax.get_all_moves(current_board=current_board, previous_board=prev_board, player=current_turn)

                    # pick a random move
                    random_move = random.choice(moves)

                    # apply move
                    prev_board, current_board = apply_move(board_state=current_board, move=random_move, player=current_turn)

                    # flip current turn
                    current_turn *= -1

                    draw_board(screen=screen, board_state=current_board)

            else:
                # get bot turn
                move = minimax.move(prev_board=prev_board, board=current_board, player=current_turn, tree_depth=level)

                # apply move
                prev_board, current_board = apply_move(current_board, move=move, player=current_turn)

                # flip current turn
                current_turn *= -1

                draw_board(screen=screen, board_state=current_board)


            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if mode == 0 and current_turn == human:
                        picked = False

                        for block, pos in chess_blocks:
                            if block.collidepoint(event.pos):
                                # reset next_move_blocks
                                next_move_blocks = []
                            
                                # create next pickable blocks
                                possible_moves = minimax.find_near_cell(
                                    current_board, pos, 0)

                                # create list of blocks to be drawn along with the moves
                                for cell in possible_moves:
                                    x, y = cell
                                    cell_block = pygame.Rect(
                                        board_left + board_gap * y - CHESS_SIZE, board_top + board_gap * x - CHESS_SIZE, CHESS_SIZE * 2, CHESS_SIZE * 2)

                                    pygame.draw.rect(
                                        screen, const.TEXT_COLOR, cell_block)

                                    next_move_blocks.append(
                                        (cell_block, (pos, cell)))

                                # to mark the below if block to not trigger
                                picked = True

                                break

                        if not picked:
                            for block, move in next_move_blocks:
                                if block.collidepoint(event.pos):
                                    # move board to new state
                                    minimax.change_board(
                                        current_board, move, player=current_turn)

                                    # rest chess_blocks 
                                    chess_blocks = []

                                    # reset next_move_blocks
                                    next_move_blocks = []

                                    # flip current turn
                                    current_turn *= -1
            
        else:
            draw_board(screen=screen, board_state=current_board)
            draw_winner(screen=screen, board_state=current_board, first_turn=first_turn)

        pygame.display.update()