def evaluate(episode,out=0, N = 6):
    agent1win=0# agent1=RL
    agent2win=0
    tie =0
    keys = table.keys()
    for ii in range(episode):
        main = resetBoard()
        turn = 1
        pas=0
        if ii%2 == 0:
            turn = 2
        if out == 1:
            print('ii:',ii)
        while True:
            valid1 = getValidMoves(main,1)
            nvalid1 = len(valid1)
            valid2 = getValidMoves(main,2)
            nvalid2 = len(valid2)
            if gameEnd(main):
                break
            if turn == 2 and nvalid2 != 0:
                move = getComputerMove(main, 2, 3)
                makeMove(main,2,move[0],move[1])
                if out == 1:
                    print('2 move:\n',main)
                turn = 1
            elif turn == 2 and nvalid2 == 0 and nvalid1 != 0:
                turn = 1
            if turn == 1 and nvalid1 != 0:
# ยังไม่ได้แก้ 4 เป็น 6
#                 tmp1 =[ii*4+jj for ii, jj in getValidMoves(main,1)]
                tmp1 =[tmp[0]*N+tmp[1] for tmp in valid1]
                tupboard = tuple(main.reshape((main.size,)))
                if out == 1:
                    print('valid move',tmp1)
                if tupboard not in keys:
                    action = random.choices(valid1)[0]
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
        if getScoreOfBoard(main)[1]>getScoreOfBoard(main)[2]:
            agent1win = agent1win+1
        elif getScoreOfBoard(main)[1]<getScoreOfBoard(main)[2]:
            agent2win = agent2win+1
        else:
            tie=tie+1
    return agent1win, agent2win, tie
