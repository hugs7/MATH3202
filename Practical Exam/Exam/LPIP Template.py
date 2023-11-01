# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:43:35 2023

@author: Hugo Burton
"""


from gurobipy import *

# Data



# Model

m = Model("Q1")

# Variables
X = { (a,b,c): m.addVar(vtype=GRB.xxxx   )  }

# Objective Function

m.setObjective(X, GRB.xxxxxx)


# Constraints


m.optimize()

print()
print("Objective Value: ", m.objVal)

