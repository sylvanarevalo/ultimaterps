#So far this is basically just what we did at Cloyne. 
#I was hoping to use a sql database, but it made more sense to just use a hashtable
#Since it is really a short program, I'll just wait for you to help me finish it off, and then do debugging and testing.
# I hope that the only thing left to do is to fill out statechanger.

#itertools is a useful python package that can do things like make the cartesian product
 #only change this line:
p1 = (0,2,2,5)
p2 = (0,2,2,5)
w1 = 2;
w2 = 2;

import itertools
product= itertools.product
#pstates are the states of the various players
p1states= tuple(product(tuple(range(w1+1)), tuple(range(-1,p1[1]+1)),tuple(range(-1,p1[2]+1)),tuple(range(-1,p1[3]+1)))) #wins, butterfly, nuke, tiesInARow
#To make the tree acylic I added restrictions on how many times you can tie with rps or croach in a row.
p2states= tuple(product(tuple(range(w2+1)), tuple(range(-1,p2[1]+1)),tuple(range(-1,p2[2]+1)),tuple(range(-1,p2[3]+1))))
states= tuple(product(p1states,p2states))
db={}
for s in states:
	val=None
	#A is the payoff matrix
	#0 is for rps, 1 is for butterfly, 2 nuke, 3 roach
	A= [[None for x in xrange(4)] for x in xrange(4)]
	p1strat= None
	p2strat= None
	db[s]= [val,A,p1strat,p2strat]

def fillTerminalStates(w1,w2):
	'''sets value of leaf nodes, so that recursion can stop
	Making an illegal move means you lose: so you wont ever play it
	If you didnt make an illegal move, but have 3 wins, then you win'''
	for state in states:
		if -1 in state[0]:
			db[state][0] = 0.0
			continue
		if -1 in state[1]:
			db[state][0]= 1.0
			continue
		if -1 in state[0] and -1 in state[1]:
			db[state][0]= .5 #don't think this matters
			continue
		if state[0][0]==w1:
			db[state][0]= 1
			continue
		if state[1][0]==w2: db[state][0]= 0

#this is a messy script, so here I'm modifying the global variable db, so that it contains all the terminal states
fillTerminalStates(w1,w2)

#solvegame is another file in this folder
import solvegame
solve = solvegame.solve

def statechanger(state,action,justtied=False):
	'''This is the meat of the program, it says how to change states.
	rsolve constantly calls statechanger to figure out what state to recursivly call'''
	s=map(list,state)
	#justtied is an optional argument that is only added as True if trr, or cc 
	if not justtied:
		s[0][3] =s[1][3]=p1[3]
	if justtied:
		s[0][3]= s[1][3]= s[0][3] -1
	if action == 'wrr':
		s[0][0]+=1
	elif action == 'lrr':
		s[1][0]+=1
	elif action == 'trr':
		pass
	elif action == 'rb':
		s[0][0]=0
		s[1][0]=0
		s[1][1]+= -1
	elif action == 'rn':
		s[1][0]+=1
		s[1][2]+= -1
	elif action == 'rc':
		s[0][0]+=1
	elif action == 'br':
		s[0][0]=0
		s[1][0]=0
		s[0][1]+= -1
	elif action == 'bb':
		s[0][0]=0
		s[1][0]=0
		s[1][1]+= -1
		s[0][1]+=-1
	elif action == 'bn':
		s[1][0]+=1
		s[0][1]+= -1
		s[1][2]+= -1
	elif action == 'bc':
		s[0][0]=0
		s[1][0]=0
		s[0][1]+= -1
	elif action == 'nr':
		s[0][0]+=1
		s[0][2]+= -1
	elif action == 'nb':
		s[0][0]+=1
		s[0][2]+= -1
		s[1][1]+= -1
	elif action == 'nn':
		s[1][2]+=-1
		s[0][2]+= -1
	elif action == 'nc':
		s[1][0]+=1
		s[0][2]+= -1
	elif action == 'cr':
		s[1][0]+=1
	elif action == 'cb':
		s[0][0]=0
		s[1][0]=0
		s[1][1]+= -1
	elif action == 'cn':
		s[0][0]+=1
		s[1][2]+= -1
	elif action == 'cc':
		pass
	else:
		print "SHOULD NEVER BE HERE!"
		#This else statement prevents the infinite loop that occurs because not everything is implemented.
		#s[0][1] = -1
	return tuple(map(tuple, s))




def rsolve(state):
	'''rsolve for recursive solve. If the state is already solved, return it,
	else start by filling A, and then calling solve on A.'''
	if db[state][0] != None: return db[state][0]
	A= db[state][1]
	if state[0][3]== 0:
		A[0][0]= .5*rsolve(statechanger(state,'wrr')) + .5*rsolve(statechanger(state,'lrr')) 
	else:
		A[0][0]= .33333333*rsolve(statechanger(state,'wrr')) + .3333333*rsolve(statechanger(state,'lrr')) + .3333333*rsolve(statechanger(state,'trr',True))
	A[0][1]=rsolve(statechanger(state,'rb'))
	A[0][2]=rsolve(statechanger(state,'rn'))
	A[0][3]=rsolve(statechanger(state,'rc'))
	A[1][0]=rsolve(statechanger(state,'br'))
	A[1][1]=rsolve(statechanger(state,'bb'))
	A[1][2]=rsolve(statechanger(state,'bn'))
	A[1][3]=rsolve(statechanger(state,'bc'))
	A[2][0]=rsolve(statechanger(state,'nr'))
	A[2][1]=rsolve(statechanger(state,'nb'))
	A[2][2]=rsolve(statechanger(state,'nn'))
	A[2][3]=rsolve(statechanger(state,'nc'))
	A[3][0]=rsolve(statechanger(state,'cr'))
	A[3][1]=rsolve(statechanger(state,'cb'))
	A[3][2]=rsolve(statechanger(state,'cn'))
	A[3][3]=rsolve(statechanger(state,'cc',True))
	solved= solve(A)
	db[state]= [solved[2], A, solved[0],solved[1]]
	return solved[2]
	#I'm worried I have row and col reversed. If funny errors, try swiching

#This line should fill up the whole database
#print isinstance(statechanger(((0,1,2,4),(0,1,2,4)),'wrr'),tuple)
#print db[statechanger(((0,1,2,4),(0,1,2,4)),'wrr')]
rsolve((p1,p2))

#now I want to save the hashtable db to a file that can be loaded.
#To do this I'll pickle it. 
import pickle
output = open('db.pkl', 'wb')
pickle.dump(db, output)
output.close()

# #To get it back run this 
# import pickle
# pkl_file = open('db.pkl', 'rb')
# db = pickle.load(pkl_file)
# pkl_file.close()