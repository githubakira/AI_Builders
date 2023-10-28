import numpy as np
import pandas as pd
import random
import pickle
# from Minimax import *

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

def otherTile(tile):
    if tile == 1:
        return 2
    else:
        return 1
def dboard(mainBoard,items,N=6):
  for kk in range(N*N):
    ii = kk//N
    jj = kk%N
    if mainBoard[ii][jj] == 1:
      # print('1')
      items[kk].style.button_color = 'black'
    if mainBoard[ii][jj] == 2:
      # print('2')
      items[kk].style.button_color = 'white'
  return

def player(b,indx,items,mainBoard,playerTile,computerTile, nstep):
  if makeMove(mainBoard, playerTile, indx[0], indx[1]):
    dboard(mainBoard,items)
    if gameEnd(mainBoard):
      with out:
        clear_output()
        print('END')
        while True:
          1==1
    else:
      if len(getValidMoves(mainBoard,1)) == 0:
        with out:
          clear_output()
          print('Computer has no move!')
      else:
        x, y = getComputerMove(mainBoard, computerTile, nstep)
        makeMove(mainBoard, computerTile, x, y)
        dboard(mainBoard,items)
        with out:
          clear_output()
          print(getScoreOfBoard(mainBoard))
        while len(getValidMoves(mainBoard,2)) == 0:
          if gameEnd(mainBoard):
            with out:
              clear_output()
              print('END')
              while True:
                1==1
          x, y = getComputerMove(mainBoard, computerTile, nstep)
          makeMove(mainBoard, computerTile, x, y)
          dboard(mainBoard,items)
          with out:
            clear_output()
            print(getScoreOfBoard(mainBoard))
  else:
    with out:
      clear_output()
      print('Cannot move here!')
    return
  return
