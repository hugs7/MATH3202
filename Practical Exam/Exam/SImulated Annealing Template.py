import math
import random
import pylab


def Cost(B):
    return 0

def ChooseNeigh(CurSol):
    pass


def MoveToNeigh(CurSol):
    pass


def RunSA(Solution,Cost,ChooseNeigh,MoveToNeigh,T,N,alpha):
    E = Cost(Solution)
    Best = E
    CostArr = [E]
    BestArr = [Best]
    BestSol = dict(Solution)  # since Solution will be a dictionary (board)
    for i in range(N):
        delta,neighbour = ChooseNeigh(Solution)
        if delta < 0 or math.exp(-delta/T) > random.random():
            MoveToNeigh(Solution,neighbour)
            E += delta
            if E < Best:
                Best = E
                BestSol = dict(Solution)
        CostArr.append(E)
        BestArr.append(Best)
        T *= alpha
    print (Best, T)
    pylab.plot(range(N+1),CostArr)
    pylab.plot(range(N+1),BestArr)
    pylab.show()
    return BestSol

Solution = []

T = 10000
N = 250000
alpha = 0.9999


BestSol = RunSA(Solution, Cost, ChooseNeigh, MoveToNeigh, T, N, alpha)