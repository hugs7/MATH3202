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

# Sets

cakes = ["Chocolate", "Plain"]
resources = ["Eggs", "Milk", "Time"]


# Data

revenue = [4, 2]
usage = [[4, 250, 20], [1, 200, 50]]
available = [30, 5000, 480]

# Define model
m = Model("Farmer Jones")

# Variables

x = dict()
for i, cake in enumerate(cakes):
    x[i] = m.addVar()

# Objective

m.setObjective(quicksum(revenue[i] * x[i] for i in range(len(cakes))), 
               GRB.MAXIMIZE)

# Constraints

for i, r in enumerate(resources):
    m.addConstr(quicksum(usage[j][i] * x.get(j) for j in range(len(cakes))) <= available[i])


m.optimize()

# Pull out the objective value in a print statement
print("Revenue is", m.objval)
print("\n")
for i, c in enumerate(cakes):
    print(x.get(i).x, c, "cakes")

print("Done")
