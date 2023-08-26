from select import select


def dupTable(base):
    newer=[]
    for i in base:
        newer.append(list(i))
    return newer

class Position():
    def __init__(self, x=0, y=0):
        self.x=x
        self.y=y
    def __eq__(self, position):
        if (self.x==position.x) and (self.y==position.y): return True
        return False

class Move():
    def __init__(self, pos_start, pos_end):
        self.pos_start=pos_start
        self.pos_end=pos_end

class board:
    current_board=[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    previous_board=[[]]
    turn=0
    def __init__(self):
        for i in range(5):
            if i==0:
                for j in range(5): board.current_board[i][j]=1
            if i==4:
                for j in range(5): board.current_board[i][j]=-1
        board.current_board[1][0], board.current_board[1][4], board.current_board[2][0] = 1, 1, 1
        board.current_board[2][4], board.current_board[3][0], board.current_board[3][4] = -1, -1, -1
    @staticmethod

    def copy_board(current_board):
        new_board=[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        for i in range(5):
            for j in range(5):
                new_board[i][j]=current_board[i][j]
        return new_board
    @staticmethod

    def filter_pos(checklist, current_board, player):
        i=0
        while(i<len(checklist)):
            if (current_board[checklist[i].x][checklist[i].y]!=player): del checklist[i]
            else: i+=1
    @staticmethod

    def connection(position):
        out=[]
        if (position.x>0): out.append(Position(position.x-1, position.y))
        if (position.y>0): out.append(Position(position.x, position.y-1))
        if (position.x<4): out.append(Position(position.x+1, position.y))
        if (position.y<4): out.append(Position(position.x, position.y+1))
        if ((position.x+position.y)%2==0):
            if (position.x>0 and position.y>0): out.append(Position(position.x-1, position.y-1))
            if (position.x<4 and position.y>0): out.append(Position(position.x+1, position.y-1))
            if (position.x<4 and position.y<4): out.append(Position(position.x+1, position.y+1))
            if (position.x>0 and position.y<4): out.append(Position(position.x-1, position.y+1))
        return out
    @staticmethod

    def vay(current_board, move, player):
        out, check=[], []
        if(move.pos_end==move.pos_start): return out
        new_board=board.copy_board(current_board)
        new_board[move.pos_start.x][move.pos_start.y]=0
        new_board[move.pos_end.x][move.pos_end.y]=player
        check=board.connection(move.pos_end)
        board.filter_pos(check, new_board, -player)
        flag=True
        while(flag):
            flag=False
            for i in range(len(check)):
                flag1=True
                for j in range(len(out)):
                    if(out[j]==check[i]):
                        flag1=False
                        break
                if(flag1):
                    out.append(check[i])
                    flag=True
            size=len(check)
            for i in range(size):
                insert=board.connection(check[0])
                board.filter_pos(insert, new_board, -player)
                for j in range(len(insert)):
                    flag1=True
                    for k in range(len(out)):
                        if(insert[j]==out[k]):
                            flag1=False
                            break
                    if(flag1): check.append(insert[j])
                del check[0]
        check.clear()
        classification=[]     
        for i in range(len(out)):
            flag=False
            size=len(classification)
            for j in range(size):
                size1=len(classification[j])
                for k in range(size1):
                    check=board.connection(classification[j][k])
                    board.filter_pos(check, new_board, -player)
                    for l in range(len(check)):
                        if (check[l]==out[i]):
                            classification[j].append(out[i])
                            flag=True
                            break
                    if (flag): break
                if (flag): break
            if (flag==False): classification.append(list([out[i]]))
        out.clear()
        check.clear()
        for i in range(len(classification)):
            flag=True
            for j in range(len(classification[i])):
                check=board.connection(classification[i][j])
                board.filter_pos(check, new_board, 0)
                if (len(check)!=0):
                    flag=False
                    break
            if (flag):
                for j in range(len(classification[i])): out.append(classification[i][j])
        return out
    @staticmethod

    def ganh(current_board, move, player):
        out = []
        if(move.pos_start == move.pos_end): return out
        check = board.connection(move.pos_end)
        i=0
        while(i<len(check)-1):
            if(current_board[check[i].x][check[i].y]==-player):
                j=i+1
                while (j<len(check)):
                    if(current_board[check[j].x][check[j].y]==-player and check[j].x+check[i].x==2*move.pos_end.x and check[j].y+check[i].y==2*move.pos_end.y):
                        out.append(check[i])
                        out.append(check[j])
                        del check[i]
                        del check[j-1]
                        i-=1
                        break
                    j+=1
            i+=1
        new_board=board.copy_board(current_board)
        for i in range(len(out)): new_board[out[i].x][out[i].y]=player
        new_board[move.pos_start.x][move.pos_start.y]=0
        new_board[move.pos_end.x][move.pos_end.y]=player
        size=len(out)
        for i in range(size):
            check.clear()
            check=board.vay(new_board, Move(Position(),out[i]), player)
            for j in range(len(check)):
                flag=True
                for k in range(len(out)):
                    if(out[k] == check[j]): flag=False
                if(flag): out.append(check[j])
        return out
    @staticmethod

    def get_valid_moves(current_board, previous_board, player):
        out=[]
        if(previous_board!=[[]]):
            change=[]
            for i in range(5):
                for j in range(5):
                    if(current_board[i][j]!=previous_board[i][j]): change.append(Position(i,j))
            if(len(change)==2):
                check, possible=[], []
                if(current_board[change[0].x][change[0].y]==-player): check=board.connection(change[0])
                else: check=board.connection(change[1])
                board.filter_pos(check, current_board, 0)
                i=0
                while(i<len(check)):
                    possible.append(board.connection(check[i]))
                    board.filter_pos(possible[-1], current_board, player)
                    if(len(possible[len(possible)-1])==0):
                        del check[i]
                        del possible[len(possible)-1]
                    else: i+=1
                for i in range(len(check)):
                    g=board.ganh(current_board, Move(possible[i][0], check[i]), player)
                    if(len(g)!=0):
                        for j in range(len(possible[i])): out.append(Move(possible[i][j], check[i]))
                if(len(out)!=0): return out
        else:
            i=1
            while(i<4):
                j=1
                while(j<4):
                    current_board[i][j]=0
                    j+=1
                i+=1
        for i in range(5):
            for j in range(5):
                if(current_board[i][j]==player):
                    check=board.connection(Position(i,j))
                    for k in check:
                        if(current_board[k.x][k.y]==0): out.append(Move(Position(i,j),k))
        return out
    @staticmethod

    def select_move(player,level):
        check=board.get_valid_moves(board.current_board, board.previous_board, player)
        probabilities=[]
        if (len(check)==0): return None
        for i in range(len(check)):
            new_board=board.copy_board(board.current_board)
            board.act_move(new_board,check[i],player)
            probabilities.append(minimax(new_board,board.current_board,-player,level))
        max=probabilities[0].point
        choice=0
        if player>0:
            for i in range(1,len(probabilities)):
                if probabilities[i].point>max:
                    max=probabilities[i].point
                    choice=i
        else:
            for i in range(1,len(probabilities)):
                if probabilities[i].point<max:
                    max=probabilities[i].point
                    choice=i
        return check[choice]
    @staticmethod

    def act_move(current_board, move, player):
        g, v=[], []
        ganh=board.ganh(current_board, move, player)
        vay=board.vay(current_board, move, player)
        for i in range(len(ganh)): current_board[ganh[i].x][ganh[i].y]=player
        for i in range(len(vay)): current_board[vay[i].x][vay[i].y]=player
        current_board[move.pos_start.x][move.pos_start.y]=0
        current_board[move.pos_end.x][move.pos_end.y]=player


class minimax:
    def __init__(self, current_board, previous_board, player, degree):
        self.point=0
        self.descendent=[]
        if degree==0:
            for i in range(5):
                for j in range(5):
                    if (current_board[i][j]==1): self.point+=1
                    if (current_board[i][j]==-1): self.point-=1
        else:
            check=board.get_valid_moves(current_board, previous_board, player)
            if (len(check)!=0):
                for i in range(len(check)): 
                    new_board=board.copy_board(current_board)
                    board.act_move(new_board, check[i], player)
                    self.descendent.append(minimax(new_board, current_board, -player, degree-1))
                if player>0:
                    self.point=self.descendent[0].point
                    for i in range(1,len(self.descendent)):
                        if self.descendent[i].point>self.point: self.point=self.descendent[i].point
                else:
                    self.point=self.descendent[0].point
                    for i in range(1,len(self.descendent)):
                        if self.descendent[i].point<self.point: self.point=self.descendent[i].point
            else:
                for i in range(5):
                    for j in range(5):
                        if (current_board[i][j]==1): self.point+=1
                        if (current_board[i][j]==-1): self.point-=1