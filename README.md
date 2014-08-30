ultimaterps
===========

Implementation for solving the game ultimaterps. Devised by Nick Altieri, and Sylvan Arevalo

The file ultimaterps.py will generate the file db.pkl if you run it. It uses the file solvegame.py,
which solves a game matrix. I found the code for solvegame.py online and copied and pasted it.

The file db.pkl can be unpickled to get a hashtable which can be queried like this:

In [95]: db[((1,0,1,4),(2,1,0,4))]
Out[95]: 
[0.41690101092669535,
 [[0.37153484615873206, 0.6681253527653382, 1.0, 0.6979628681638872],
  [0.0, 0.0, 0.0, 0.0],
  [0.49185936495592664, 0.49794235798353986, 1.0, 0],
  [0, 0.6681253527653382, 1.0, 0.4166417189561096]],
 [0.68, 0.0, 0.32, 0.0],
 [0.84, 0.0, 0.0, 0.16]]
 
 
Understanding this query: The input is of the form:
((w,b,n,t),(w,b,n,t)) where w= wins, b= butterfly, n= nukes, t= consecuitive 
ties you still have before the game ends in a draw
(I added t in order to make the game easier to solve.) 
The starting state is: ((0,1,2,4),(0,1,2,4))
 
The output is a list:
[Probability of P1 win,
A,
p1 strategy,
p2 strategy]

Where A is the value of the game if that strategy pair was chosen.
A[0][1] is the value of the game if p1 plays rock, and p2 plays butterfly.
Here we see that the value of that game is .668... which makes sense, 
because that is how much better it is to be up a nuke when the game is tied at 0,0

The strategies for p1 and p2 show the percentage you should play [rps, butterfly, nuke, cockroach]


