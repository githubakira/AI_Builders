def numToList(num, N=6):
    row = num//N
    column = num%N
    action = [row, column]
    return action
        
def compstnum(state):
    tmp = state.reshape(16,)
    statenumber = 0
    for ii in range(16):
        statenumber = statenumber + tmp[ii]*(3**ii)
    return statenumber

def makeMoveRl(move, board, tile, N = 6):
    nboard = getBoardCopy(board)
    makeMove(nboard, tile, move[0],move[1])
    if getScoreOfBoard(nboard)[tile]>getScoreOfBoard(nboard)[otherTile(tile)]and gameEnd(nboard):
        return nboard, 1, True
    elif getScoreOfBoard(nboard)[tile]<getScoreOfBoard(nboard)[otherTile(tile)]and gameEnd(nboard):
        return nboard, -1, True
    elif getScoreOfBoard(nboard)[tile]==getScoreOfBoard(nboard)[otherTile(tile)]and gameEnd(nboard):
        return nboard, 0.5, True
    elif len(getValidMoves(nboard,tile))==0:
        return nboard, -1, False
    elif len(getValidMoves(nboard,otherTile(tile)))==0:
        return nboard, 1, False
    else:
        return nboard, (1/(0.5*(N*N-4))), False

def oneToTwo(board,tile,N=6):
    newBoard=board.copy()
    for i in range(N):
        for ii in range(N):
            if newBoard[i][ii] == tile:
                newBoard[i][ii]=otherTile(tile)
            elif newBoard[i][ii] == otherTile(tile):
                newBoard[i][ii]=tile
    newBoard = newBoard[:,N::-1]
    return newBoard

q_table = dict()
keys = q_table.keys()
keys

episode = 2001
N = 6
"""Training the agent"""
import random
from IPython.display import clear_output
# Hyperparameters
alpha = 0.2
gamma = 0.6
epsilon = 0.1
# For plotting metrics
all_epochs = []
all_penalties = []
for ii in range(1001, episode):
    state = resetBoard()    
    epochs, penalties, reward, = 0, 0, 0
    done = False    
    RLtile=1
    computerTile=2    
    if ii%2 == 0: # เลขคู่ computer move first        
        if random.uniform(0, 1) <= 0.2:
#             print('computer move minimax')
            state,reward, done = agentminimax(state, computerTile)
        else:
#             print('computer move random')
            action = random.choice(getValidMoves(state, computerTile))
            state,reward, done = makeMoveRl(action, state, computerTile)
    while not done:
        valid = getValidMoves(state,RLtile)
        validnum = [tmp[0]*N+tmp[1] for tmp in valid]
        keys = q_table.keys()
        tup_state = tuple(state.reshape(state.size,))
        if tup_state not in keys: #ดูว่า มี state นี่อยู่แล้วหรือไม่
            q_table[tup_state] = np.zeros((N*N,))
            q_table[tup_state][validnum] = (1/(0.5*(N*N-4)))*np.ones((len(validnum),))
#         print(q_table[tup_state])
        if len(valid) != 0 and gameEnd(state) == False: # RL มีตำแหน่งลงได้
            if random.uniform(0, 1) < epsilon:
#                 print('RL move random')
                action = random.choice(valid) # Explore action space
            else:
#                 print('RL move q_table')
                tmp = validnum[np.argmax(q_table[tup_state][validnum])]
                action = numToList(tmp) 
            next_state, reward, done = makeMoveRl(action, state, RLtile)
        else: # เพิ่มจาก version 20210621 ถ้า RL ลงไม่ได้ต้องให้ next_state = state เลย 
            next_state = state # แต่ของเดิม ก่อนมาถึงจุดนี้ ให้ state = next_stae ตอนจบ loop อยู่แล้วน่าจะไม่ผิด

        if len(getValidMoves(next_state,computerTile)) != 0 and gameEnd(state) == False:
            if random.uniform(0, 1) <= 0.5:
#                 print('computer move minimax')
                next_state,reward, done = agentminimax(next_state, computerTile)
            else:
#                 print('computer move random')
                agent_act = random.choice(getValidMoves(next_state, computerTile))
                next_state,reward, done = makeMoveRl(agent_act, next_state, computerTile)
# ถ้า RL ลงไม่ได้ "action" จะเป็นขอตาก่อนหน้า เพราะ ตานี้ไม่มี action เราต้องไม่ใส่คะแนนเข้าไปใน q_table
# edit from version 20210621
        if len(valid) != 0:
            valid = getValidMoves(next_state,RLtile)
            validnum = [tmp[0]*N+tmp[1] for tmp in valid]
            keys = q_table.keys()
            tup_nextstate = tuple(next_state.reshape(next_state.size,))
            if tup_nextstate not in keys:
                q_table[tup_nextstate] = np.zeros((N*N,))
                q_table[tup_nextstate][validnum] = (1/(0.5*(N*N-4)))*np.ones((len(validnum),))
            old_value = q_table[tup_state][action[0]*4+action[1]]
            next_max = np.max(q_table[tup_nextstate])        
            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[tup_state][action[0]*4+action[1]] = new_value
        else: # สร้าง q_table ของ next_state
            valid = getValidMoves(next_state,RLtile)
            validnum = [tmp[0]*N+tmp[1] for tmp in valid]
            keys = q_table.keys()
            tup_nextstate = tuple(next_state.reshape(next_state.size,))
            if tup_nextstate not in keys:
                q_table[tup_nextstate] = np.zeros((N*N,))
                q_table[tup_nextstate][validnum] = (1/(0.5*(N*N-4)))*np.ones((len(validnum),))
        state = next_state

def rlMove(board):
    if tup_state not in keys: #ดูว่า มี state นี่อยู่แล้วหรือไม่
        return random.choice(getValidMoves(board,1)
    else:
        tmp = validnum[np.argmax(q_table[tup_state][validnum])]
        action = numToList(tmp) 
        return action
        return action
