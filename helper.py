import pygame
import const
from const import IMAGE_SIZE, FONT_BOLD_PATH, FONT_PATH, TEXT_COLOR

def collision(outer, inner):
    return outer[0] <= inner[0] and \
            outer[0] + IMAGE_SIZE >= inner[0] and \
                outer[1] <= inner[1] and \
                    outer[1] + IMAGE_SIZE >= inner[1]


def draw_title(screen: pygame.Surface):
    fontTitle = pygame.font.Font(FONT_BOLD_PATH, 50)
    textTitle = fontTitle.render("CỜ GÁNH", True, TEXT_COLOR)

    text_rect = textTitle.get_rect()

    top_offset = 60
    screen.blit(textTitle, (const.SCREEN_WIDTH /
                2 - text_rect.width / 2, top_offset))

    return text_rect.bottom

def draw_pick_player(screen: pygame.Surface, wrapper_color: pygame.Color):
    container_width, container_height = const.CONTAINER_WIDTH, 80

    # draw container
    container = pygame.Rect(
        (const.SCREEN_WIDTH - container_width) / 2, 200, container_width, container_height)
    pygame.draw.rect(screen, wrapper_color, container,
                     border_radius=int(container_height / 2))

    bold_font = pygame.font.Font(FONT_BOLD_PATH, 25)
    textFirst = bold_font.render("Chọn người chơi trước:", True, TEXT_COLOR)

    font = pygame.font.Font(FONT_PATH, 25)
    textRan = font.render("Agent Random/Người", True, TEXT_COLOR)
    textBot = font.render("Bot", True, TEXT_COLOR)

    text_rect = textFirst.get_rect()
    text_height = container.top + container.height / 2 - text_rect.height / 2

    # left from container
    left_border = container.left + 50

    screen.blit(textFirst, (left_border, text_height))

    offset = 80
    box_offset = 20

    text_left_1 = left_border + text_rect.width + offset

    screen.blit(textRan, (text_left_1 + IMAGE_SIZE + box_offset, text_height))

    text_rect = textRan.get_rect()
    text_left_2 = text_left_1 + text_rect.width + offset
    screen.blit(textBot, (text_left_2 + IMAGE_SIZE + box_offset, text_height))

    return container, text_left_1, text_left_2

def draw_pick_level(screen: pygame.Surface, container: pygame.Rect, wrapper_color: pygame.Color):
    container_width, container_height = const.CONTAINER_WIDTH, 100
    second_container = pygame.Rect(
        (const.SCREEN_WIDTH - container_width) / 2, container.bottom + 50, container_width, container_height)

    pygame.draw.rect(screen, wrapper_color, second_container,
                     border_radius=int(second_container.height / 2))

    # draw inside second container
    bold_font = pygame.font.Font(FONT_BOLD_PATH, 25)
    textLevel = bold_font.render("Chọn cấp độ Bot:", True, TEXT_COLOR)

    text_rect = textLevel.get_rect()
    text_height = second_container.top + \
        second_container.height / 2 - text_rect.height / 2

    left_border = second_container.left + 50
    screen.blit(textLevel, (left_border, text_height))

    box_offset = 110

    font = pygame.font.Font(FONT_PATH, 25)

    box_left = 527

    level_height = second_container.top + second_container.height / 2 - IMAGE_SIZE
    level_coors = [(i*box_offset + box_left, level_height) for i in range(const.LEVEL_COUNT)]

    height_offset = 50
    for i in range(const.LEVEL_COUNT):
        levelText = font.render(str(i+1), True, TEXT_COLOR)
        screen.blit(levelText, (level_coors[i][0] + 15, level_coors[i][1] + height_offset))

    return second_container, level_coors 

def draw_play_button(screen: pygame.Surface, container: pygame.Rect):
    button_color = pygame.Color("#C70039")
    button_text_color = pygame.Color("#FFE5E5")

    button_width, button_height = 270, 70

    button_offset = 80
    button_top = container.bottom + button_offset

    button_padding = 30

    human_left = const.SCREEN_WIDTH / 2 - button_padding / 2 - button_width
    human = pygame.Rect(human_left, button_top, button_width, button_height)

    play_left = const.SCREEN_WIDTH / 2 + button_padding / 2 
    play = pygame.Rect(play_left, button_top, button_width, button_height)
    pygame.draw.rect(screen, button_color, human,
                     border_radius=int(button_height / 2))
    pygame.draw.rect(screen, button_color, play,
                     border_radius=int(button_height / 2))

    font = pygame.font.Font(FONT_BOLD_PATH, 25)
    textVSHuman = font.render("Đánh với người", True, button_text_color)
    textVSRandom = font.render("Đánh ngẫu nhiên", True, button_text_color)

    text_rect = textVSHuman.get_rect()

    human_text_left = human.left + human.width / 2 - textVSHuman.get_rect().width / 2
    screen.blit(textVSHuman, (human_text_left, int(human.top + human.height / 2 - text_rect.height / 2)))

    random_text_left = play.left + play.width / 2 - textVSRandom.get_rect().width / 2
    screen.blit(textVSRandom, (random_text_left, int(play.top + human.height / 2 - text_rect.height / 2)))

    return play, human