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

