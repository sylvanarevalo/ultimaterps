# import sqlite3
# conn = sqlite3.connect('./example.db')
# c = conn.cursor()

# # Create table
# c.execute('''CREATE TABLE stocks
#              (date text, trans text, symbol text, qty real, price real)''')

# # Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# # Save (commit) the changes
# conn.commit()

# # We can also close the connection if we are done with it.
# # Just be sure any changes have been committed or they will be lost.
# conn.close()


# #####
import itertools
product= itertools.product
pstates= product((0,1,2,3), (-1,0,1),(-1,0,1,2),(-1,0,1,2,3,4), (-1,0,1,2)) #wins, butterfly, nuke, rps, croach
states= product(pstates,pstates)
db={}
for s in states:
	val=None
	#0 is for rps, 1 is for butterfly, 2 nuke, 3 roach
	A= [[None for x in xrange(4)] for x in xrange(4)]
	p1strat= None
	p2strat= None
	db[s]= [val,A,p1strat,p2strat]

def fillTerminalStates():
	'''sets value of leaf nodes, so that recursion can stop'''
	for state in states:
		if -1 in state[0]: db[state][0] = 0.0
		if -1 in state[1]: db[state][0]= 1.0
		if -1 in state[0] and -1 in state[1]: db[state][0]= .5 #don't think this matters
		if state[0][0]==3: db[state][0]= 1
		if state[1][0]==3: db[state][0]= 1
fillTerminalStates()


import solvegame
solve = solvegame.solve

def statechanger(state,action):
	s=map(list,state)
	if action == 'wrr':
		s[0][0]+=1
	elif action == 'lrr':
		s[1][0]+=1
	elif action == 'trr':

	elif action == 'rb':
		s[0][0]=0
		s[1][0]=0
		s[1][1]+= -1
	return map(tuple, s)




def rsolve(state):
	'''rsolve for recursive solve. If the state is already solved, return it,
	else start by filling A, and then calling solve on A.'''
	if db[state][0] != None: return db[state][0]
	A= db[state][1]
	A[0][0]= .33333333*rsolve(db[statechanger(state,'wrr')]) + .3333333*rsolve(db[statechanger(state,'lrr')]) + .3333333 rsolve(db[statechanger(state,'trr')])
	A[0][1]=rsolve(db[statechanger(state,'rb')])
	A[0][2]=rsolve(db[statechanger(state,'rn')])
	A[0][3]=rsolve(db[statechanger(state,'rc')])
	A[1][0]=rsolve(db[statechanger(state,'br')])
	A[1][1]=rsolve(db[statechanger(state,'bb')])
	A[1][2]=rsolve(db[statechanger(state,'bn')])
	A[1][3]=rsolve(db[statechanger(state,'bc')])
	A[2][0]=rsolve(db[statechanger(state,'nr')])
	A[2][1]=rsolve(db[statechanger(state,'nb')])
	A[2][2]=rsolve(db[statechanger(state,'nn')])
	A[2][3]=rsolve(db[statechanger(state,'nc')])
	A[3][0]=rsolve(db[statechanger(state,'cr')])
	A[3][1]=rsolve(db[statechanger(state,'cb')])
	A[3][2]=rsolve(db[statechanger(state,'cn')])
	A[3][3]=rsolve(db[statechanger(state,'cc')])#uh oh, this one will create infinite loop
	solved= solve(A)
	db[state]= [solved[2], A, solved[0],solved[1]]
	#I'm worried I have row and col reversed. If funny errors, try swiching





