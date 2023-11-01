# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 16:58:38 2023

@author: Hugo Burton
"""

from gurobipy import *

Ports = ['Manly','Cleveland','Dunwich']
P = range(len(Ports))
B = range(18)

# Boat, port
Travel = [
	[29, 27, 21], [39, 18, 30], [40, 20, 31], [33, 19, 27], [35, 29, 36], [21, 23, 20],
	[30, 41, 32], [37, 27, 36], [20, 25, 34], [36, 28, 20], [24, 23, 25], [38, 22, 40], 
	[39, 19, 27], [30, 18, 28], [40, 20, 32], [21, 32, 40], [23, 18, 20], [31, 18, 20]
]

Cap = [8, 8, 6]


m = Model("Boats in Storm")

# Variables
X = { (b,p): m.addVar(vtype=GRB.INTEGER) for b in B for p in P }
Y = m.addVar(vtype=GRB.CONTINUOUS)

# Objective Function

m.setObjective(Y, GRB.MINIMIZE)


# Constraints

for p in P:
    m.addConstr(quicksum(X[b,p] for b in B) <= Cap[p])
    
for b in B:
    m.addConstr(quicksum(X[b,p] for p in P) == 1)
    m.addConstr(Y >= quicksum(Travel[b][p] * X[b,p] for p in P))
    
m.optimize()

print("Maximum Travel Time: ", m.objVal, "minutes")


for p in P:
    print("\nPort")
    for b in B:
        if X[b,p].x == 1:
            print(b, "docking at port with time", Travel[b][p], "minutes")
