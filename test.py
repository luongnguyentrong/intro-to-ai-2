import pygame
import welcome

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def setup():
    pygame.display.set_caption("Bài tập lớn 2 - Game Playing")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    return screen

def main():
    pygame.init()

    screen = setup()

    running = True
    clock = pygame.time.Clock()

    rect_width, rect_height = 100, 50

    # goFirst,level,mode = welcome.welcome(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(pygame.Color("#900C3F"))
        pygame.draw.rect(screen, pygame.Color("#F8DE22"), pygame.Rect(SCREEN_WIDTH / 2 - rect_width / 2, SCREEN_HEIGHT / 2 - rect_height / 2, rect_width, rect_height))
        # fontTitle=pygame.font.Font("fonts/Montserrat-VariableFont_wght.ttf", 50)
        fontTitle=pygame.font.Font("fonts/static/Montserrat-Bold.ttf", 50)

        fontTitle.bold = True
        textTitle=fontTitle.render("Cờ gánh",True, (0,0,0))

        screen.blit(textTitle,(320,60))

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

main()