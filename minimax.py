import random


def get_all_direction(current_board, cur_pos):
    all_direction = []

    x, y = cur_pos

    if (x > 0):
        all_direction.append((x-1, y))
    if (y > 0):
        all_direction.append((x, y-1))
    if (x < 4):
        all_direction.append((x+1, y))
    if (y < 4):
        all_direction.append((x, y+1))

    if ((x+y) % 2 == 0):
        if (x > 0 and y > 0):
            all_direction.append((x-1, y-1))
        if (x < 4 and y > 0):
            all_direction.append((x+1, y-1))
        if (x < 4 and y < 4):
            all_direction.append((x+1, y+1))
        if (x > 0 and y < 4):
            all_direction.append((x-1, y+1))

    return all_direction


def find_near_cell(current_board, cur_pos, cell_code):
    all_pos = get_all_direction(current_board=current_board, cur_pos=cur_pos)

    result = []
    for pos in all_pos:
        x, y = pos

        if current_board[x][y] == cell_code:
            result.append(pos)

    return result


def valid_index(id: int) -> bool:
    return id >= 0 and id < 5


def vay(current_board, cur_pos, player: int):
    near_opponents = find_near_cell(
        current_board=current_board, cur_pos=cur_pos, cell_code=-player)

    clusters = []
    visited = {}

    for cell in near_opponents:
        if not visited.get(str(cell), False):
            clusters.append([cell])
            visited[str(cell)] = True

            cur_cluster = clusters[-1]

            for cluster_cell in cur_cluster:
                near_cell_opponents = find_near_cell(
                    current_board=current_board, cur_pos=cluster_cell, cell_code=-player)

                for near_cell in near_cell_opponents:
                    if not visited.get(str(near_cell), False):
                        cur_cluster.append(near_cell)
                        visited[str(near_cell)] = True

    final_cluster = []

    for cluster in clusters:
        is_isolated = True

        for cell in cluster:
            empty_cells = find_near_cell(
                current_board=current_board, cur_pos=cell, cell_code=0)

            if len(empty_cells) > 0:
                is_isolated = False
                break

        if is_isolated:
            final_cluster.append(cluster)

    return final_cluster


def ganh(current_board, cur_pos, player: int):
    direction_vector = [(0, 1), (1, 0), (1, 1), (1, -1)]

    pos = []

    x, y = cur_pos
    for v in direction_vector:
        v_x, v_y = v

        back_x = x - v_x
        back_y = y - v_y

        front_x = x + v_x
        front_y = y + v_y

        if valid_index(back_x) and valid_index(back_y) and valid_index(front_x) and valid_index(front_y):
            if current_board[back_x][back_y] == -player and current_board[front_x][front_y] == -player:
                pos.append((back_x, back_y))
                pos.append((front_x, front_y))

    return pos


def trap_moves(current_board, recent_opponent_cell, player: int):
    ganhed_cell = ganh(current_board=current_board,
                       cur_pos=recent_opponent_cell, player=player)

    if (len(ganhed_cell) > 0):
        near_players = find_near_cell(
            current_board=current_board, cur_pos=recent_opponent_cell, cell_code=player)

        return [(near_player, recent_opponent_cell) for near_player in near_players]

    return []


def get_all_moves(current_board, previous_board, player: int):
    if (previous_board != [[]] and previous_board is not None):
        track_diff = []
        for i in range(5):
            for j in range(5):
                if (current_board[i][j] != previous_board[i][j]):
                    track_diff.append((i, j))

        # check if opponent has trap moves
        if (len(track_diff) == 2):
            opponent_move = None

            if (current_board[track_diff[0][0]][track_diff[0][1]] == 0):
                opponent_move = track_diff[0]
            else:
                opponent_move = track_diff[1]

            moves = trap_moves(current_board=current_board,
                               recent_opponent_cell=opponent_move, player=player)

            if (len(moves) > 0):
                return moves

    moves = []

    for i in range(5):
        for j in range(5):
            if (current_board[i][j] == player):
                empty_cells = find_near_cell(
                    current_board=current_board, cur_pos=(i, j), cell_code=0)

                moves.extend([((i, j), cell) for cell in empty_cells])

    return moves


def copy_board(current_board):
    result = [list(range(5)) for _ in range(5)]

    for i in range(5):
        for j in range(5):
            result[i][j] = current_board[i][j]

    return result


def get_score(current_board):
    score = 0

    for row in current_board:
        for value in row:
            score += value

    return score


def change_board(current_board, move, player):
    old_pos, new_pos = move

    if current_board[old_pos[0]][old_pos[1]] == 0:
        return
    if current_board[new_pos[0]][new_pos[1]] != 0:
        return

    current_board[old_pos[0]][old_pos[1]] = 0
    current_board[new_pos[0]][new_pos[1]] = player

    ganhed_cells = ganh(current_board=current_board,
                        cur_pos=new_pos, player=player)
    vayed_clusters = vay(current_board=current_board,
                         cur_pos=new_pos, player=player)

    for cell in ganhed_cells:
        x, y = cell

        current_board[x][y] = player

        new_vayed_clusters = vay(
            current_board=current_board, cur_pos=cell, player=player)

        for new_clusters in new_vayed_clusters:
            for new_cell in new_clusters:
                x, y = new_cell

                current_board[x][y] = player

    for cluster in vayed_clusters:
        for cell in cluster:
            x, y = cell

            current_board[x][y] = player


def is_finished(current_board) -> bool:
    has_player = False
    has_opponent = False

    for row in current_board:
        for cell in row:
            if cell == -1:
                has_opponent = True
            elif cell == 1:
                has_player = True

    return not (has_opponent and has_player)


def minimax(current_board, previous_board, player: int, degree: int, alpha, beta) -> int:
    # return score value at leaf node
    if degree == 0 or is_finished(current_board=current_board):
        return get_score(current_board=current_board)

    moves = get_all_moves(
        current_board=current_board, previous_board=previous_board, player=player)

    inner_value = None

    for i, move in enumerate(moves):
        new_board = copy_board(current_board=current_board)

        change_board(current_board=new_board, move=move, player=player)

        child_value = minimax(
            current_board=new_board, previous_board=current_board, player=-player, degree=degree - 1, alpha=alpha, beta=beta)

        if player == 1:
            if inner_value is None:
                inner_value = child_value
            else:
                inner_value = max(inner_value, child_value)

            alpha = max(alpha, inner_value)

        elif player == -1:
            if inner_value is None:
                inner_value = child_value
            else:
                inner_value = min(inner_value, child_value)

            beta = min(beta, inner_value)

        if alpha >= beta:
            break

    return inner_value


def move(prev_board, board, player, tree_depth):
    if is_finished(current_board=board):
        return

    TREE_DEPTH = tree_depth

    if prev_board is not None:
        previous_board = copy_board(current_board=prev_board)
    else:
        previous_board = None

    current_board = copy_board(current_board=board)

    moves = get_all_moves(current_board=current_board,
                          previous_board=previous_board, player=player)

    scores = []

    for move in moves:
        test_board = copy_board(current_board=current_board)
        change_board(current_board=test_board, move=move, player=player)

        scores.append(minimax(current_board=test_board,
                      previous_board=current_board, player=-player, degree=TREE_DEPTH, alpha=-1000, beta=1000))

    layer_value = None
    if player == 1:
        layer_value = max(scores)
    elif player == -1:
        layer_value = min(scores)

    best_idx = [i for i, val in enumerate(scores) if val == layer_value]

    choosen_idx = random.choice(best_idx)

    return moves[choosen_idx]
