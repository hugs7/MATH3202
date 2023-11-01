import math
import random
from gurobipy import *
import pylab

def Distance(p1, p2):
  return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

nLoc = 1500
N = range(nLoc)
Square = 1000
random.seed(nLoc)
Pos = [(random.randint(0,Square), random.randint(0,Square)) for i in N]

# D is the cost matrix
D = [[Distance(Pos[i],Pos[j]) for j in N] for i in N]

# Set up the random initial assignment
Assignment = list(N)
random.shuffle(Assignment)

# Generic SA function

def RunSA(Initial,Cost,ChooseNeigh,MoveToNeigh,T,N,alpha):
    E = Cost(Initial)
    Best = E
    CostArr = [E]
    BestArr = [Best]
    for i in range(N):
        delta,neighbour = ChooseNeigh(Initial)
        if delta < 0 or math.exp(-delta/T) > random.random():
            MoveToNeigh(Initial,neighbour)
            E += delta
            if E < Best:
                Best = E
        CostArr.append(E)
        BestArr.append(Best)
        T *= alpha
	# This code shows the progress
    print E, T
    pylab.plot(range(N+1),CostArr)
    pylab.plot(range(N+1),BestArr)
    pylab.show()

# Problem-specific functions

def Cost(Assignment):


def ChooseNeigh(Assignment):
    

def MoveToNeigh(Assignment, neigh):

