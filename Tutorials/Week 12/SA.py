import math
import random
import pylab



def RunSA(Solution,Cost,ChooseNeigh,MoveToNeigh,T,N,alpha):
    E = Cost(Solution)
    Best = E
    CostArr = [E]
    BestArr = [Best]
    BestSol = list(Solution)
    for i in range(N):
        delta,neighbour = ChooseNeigh(Solution)
        if delta < 0 or math.exp(-delta/T) > random.random():
            MoveToNeigh(Solution,neighbour)
            E += delta
            if E < Best:
                Best = E
                BestSol = list(Solution)
        CostArr.append(E)
        BestArr.append(Best)
        T *= alpha
    print (Best, T)
    pylab.plot(range(N+1),CostArr)
    pylab.plot(range(N+1),BestArr)
    pylab.show()
    return BestSol

