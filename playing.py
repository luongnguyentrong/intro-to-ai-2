import pygame
def play(board2,screen,counter,moves):
    print("check")
    moveSet={}
    for i in moves:
        start=(i.pos_start.x,i.pos_start.y)
        end=(i.pos_end.x,i.pos_end.y)
        if(start in moveSet.keys()):
            moveSet[start].append(end)
        else:
            moveSet[start]=[end]
    screen.fill((131,238,255))
    running=True
    #####################
    #Title
    title=[pygame.Rect(200,40,400,100),pygame.Rect(210,50,380,80)]
    pygame.draw.rect(screen,(139,69,19),title[0])
    pygame.draw.rect(screen,(255,222,173),title[1])
    fontTitle=pygame.font.Font("./font/Unicode/times.ttf",50)
    textTitle=fontTitle.render("Bước "+str(counter),True, (0,0,0))
    screen.blit(textTitle,(320,60))
    #####################
    #Board
    
    start=-1
    end=-1
    while running:
        board=[pygame.Rect(255,160,290,290),pygame.Rect(260,165,280,280)]
        pygame.draw.rect(screen,(139,69,19),board[0])
        pygame.draw.rect(screen,(255,222,173),board[1])
        pygame.draw.line(screen,(0,0,0),(260,165),(540,445),5)
        pygame.draw.line(screen,(0,0,0),(260,445),(540,165),5)
        pygame.draw.line(screen,(0,0,0),(400,165+26),(540-26,305),5)
        pygame.draw.line(screen,(0,0,0),(400,165+26),(260+26,305),5)
        pygame.draw.line(screen,(0,0,0),(400,445-26),(260+26,305),5)
        pygame.draw.line(screen,(0,0,0),(400,445-26),(540-26,305),5)
        for i in range(5):
            pygame.draw.line(screen,(0,0,0),(260+28+56*i,445),(260+28+56*i,165),5)
            pygame.draw.line(screen,(0,0,0),(260,165+28+56*i),(540,165+28+56*i),5)
        startSet=[[0]*5 for i in range(5)]
        endSet=[[0]*5 for i in range(5)]


        for i in range(5):
            for j in range(5):
                startLeft=j*57 + 260
                startTop=i*57 + 165
                init=(i,j)
                if(board2[i][j]==1):
                    if(start==-1 and (init in moveSet.keys())):
                        startSet[i][j]=pygame.Rect(startLeft,startTop,57,57)
                        pygame.draw.rect(screen,(85, 255, 0),startSet[i][j])
                    else:
                        if(start!=-1 and start[0]==i and start[1]==j):
                            startSet[i][j]=pygame.Rect(startLeft,startTop,57,57)
                            pygame.draw.rect(screen,(148, 148, 184),startSet[i][j])
                    pygame.draw.circle(screen,(200,0,0),(startLeft+26,startTop+26),15)
                elif (board2[i][j]==-1):
                    pygame.draw.circle(screen,(0,0,200),(startLeft+26,startTop+26),15)
                else:
                    if(start!=-1 and init in moveSet[start]):
                        endSet[i][j]=pygame.Rect(startLeft,startTop,57,57)
                        pygame.draw.rect(screen,(0, 230, 230),endSet[i][j])
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                return -1,-1
            if event.type==pygame.MOUSEBUTTONUP:
                for i in range(5):
                    for j in range(5):
                        if(start==-1 and startSet[i][j]!=0):
                            if startSet[i][j].collidepoint(event.pos):
                                
                                start=(i,j)
                                print(start)
                        elif(start!=-1 and startSet[i][j]!=0):
                            if start[0]==i and start[1]==j and startSet[i][j].collidepoint(event.pos):
                                start=-1
                        elif(start!=-1 and endSet[i][j]!=0):
                            if endSet[i][j].collidepoint(event.pos):
                                running=False
                                return start,(i,j)
        pygame.display.update()