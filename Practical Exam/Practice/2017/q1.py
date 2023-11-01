# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 17:35:07 2023

@author: Hugo Burton
"""

from gurobipy import *

# Sets
P = range(15)
C = range(4)

# Data

mass = [70, 90, 100, 110, 120, 130, 150, 180, 210, 220, 250, 280, 340, 350, 400]

capmax = 1000 #kg
minpack = 3 # packages


# Model

m = Model("Packages")

# Variables
X = {(p,c): m.addVar(vtype=GRB.BINARY) for p in P for c in C}

# Constraints

for p in P:
    m.addConstr(quicksum(X[p,c] for c in C) == 1)

m.addConstr(quicksum(X[p,0] * mass[p] for p in P) == quicksum(X[p,3] * mass[p] for p in P))
m.addConstr(quicksum(X[p,1] * mass[p] for p in P) == quicksum(X[p,2] * mass[p] for p in P))

for c in C:
    m.addConstr(quicksum(X[p,c] * mass[p] for p in P) <= capmax)
    m.addConstr(quicksum(X[p,c] for p in P) >= minpack)
    
m.optimize()

Comps = ["A", "B", "C", "D"]

for c in C:
    print("Compartment:", Comps[c])
    for p in P:
        if X[p,c].x == 1:
            print("Package", p, "with mass", mass[p], "kg.")
            
    print("\nTotal mass =", sum(X[p,c].x * mass[p] for p in P))
        
    print("")

print("Total Total mass =", sum(X[p,c].x * mass[p] for p in P for c in C))