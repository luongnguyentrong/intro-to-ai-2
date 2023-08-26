import pygame
import const

TEXT_COLOR = pygame.Color("#3F1D38")
FONT_PATH = "fonts/static/Montserrat-Regular.ttf"


def collision(outer, inner):
    return outer[0] <= inner[0] and outer[0]+40 >= inner[0] and outer[1] <= inner[1] and outer[1]+40 >= inner[1]


def draw_title(screen: pygame.Surface):
    fontTitle = pygame.font.Font(FONT_PATH, 50)
    textTitle = fontTitle.render("CỜ GÁNH", True, TEXT_COLOR)

    text_rect = textTitle.get_rect()

    top_offset = 60
    screen.blit(textTitle, (const.SCREEN_WIDTH /
                2 - text_rect.width / 2, top_offset))

    return text_rect.bottom


def render(screen: pygame.Surface):
    pygame.init()

    # set background color
    screen.fill(pygame.Color("#FBF0B2"))

    draw_title(screen=screen)

    # set color
    wrapper_color = pygame.Color("#CEDEBD")

    # select first player
    container_width, container_height = 760, 80
    container = pygame.Rect(
        (const.SCREEN_WIDTH - container_width) / 2, 200, container_width, container_height)
    pygame.draw.rect(screen, wrapper_color, container,
                     border_radius=int(container_height / 2))

    font = pygame.font.Font(FONT_PATH, 25)
    textFirst = font.render("Chọn người chơi trước:", True, TEXT_COLOR)

    textRan = font.render("Agent Random/Người", True, TEXT_COLOR)
    textBot = font.render("Bot", True, TEXT_COLOR)

    text_rect = textFirst.get_rect()
    text_height = container.top + container.height / 2 - text_rect.height / 2

    screen.blit(textFirst, (50, text_height))

    screen.blit(textRan, (400, text_height))
    screen.blit(textBot, (700, text_height))

    checkPos = [(350, 205), (650, 205)]
    uncheck = pygame.transform.scale(
        pygame.image.load("./img/uncheck.png"), (40, 40))
    checked = pygame.transform.scale(
        pygame.image.load("./img/check.png"), (40, 40))

    check = [uncheck, checked]
    # Level
    container_width, container_height = 760, 100
    second_container = pygame.Rect(
        (const.SCREEN_WIDTH - container_width) / 2, container.bottom + 50, container_width, container_height)

    pygame.draw.rect(screen, wrapper_color, second_container, border_radius=int(second_container.height / 2))

    # draw inside second container
    textLevel = font.render("Chọn cấp độ Bot:", True, TEXT_COLOR)

    text_rect = textLevel.get_rect()
    text_height = second_container.top + second_container.height / 2 - text_rect.height / 2

    screen.blit(textLevel, (30, text_height))

    # draw level
    LEVEL_COUNT = 4

    levelCoor = [(i*110+350, 320) for i in range(LEVEL_COUNT)]

    for i in range(LEVEL_COUNT):
        levelText = font.render(str(i+1), True, (0, 0, 0))
        screen.blit(levelText, (levelCoor[i][0]+15, levelCoor[i][1]+50))
    #####################

    # draw play button
    button_offset = 100
    button_color = pygame.Color("#C70039")
    button_text_color = pygame.Color("#252B48")

    button_width, button_height = 200, 70

    button_top = second_container.bottom + button_offset

    human = pygame.Rect(166, button_top, button_width, button_height)
    play = pygame.Rect(482, button_top, button_width, button_height)
    pygame.draw.rect(screen, button_color, human, border_radius=int(button_height / 2))
    pygame.draw.rect(screen, button_color, play, border_radius=int(button_height / 2))

    textVSHuman = font.render("VS người", True, button_text_color)
    screen.blit(textVSHuman, (190, 487))
    textVSRandom = font.render("VS random", True, button_text_color)
    screen.blit(textVSRandom, (500, 487))
    #####################

    pygame.display.update()
    running = True
    player = [0, 0]
    level = [0, 0, 0, 0]
    playerOut = -1
    levelOut = -1
    while running:
        screen.blit(check[player[0]], checkPos[0])
        screen.blit(check[player[1]], checkPos[1])
        for i in range(4):
            screen.blit(check[level[i]], levelCoor[i])
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for coor in range(2):
                    if (collision(checkPos[coor], pos)):
                        player[coor] = (player[coor]+1) % 2
                        player[(coor+1) % 2] = 0
                for coor in range(4):
                    if (collision(levelCoor[coor], pos)):
                        level[coor] = (level[coor]+1) % 2
                        for index in range(4):
                            if (index != coor):
                                level[index] = 0
                if (play.collidepoint(pos) or human.collidepoint(pos)):
                    for i in range(2):
                        if (player[i] == 1):
                            playerOut = i
                    for i in range(4):
                        if (level[i] == 1):
                            levelOut = i
                    if (playerOut == -1):
                        err = font.render(
                            "Chưa chọn người đi trước!!", True, (200, 0, 0))
                        screen.blit(err, (30, 250))
                    if (levelOut == -1):
                        err = font.render(
                            "Chưa chọn cấp độ!!", True, (200, 0, 0))
                        screen.blit(err, (30, 410))
                    if (playerOut != -1 and levelOut != -1):
                        running = False
                        if (play.collidepoint(pos)):
                            return playerOut, levelOut, 1
                        if (human.collidepoint(pos)):
                            return playerOut, levelOut, 0
            if event.type == pygame.QUIT:
                running = False
                return -1, -1, -1
            playerOut = -1
            levelOut = -1
        pygame.display.update()
