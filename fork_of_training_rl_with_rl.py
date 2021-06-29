# -*- coding: utf-8 -*-
"""fork-of-training-rl-with-rl.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lCwQQknM7bld4K7m-UcL4MMyauLt_A82
"""

import numpy as np
import pandas as pd
import random
import pickle

def resetBoard(N=6):
    board = np.array([0 for ii in range(N*N)]).reshape(N,N)
    board[N//2-1][N//2-1] = 1# 0=' ' 1=X 2=O
    board[N//2-1][N//2] = 2
    board[N//2][N//2-1] = 2
    board[N//2][N//2] = 1
    return board

def getBoardCopy(board):
    dupeBoard = board.copy()
    return dupeBoard

def enterPlayerTile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    if tile == 'X':
        return [1, 2]# ''=0 x=1 o=2
    else:
        return [2, 1]

def makeMove(board, tile, xstart, ystart):
    tilesToFlip = ValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False 
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def isOnBoard(x, y, N = 6):
    return x >= 0 and x <= N-1 and y >= 0 and y <= N-1

def gameEnd(board):
    N = board.shape[0]
    if (getScoreOfBoard(board)[1])+(getScoreOfBoard(board)[2])==N*N:
        return True
    elif len(getValidMoves(board,1))==0 and len(getValidMoves(board,2))==0:
        return True
    else:
        return False

def ValidMove(board, tile, xstart, ystart):
  #check if player 1 or 2 is on the tile or outsize thee board
    if board[xstart][ystart] != 0 or not isOnBoard(xstart, ystart):
    # print('1')
        return False
#     board[xstart][ystart] = tile
    if tile == 1:
        otherTile = 2
    else:
        otherTile = 1

    tilesToFlip = []
  #check 8 directions
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
#         print(xstart, ',',ystart,[xdirection,ydirection],x,',',y)
        while isOnBoard(x, y):
            if board[x][y] == otherTile:
                x += xdirection
                y += ydirection
#         print(x,',',y)
            else:
                break
        if not isOnBoard(x, y):
            continue
        elif board[x][y] == 0:
            continue
        else:
            while True:
                x -= xdirection
                y -= ydirection
                if x == xstart and y == ystart:
                    break
                tilesToFlip.append([x, y])
#     board[xstart][ystart] = 0
    if len(tilesToFlip) == 0:
    # print('2')
        return False
    return tilesToFlip

def getValidMoves(board, tile, N=6):
    validMoves = []
    for x in range(N):
        for y in range(N):
            if ValidMove(board, tile, x, y) != False:
#                 print(x,y)
#                 print(ValidMove(board, tile, x, y))
                validMoves.append([x, y])
    return validMoves

def otherTile(tile):
    if tile == 1:
        return 2
    else:
        return 1

"""## Score"""

def getScoreOfBoard(board):
    N = board.shape[0]
    xscore = 0
    oscore = 0
    for x in range(N):
        for y in range(N):
            if board[x][y] == 1:
                xscore += 1
            if board[x][y] == 2:
                oscore += 1
    return {1:xscore, 2:oscore}

def showPoints(playerTile, computerTile):
    scores = getScoreOfBoard(mainBoard)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))

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
    elif len(getValidMoves(nboard,tile))==0: # add from version 20210621 RL no move reward = -1
        return nboard, -1, False
    elif len(getValidMoves(nboard,otherTile(tile)))==0: # add from version 20210621 Computer no move reward = 1
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
#Akira works
#     newBoard[N//2-1][N//2-1] = 1
#     newBoard[N//2-1][N//2] = 2
#     newBoard[N//2][N//2-1] = 2
#     newBoard[N//2][N//2] = 1
    return newBoard

q_table = dict()
# file = open('/kaggle/input/q-table-evaluation-6x6/q_table2000.pkl','rb')
# q_table = pickle.load(file)
# file.close()
keys = q_table.keys()
keys

def getComputerMove(board,tile):
    validMove = getValidMoves(board, tile)
    move = random.choice(validMove)
    return move
def evaluate(episode,out=0, N = 6):
    table = q_table
    agent1win=0# agent1=RL
    agent2win=0
    tie =0
    not_in_table = []
    ag_pts1 = []
    ag_pts2 = []
    keys = table.keys()
    for ii in range(episode):
        main = resetBoard()
        turn = 1
        pas=0
        ep_not_in_table = 0
        if ii%2 == 0:
            turn = 2
        while True:
            valid1 = getValidMoves(main,1)
            nvalid1 = len(valid1)
            valid2 = getValidMoves(main,2)
            nvalid2 = len(valid2)
            if gameEnd(main):
                break
            if turn == 2 and nvalid2 != 0:
                move = getComputerMove(main, 2)
#                 print(move)
                makeMove(main,2,move[0],move[1])
                if out == 1:
                    print('2 move:\n',main)
                turn = 1
            elif turn == 2 and nvalid2 == 0 and nvalid1 != 0:
                turn = 1
            valid1 = getValidMoves(main,1)
            nvalid1 = len(valid1)
            if turn == 1 and nvalid1 != 0:
# ยังไม่ได้แก้ 4 เป็น 6
#                 tmp1 =[ii*4+jj for ii, jj in getValidMoves(main,1)]
                tmp1 =[tmp[0]*N+tmp[1] for tmp in valid1]
                tupboard = tuple(main.reshape((main.size,)))
                if out == 1:
                    print('valid move',tmp1)
                if tupboard not in keys:
                    action = random.choices(valid1)[0]
                    ep_not_in_table = ep_not_in_table+1
                    if out == 1:
                        print('action from random:',action)
                else:
                    action=numToList(tmp1[np.argmax(table[tupboard ][tmp1])])
                    if out == 1:
                        print('action from q_table:',action)
                        print(table[tupboard])
                makeMove(main,1,action[0],action[1])
                turn = 2
            elif turn == 1 and nvalid1==0 and nvalid2!=0:
                turn = 2
        not_in_table.append(ep_not_in_table)
        ag_pts1.append(getScoreOfBoard(main)[1])
        ag_pts2.append(getScoreOfBoard(main)[2])
        if getScoreOfBoard(main)[1]>getScoreOfBoard(main)[2]:
            agent1win = agent1win+1
        elif getScoreOfBoard(main)[1]<getScoreOfBoard(main)[2]:
            agent2win = agent2win+1
        else:
            tie=tie+1
    return agent1win, agent2win, tie, not_in_table, ag_pts1, ag_pts2

q_table = dict()
# file = open('/kaggle/input/q-table-evaluation-6x6/q_table2000.pkl','rb')
# q_table = pickle.load(file)
# file.close()
keys = q_table.keys()
keys

episode = 10000
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
info = []
for ii in range(0, episode):
    state = resetBoard()    
    epochs, penalties, reward, = 0, 0, 0
    done = False    
    RLtile=1
    computerTile=2    
#     print(ii)
    times=0
    if ii%2 == 0: # เลขคู่ computer move first
        valid = getValidMoves(state,computerTile)
        validnum = [tmp[0]*N+tmp[1] for tmp in valid]
        keys = q_table.keys()
        #20210629 change valid => comValid validnum => comValidnum
        comState = oneToTwo(state,computerTile)
        comValid = getValidMoves(comState,RLtile)
        comValidnum = [tmp[0]*N+tmp[1] for tmp in comValid]
#         print(state)
#         print(comState)
        tup_state = tuple(comState.reshape(comState.size,))
        if tup_state not in keys: #ดูว่า มี state นี่อยู่แล้วหรือไม่
            q_table[tup_state] = np.zeros((N*N,))
            #20210629
            q_table[tup_state][comValidnum] = (1/(0.5*(N*N-4)))*np.ones((len(comValidnum),))
#             q_table[tup_state][validnum] = (1/(0.5*(N*N-4)))*np.ones((len(validnum),))
        if random.uniform(0, 1) < epsilon:
            action = random.choice(valid) # Explore action space
        else:
            #20210629
            tmp = comValidnum[np.argmax(q_table[tup_state][comValidnum])]
#             tmp = validnum[np.argmax(q_table[tup_state][validnum])]
            action = numToList(tmp) 
            print('0',action)
            action[1] = (N-1)-action[1]
            print('1',action)
#         print('act',action)
#         print(makeMoveRl(action, state, RLtile))
        state, comReward, done = makeMoveRl(action, state, computerTile)
    print(ii)
    print(action)
    print('comState')
    print(np.array(comState).reshape((N,N)))
    print('state')
    print(np.array(state).reshape((N,N)))
    print('q_value')
    print(np.array(q_table[tup_state]).reshape((N,N)))
    print(q_table[tup_state][comValidnum])
    
    while not done:
#         print(state)
#         print(times)
#         times=times+1
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
            print('after RL')
            print(np.array(next_state).reshape((N,N)))

        else: # เพิ่มจาก version 20210621 ถ้า RL ลงไม่ได้ต้องให้ next_state = state เลย 
            next_state = state # แต่ของเดิม ก่อนมาถึงจุดนี้ ให้ state = next_stae ตอนจบ loop อยู่แล้วน่าจะไม่ผิด
#         print(next_state)
        if len(getValidMoves(next_state,computerTile)) != 0 and gameEnd(state) == False:
            valid1 = getValidMoves(next_state,computerTile)
            validnum = [tmp[0]*N+tmp[1] for tmp in valid1]
            keys = q_table.keys()
            comState = oneToTwo(next_state,computerTile)
            #20210629
            comValid = getValidMoves(comState,RLtile)
            comValidnum = [tmp[0]*N+tmp[1] for tmp in comValid]
            tup_state = tuple(comState.reshape(comState.size,))
            if tup_state not in keys: #ดูว่า มี state นี่อยู่แล้วหรือไม่
                q_table[tup_state] = np.zeros((N*N,))
                q_table[tup_state][comValidnum] = (1/(0.5*(N*N-4)))*np.ones((len(comValidnum),))
#                 q_table[tup_state][validnum] = (1/(0.5*(N*N-4)))*np.ones((len(validnum),))
            if random.uniform(0, 1) < epsilon:
                action = random.choice(valid1) # Explore action space
            else:
                #20210629
                tmp = comValidnum[np.argmax(q_table[tup_state][comValidnum])]
#                 tmp = validnum[np.argmax(q_table[tup_state][validnum])]
                action = numToList(tmp) 
                action[1] = (N-1)-action[1] 
            print(action)
            next_state, comReward, done = makeMoveRl(action, next_state, computerTile)
            print('after Comp')
            print(np.array(next_state).reshape((N,N)))
#         print(action, state, computerTile)
#         print(done)
# ถ้า RL ลงไม่ได้ "action" จะเป็นขอตาก่อนหน้า เพราะ ตานี้ไม่มี action เราต้องไม่ใส่คะแนนเข้าไปใน q_table
# edit from version 20210621
        if len(valid) != 0:
            valid = getValidMoves(next_state,RLtile)
            validnum = [tmp[0]*N+tmp[1] for tmp in valid]
            keys = q_table.keys()
            tup_nextstate = tuple(next_state.reshape(next_state.size,))
            if tup_nextstate not in keys:
#                 print('not in keys')
#                 print(next_state)
                q_table[tup_nextstate] = np.zeros((N*N,))
                q_table[tup_nextstate][validnum] = (1/(0.5*(N*N-4)))*np.ones((len(validnum),))
            old_value = q_table[tup_state][action[0]*N+action[1]] # this line was wrong change 4 to N
            next_max = np.max(q_table[tup_nextstate])        
            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[tup_state][action[0]*N+action[1]] = new_value # this line was wrong change 4 to N
        else: # สร้าง q_table ของ next_state
            valid = getValidMoves(next_state,RLtile)
            validnum = [tmp[0]*N+tmp[1] for tmp in valid]
            keys = q_table.keys()
            tup_nextstate = tuple(next_state.reshape(next_state.size,))
            if tup_nextstate not in keys:
#                 print('not in keys')
#                 print(next_state)
                q_table[tup_nextstate] = np.zeros((N*N,))
                q_table[tup_nextstate][validnum] = (1/(0.5*(N*N-4)))*np.ones((len(validnum),))
#_________________________________________________________
        state = next_state
        epochs += 1
    if ii%500 == 0:
        agent1win, agent2win, tie, not_in_table, ag_pts1, ag_pts2 = evaluate(100,out=0, N = 6)
        filename = 'evaluate'+str(ii)+'.pkl'
        data = [agent1win, agent2win, tie, not_in_table, ag_pts1, ag_pts2]
        file = open(filename,'wb')
        pickle.dump(data, file)
        file.close()
filename = '/kaggle/working/q_table'+str(ii)+'.pkl'
outfile = open(filename,'wb')
pickle.dump(q_table,outfile)
outfile.close()
print("Training finished.\n")

# filename = '/kaggle/working/q_table_rlrl.pkl'
# outfile = open(filename,'wb')
# pickle.dump(q_table,outfile)
# outfile.close()

# len(q_table)

# table = q_table
# [agent1win, agent2win, tie, not_in_table, ag_pts1, ag_pts2] = evaluate(10000,out=0, N = 6)
# data = [agent1win, agent2win, tie, not_in_table, ag_pts1, ag_pts2]
