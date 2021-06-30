from Environment import *
#load previous trained q_table
# path = 'file location'
# file = open(path,'rb')
# q_table = pickle.load(file)
# file.close()
# or start with new q_table
# q_table = dict()
# keys = q_table.keys()

episode = 60001
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
for ii in range(40001, episode):
    state = resetBoard()    
    epochs, penalties, reward, = 0, 0, 0
    done = False    
    RLtile=1
    computerTile=2    
    times=0
    if ii%2 == 0: # เลขคู่ computer move first
        valid1 = getValidMoves(state,computerTile)
        validnum1 = [tmp[0]*N+tmp[1] for tmp in valid1]
        keys = q_table.keys()
        #20210629 change valid => comValid validnum => comValidnum
        comState = oneToTwo(state,computerTile)
        comValid = getValidMoves(comState,RLtile)
        comValidnum = [tmp[0]*N+tmp[1] for tmp in comValid]
        comTup_state = tuple(comState.reshape(comState.size,))
        if comTup_state not in keys: #ดูว่า มี state นี่อยู่แล้วหรือไม่
            q_table[comTup_state] = np.zeros((N*N,))
            #20210629
            q_table[comTup_state][comValidnum] = (1/(0.5*(N*N-4)))*np.ones((len(comValidnum),))
        if random.uniform(0, 1) < epsilon:
            comAction = random.choice(valid1) # Explore action space
        else:
            #20210629
            tmp = comValidnum[np.argmax(q_table[comTup_state][comValidnum])]
            comAction = numToList(tmp) 
            comAction[1] = (N-1)-comAction[1]
        state, reward, done = makeMoveRl(comAction, state, computerTile)
    while not done:
        valid = getValidMoves(state,RLtile)
        validnum = [tmp[0]*N+tmp[1] for tmp in valid]
        keys = q_table.keys()
        tup_state = tuple(state.reshape(state.size,))
        if tup_state not in keys: #ดูว่า มี state นี่อยู่แล้วหรือไม่
            q_table[tup_state] = np.zeros((N*N,))
            q_table[tup_state][validnum] = (1/(0.5*(N*N-4)))*np.ones((len(validnum),))
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
            valid1 = getValidMoves(next_state,computerTile)
            validnum1 = [tmp[0]*N+tmp[1] for tmp in valid1]
            keys = q_table.keys()
            comState = oneToTwo(next_state,computerTile)
            #20210629
            comValid = getValidMoves(comState,RLtile)
            comValidnum = [tmp[0]*N+tmp[1] for tmp in comValid]
            comTup_state = tuple(comState.reshape(comState.size,))
            if comTup_state not in keys: #ดูว่า มี state นี่อยู่แล้วหรือไม่
                q_table[comTup_state] = np.zeros((N*N,))
                q_table[comTup_state][comValidnum] = (1/(0.5*(N*N-4)))*np.ones((len(comValidnum),))
            if random.uniform(0, 1) < epsilon:
                comAction = random.choice(valid1) # Explore action space
#                 print('comp random')
            else:
                #20210629
                tmp = comValidnum[np.argmax(q_table[comTup_state][comValidnum])]
                comAction = numToList(tmp) 
                comAction[1] = (N-1)-comAction[1] 
            next_state, reward, done = makeMoveRl(comAction, next_state, computerTile)
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
                q_table[tup_nextstate] = np.zeros((N*N,))
                q_table[tup_nextstate][validnum] = (1/(0.5*(N*N-4)))*np.ones((len(validnum),))
#_________________________________________________________
        state = next_state
        epochs += 1
    if ii%500 == 0:
        agent1win, agent2win, tie, not_in_table, ag_pts1, ag_pts2 = evaluate(1000,out=0, N = 6)
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
