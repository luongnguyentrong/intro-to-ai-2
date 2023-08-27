import welcome
import sys
import pygame
import board
import const


def setup():
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    pygame.display.set_caption("Bài tập lớn 2 - Game Playing")

    return screen


def main(board_state: list):
    pygame.init()

    screen = setup()

    # show welcome screen
    first_turn, level, mode = welcome.render(screen)

    if (first_turn == -1 and level == -1):
        print("Ambiguos user input!")
        sys.exit()

    # render board game
    board.render(screen=screen, board_state=board_state,
                 first_turn=first_turn, mode=mode, level=level + 1)


if __name__ == "__main__":
    # set fps
    clock = pygame.time.Clock()
    clock.tick(60)

    # init state
    init_state = [[1, 1, 1, -1, -1],
                  [1, 0, 0, 0, -1],
                  [1, 0, 0, 0, -1],
                  [1, 0, 0, 0, -1],
                  [1, 1, -1, -1, -1]]

    main(board_state=init_state)
