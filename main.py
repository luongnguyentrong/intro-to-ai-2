import minmax as mm
import welcome
import random
import demo
import sys
import pygame
import playing
import time
import const

def setup():
    screen=pygame.display.set_mode((const.SCREEN_WIDTH ,const.SCREEN_HEIGHT))
    pygame.display.set_caption("Bài tập lớn 2 - Game Playing")

    return screen


def main():
    pygame.init() 

    while True:
        screen = setup()

        # show welcome screen
        goFirst, level, mode = welcome.render(screen)

        print(mode)
        #If user decided to escape
        if(goFirst ==-1 and level ==-1):
            print("Program exited.")
            sys.exit()

        ###############
        #Who get to go first
        if (goFirst==1): player=-1 
        else: player=1 
        ###############
        #Setting up board
        mm.board()
        ###############
        #Current board
        res=[mm.dupTable(mm.board.current_board)]
        ###############
        counter=0
        demo.move(mm.board.current_board,screen,counter)

        win=0
        while True:
            previous_board=mm.board.copy_board(mm.board.current_board)

            if (player==-1): #Bot -1
                move=mm.board.select_move(player,level)
                if move==None: 
                    win=1
                    break
            else:            #Random Agent 1
                valid_move_temp=mm.board.get_valid_moves(mm.board.current_board, mm.board.previous_board, player)
                if(len(valid_move_temp)==0):
                    win=-1
                    break
                if(mode==1):
                    index=random.randint(0,len(valid_move_temp)-1)
                    move=valid_move_temp[index]
                elif(mode==0):
                    a,b=playing.play(mm.board.current_board,screen,counter,valid_move_temp)
                    if(a==-1 and b==-1):
                        sys.exit()
                    move=mm.Move(mm.Position(a[0],a[1]),mm.Position(b[0],b[1]))
            #Move
            mm.board.act_move(mm.board.current_board,move,player)
            mm.board.previous_board=mm.board.copy_board(previous_board)
            counter+=1

            #Update to UI
            demo.move(mm.board.current_board,screen,counter)
            time.sleep(1)
            
            #Print to terminal for Debugging
            for i in range(5): print(mm.board.current_board[i])
            print()
            res.append(mm.dupTable(mm.board.current_board))
            player=-player
            if(counter>=100):
                score=0
                for i in range(5):
                    for j in range(5):
                        if(mm.board.current_board[i][j]==1): score-=1
                        elif(mm.board.current_board[i][j]==-1): score+=1
                if(score>0):
                    win=-1
                elif(score<0):
                    win=1
                else:
                    win=0
                break
        restart=demo.resDisOut(win,res,len(res),screen)
        res=[]
        mm.board.current_board=[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        mm.board.previous_board=[[]]
        if(restart):pass
        else: break


if __name__ == "__main__":
    clock = pygame.time.Clock()
    clock.tick(60)

    main()