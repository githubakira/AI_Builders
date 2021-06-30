from Environment import *
def rlMove(board,q_table):
    board = np.array(board)
    N = board.shape[0]
    valid = getValidMoves(board,1)
    validnum = [tmp[0]*N+tmp[1] for tmp in valid]
    tup_state = tuple(board.reshape(board.size,))
    keys =q_table.keys()
    if tup_state not in keys: #ดูว่า มี state นี่อยู่แล้วหรือไม่
        return random.choice(getValidMoves(board,1)
    else:
        tmp = validnum[np.argmax(q_table[tup_state][validnum])]
        action = numToList(tmp) 
        return action
