# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 16:46:44 2023

@author: Hugo Burton
"""

from gurobipy import *
import pandas
import math

# Use read_csv to read the CSV data into a pandas DataFrame
nodes = pandas.read_csv("nodes2.csv")
pipelines = pandas.read_csv("pipelines.csv")

N = range(len(nodes['Node']))

# To show how a DataFrame can be accessed, extract a list of node demands
print(nodes)
print(type(nodes))
demand = nodes.loc[:, 'D0':'D13'].values.tolist()
print(demand)
print(len(demand))
print(type(demand))

# capacity and cost for each generator node
capacity = {15: 434, 
            31: 928, 
            35: 961, 
            43: 680}
cost = {15: 85, 
        31: 62, 
        35: 75, 
        43: 66}

# P[i,j] gives the distance (km) from node i to node j via pip p
P = {}
for j in range(len(pipelines['Pipeline'])):
    n1 = pipelines['Node1'][j]
    n2 = pipelines['Node2'][j]
    distance = math.hypot(nodes['X'][n1]-nodes['X'][n2],nodes['Y'][n1]-nodes['Y'][n2])
    P[n1,n2] = distance
    # create a pipe in both directions
    #P[n2,n1] = distance

# Days
days = range(14)    # Two weeks

m = Model("PPC")

E = 0.01 # $ / MJ / h

# Variables
X = {}
for p in P:
    for t in days:
        X[(p, t)] = m.addVar()

Y = {}
for n in N:
    for t in days:
        Y[(n, t)] = m.addVar()


# Objective
# Revised in comunication 3 to sum over days
m.setObjective(quicksum(quicksum(cost[n] * Y[(n, t)] for n in N if n in cost) + 
               E * quicksum(P[p] * X[(p,t)] for p in P) for t in days), 
               GRB.MINIMIZE)

# Flow balance constraint
# Communication 3 - Revised for 2 week forecast
for n in N:
    for t in days:
        m.addConstr(Y[(n,t)] + quicksum(X[(p,t)] for p in P if p[1] == n) == 
                demand[n][t] + quicksum(X[(p,t)] for p in P if p[0] == n))
    
# Generator capacity
for n in N:
    for t in days:
        if n not in capacity:
            m.addConstr(Y[(n,t)] <= 0)
        else:
            m.addConstr(Y[(n,t)] <= capacity[n])

# Communication 2
# Pipelines have a maximum capacity of 487 MJ per day

for p in P:
    for t in days:
        m.addConstr(X[(p,t)] <= 487) # MJ / day limit

# Communication 4
# Each supplier limited to 11606 MJ gas over two week periodfor p in P
for n in N:
    m.addConstr(quicksum(Y[n, t] for t in days) <= 11606)

m.optimize()

print("Total cost = ", round(m.objval, 5))
print()
for t in days:
    print("Day", t)
    for n in N:
        if Y[(n,t)].x > 0:
            print("Gas produced", n, "=", round(Y[(n,t)].x, 3), "(MJ)")
    print()
    for p in P:
        if X[(p,t)].x > 0:
            print("Gas flowed through", p, "=", round(X[(p,t)].x, 3), " (MJ)")
            
    print()

print()
 
        
print("Done")