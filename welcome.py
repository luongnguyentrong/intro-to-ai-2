import pygame
import helper
import const


def render(screen: pygame.Surface):
    pygame.init()

    # set background color
    screen.fill(pygame.Color("#FBF0B2"))

    helper.draw_title(screen=screen)

    # set color
    wrapper_color = pygame.Color("#CEDEBD")

    # draw options to select first player
    container, first_box_left, second_box_left = helper.draw_pick_player(screen=screen, wrapper_color=wrapper_color)

    # draw options to pick bot level
    second_container, level_coors = helper.draw_pick_level(screen=screen, container=container, wrapper_color=wrapper_color)

    # draw play button
    play, human = helper.draw_play_button(screen=screen, container=second_container)

    # event listener
    font = pygame.font.Font(const.FONT_PATH, 25)
    pygame.display.update()

    uncheck = pygame.image.load("./img/uncheck.png")
    checked = pygame.image.load("./img/check.png")

    box_height = container.top + container.height / 2 - uncheck.get_height() / 2
    checkPos = [(first_box_left, box_height), (second_box_left, box_height)]

    check = [uncheck, checked]
    running = True
    player = [0, 0]
    level = [0, 0, 0, 0]
    playerOut = -1
    levelOut = -1

    while running:
        # draw first option
        screen.blit(check[player[0]], checkPos[0])
        screen.blit(check[player[1]], checkPos[1])

        # draw level picked
        for i in range(const.LEVEL_COUNT):
            screen.blit(check[level[i]], level_coors[i])

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # save first player picked
                for coor in range(2):
                    if (helper.collision(checkPos[coor], pos)):
                        player[coor] = (player[coor] + 1) % 2
                        player[(coor + 1) % 2] = 0

                # save bot level picked
                for coor in range(const.LEVEL_COUNT):
                    if (helper.collision(level_coors[coor], pos)):
                        # toggle picked level value
                        level[coor] = (level[coor] + 1) % 2

                        # unset all other boxes
                        for index in range(4):
                            if (index != coor):
                                level[index] = 0

                if (play.collidepoint(pos) or human.collidepoint(pos)):
                    for i in range(2):
                        if (player[i] == 1):
                            playerOut = i

                    for i in range(const.LEVEL_COUNT):
                        if (level[i] == 1):
                            levelOut = i

                    if (playerOut == -1):
                        err = font.render(
                            "Bạn chưa chọn người đi trước!!", True, (200, 0, 0))
                        screen.blit(err, (30, 250))

                    if (levelOut == -1):
                        err = font.render(
                            "Bạn chưa chọn cấp độ!!", True, (200, 0, 0))
                        screen.blit(err, (30, 410))

                    if (playerOut != -1 and levelOut != -1):
                        running = False
                        if (play.collidepoint(pos)):
                            return playerOut, levelOut, const.GAME_MODE["RANDOM"]

                        if (human.collidepoint(pos)):
                            return playerOut, levelOut, const.GAME_MODE["HUMAN"]

            if event.type == pygame.QUIT:
                running = False
                return -1, -1, -1

            playerOut = -1
            levelOut = -1

        pygame.display.update()
