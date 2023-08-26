import pygame

def collision(outer,inner):
    return outer[0]<=inner[0] and outer[0]+40>=inner[0] and outer[1]<=inner[1] and outer[1]+40>=inner[1]

def welcome(screen):
    pygame.init()

    #Basic visual details
    screen.fill((131,238,255))
    
    #####################
    #Title
    title=[pygame.Rect(200,40,400,100),pygame.Rect(210,50,380,80)]
    pygame.draw.rect(screen,(139,69,19),title[0])
    pygame.draw.rect(screen,(255,222,173),title[1])
    fontTitle=pygame.font.Font("./font/Unicode/times.ttf",50)
    textTitle=fontTitle.render("Cờ gánh",True, (0,0,0))
    screen.blit(textTitle,(320,60))
    #####################
    #Priority
    priority=pygame.Rect(20,200,760,50)
    pygame.draw.rect(screen,((255,222,173)),priority)
    font=pygame.font.Font("./font/Unicode/times.ttf",25)
    textFirst=font.render("Chọn người chơi đi trước:",True,(0,0,0))
    textRan=font.render("Agent Random/Người",True,(0,0,0))
    textBot=font.render("Bot",True,(0,0,0))
    screen.blit(textFirst,(30,210))
    checkPos=[(350,205),(650,205)]
    uncheck=pygame.transform.scale(pygame.image.load("./img/uncheck.png"),(40,40))
    checked=pygame.transform.scale(pygame.image.load("./img/check.png"),(40,40))
    check=[uncheck,checked]
    screen.blit(textRan,(400,210))
    screen.blit(textBot,(700,210))
    #####################
    #Level
    levelBlock=pygame.Rect(20,310,760,100)
    pygame.draw.rect(screen,((255,222,173)),levelBlock)
    textLevel=font.render("Chọn cấp độ chơi của Bot:",True,(0,0,0))
    levelCoor=[(i*110+350,320) for i in range(4)]
    screen.blit(textLevel,(30,345))
    for i in range(4):
        levelText=font.render(str(i+1),True,(0,0,0))
        screen.blit(levelText,(levelCoor[i][0]+15,levelCoor[i][1]+50))
    #####################

    #Play button
    human=pygame.Rect(166,470,150,70)
    play=pygame.Rect(482,470,150,70)
    pygame.draw.rect(screen,((50,205,50)),human)
    pygame.draw.rect(screen,((50,205,50)),play)
    textVSHuman=font.render("VS người",True,(0,0,0))
    screen.blit(textVSHuman,(190,487))
    textVSRandom=font.render("VS random",True,(0,0,0))
    screen.blit(textVSRandom,(500,487))
    #####################
    pygame.display.update()
    running = True
    player=[0,0]
    level=[0,0,0,0]
    playerOut=-1
    levelOut=-1
    while running:
        screen.blit(check[player[0]],checkPos[0])
        screen.blit(check[player[1]],checkPos[1])
        for i in range(4):
            screen.blit(check[level[i]],levelCoor[i])
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONUP:
                pos=pygame.mouse.get_pos()
                for coor in range(2):
                    if(collision(checkPos[coor],pos)):
                        player[coor]=(player[coor]+1)%2
                        player[(coor+1)%2]=0
                for coor in range(4):
                    if(collision(levelCoor[coor],pos)):
                        level[coor]=(level[coor]+1)%2
                        for index in range(4):
                            if(index!=coor):
                                level[index]=0
                if(play.collidepoint(pos) or human.collidepoint(pos)):
                    for i in range(2):
                        if(player[i]==1):
                            playerOut=i
                    for i in range(4):
                        if(level[i]==1):
                            levelOut=i
                    if(playerOut==-1):
                        err=font.render("Chưa chọn người đi trước!!",True,(200,0,0))
                        screen.blit(err,(30,250))
                    if(levelOut==-1):
                        err=font.render("Chưa chọn cấp độ!!",True,(200,0,0))
                        screen.blit(err,(30,410))
                    if(playerOut!=-1 and levelOut!=-1):
                        running=False
                        if(play.collidepoint(pos)):
                            return playerOut,levelOut,1
                        if(human.collidepoint(pos)):
                            return playerOut,levelOut,0
            if event.type==pygame.QUIT:
                running=False
                return -1,-1,-1
            playerOut=-1
            levelOut=-1
        pygame.display.update()