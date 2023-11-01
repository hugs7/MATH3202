# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:06:45 2023

@author: Hugo Burton

This python program will aim to solve the Farmer Jones problem in pyton. The 
problem is given as follows

Farmer Jones bakes two types of cake (chocolate and plain) to supplement his 
income. Each chocolate cake can be sold for $4 and each plain cake can be 
sold for $2. Each chocolate cake requires 20 minutes of baking time, 250 mL 
of milk and 4 eggs, while each plain cakeneeds 50 minutes baking, 200 mL of 
milk and only 1 egg. In each day there are eight hours of baking time 
available. Farmer Jones’ henslay30eggs eachdayandhiscowsproduce5 L of milk. 
How many of each type of cake should Farmer Jones bake each day to maximize 
his revenue?
"""

from gurobipy import *

# Define model
m = Model("Farmer Jones")

# Add variables
x1 = m.addVar()
x2 = m.addVar()

# Set objective. We want to set the objective to the profit function of the 
# cakes
m.setObjective(4 * x1 + 2 * x2, GRB.MAXIMIZE)


# Constraints
m.addConstr(20 * x1 + 50 * x2 <= 480)
m.addConstr(250 * x1 + 200 * x2 <= 5000)
m.addConstr(4 * x1 + 1 * x2 <= 30)

m.optimize()

# Pull out the objective value in a print statement
print("Revenue is", m.objval)
print("\n")
print (x1.x, "chocolate cakes")
print (x2.x, "plain cakes")

print("Done")
