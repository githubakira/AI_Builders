def corner(x, y,N=6):
    tmp1 = [0,N-1]
    tmp2 = [0,N-1]
    tmp1, tmp2 = np.meshgrid(tmp1,tmp2)
    tmp1 = tmp1.ravel() 
    tmp2 = tmp2.ravel()
    tmp = [[tmp1[ii],tmp2[ii]] for ii in range(len(tmp1))]
    return [x,y] in tmp

def outside(x, y,N=6):
    tmp1 = [ [0,ii] for ii in range(1,N-1)]
    tmp2 = [ [N-1,ii] for ii in range(1,N-1)]
    tmp3 = [ [ii,0] for ii in range(1,N-1)]
    tmp4 = [ [ii,N-1] for ii in range(1,N-1)]
    tmp = tmp1+tmp2+tmp3+tmp4
    return [x,y] in tmp

def middle(x, y, N=6):
    tmp1 = range(1,N-1)
    tmp2 = range(1,N-1)
    tmp1, tmp2 = np.meshgrid(tmp1,tmp2)
    tmp1 = tmp1.ravel() 
    tmp2 = tmp2.ravel()
    tmp = [[tmp1[ii],tmp2[ii]] for ii in range(len(tmp1))]
    return [x,y] in tmp

def get_heuristic(board, tile):
    N = board.shape[0]
    score = 0
    for x in range(N):
        for y in range(N):
            if corner(x,y) and board[x][y] == tile:
                score = score + 7
            elif corner(x,y) and board[x][y] == otherTile(tile):
                score = score - 7
            elif outside(x,y) and board[x][y] == tile:
                score = score + 2
            elif outside(x,y) and board[x][y] == otherTile(tile):
                score = score - 2
            elif middle(x,y) and board[x][y] == tile:
                score = score + 1
            elif middle(x,y) and board[x][y] == otherTile(tile):
                score = score - 1
    return score

def minimax(node, depth, maximizingPlayer, tile):
    if depth == 0 or gameEnd(node):
        return get_heuristic(node,tile)
    if maximizingPlayer:
        value = -np.Inf
        for x,y in valid_moves:
            child = getBoardCopy(node)
            makeMove(child, tile, x, y)
            value = max(value, minimax(child, depth - 1, False, tile))
        return value
    else:
        value = np.Inf
        for x,y in valid_moves:
            child = getBoardCopy(node)
            makeMove(child, otherTile(tile), x, y)
            value = min(value, minimax(child, depth - 1, True, tile))
        return value

def score_move(board, x, y, computertile, nsteps):
    dupeBoard = getBoardCopy(board)
    makeMove(dupeBoard, computertile, x, y)
    score = minimax(dupeBoard, nsteps-1, False, computertile)
    return score

def minimaxMove(board, computerTile, depth):
    is_terminal = gameEnd(board)
    valid_moves = getValidMoves(board, computerTile)
    def score_move(board, x, y, computertile, nsteps):
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computertile, x, y)
        score = minimax(dupeBoard, nsteps-1, False, computertile)
        return score
    scores = dict(zip(list(range(len(valid_moves))), [score_move(board, ii[0], ii[1], computerTile, depth) for ii in valid_moves]))
    max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
    return valid_moves[random.choice(max_cols)]
