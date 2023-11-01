#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 16:06:59 2023

@author: luke
"""

# -*- coding: utf-8 -*-

from gurobipy import *
import pandas
import math

# Use read_csv to read the CSV data into a pandas DataFrame
nodes = pandas.read_csv("nodes3.csv")
pipelines = pandas.read_csv("pipelines.csv")

N = range(len(nodes['Node']))
T = [0,1]
# To show how a DataFrame can be accessed, extract a list of node demands
demand10 = [nodes['Year10'][j] for j in N]
demand5 = [nodes['Year5'][j] for j in N]

# capacity and cost for each generator node
capacity = { 9: 385, 15: 794, 27: 788, 38: 590 }

pipeUCost = 200000
pipeCap = 308
S = [9, 15, 27, 38]

U = [0, 1, 2, 3]

capUpgrades = { 
    9: [385,87,189,392], 
    15: [794,160,399,799], 
    27: [788,156,399,792], 
    38:[590,120,295,594] 
    }
costUpgrades = { 
    9: [0,7512000,19097000,36563000], 
    15: [0,16308000,37803000,72836000], 
    27: [0,15714000,37365000,71861000], 
    38: [0,11957000,29106000,56036000] 
    }

dis = [0, 0.3]
# P[i,j] gives the distance (km) from node i to node j
P = {}
for j in range(len(pipelines['Pipeline'])):
    n1 = pipelines['Node1'][j]
    n2 = pipelines['Node2'][j]
    distance = math.hypot(nodes['X'][n1]-nodes['X'][n2],nodes['Y'][n1]-nodes['Y'][n2])
    P[n1,n2] = distance
    
TotalDemand10 = sum(demand10)
TotalDemand5 = sum(demand5)

currentCap = 0
for currentSup in capacity:
    currentCap += capacity[currentSup]

m = Model("PacificParadise")

# Variables
# Gas produced
X = {(n,t): m.addVar() for n in N for t in T}

# Gas flow
Y = {(p,t): m.addVar() for p in P for t in T}

# Supplier upgrades
SU = {(n,t,u): m.addVar(vtype=GRB.BINARY) for n in N for t in T for u in U}

# Pipe upgrades
PU = {(p,t): m.addVar(vtype=GRB.BINARY) for p in P for t in T}
    
# Objective

m.setObjective(quicksum(quicksum(costUpgrades[n][u] * SU[n,t,u] * (1 - dis[t]) for n in S for u in U) 
                      + quicksum(pipeUCost * P[p] * (1 - dis[t]) * PU[p,t] for p in P)
            for t in T), GRB.MINIMIZE)

# Constraints
# generator upgrades
for n in S:
    m.addConstr(quicksum(SU[n,t,u] for u in [1,2,3] for t in T) <= 1)
    for t in T:
        m.addConstr(quicksum(SU[n,t,u] for u in U) == 1)

for n in N:
    if n not in S:
        m.addConstr(quicksum(SU[n,t,u] for u in U for t in T) == 0)

        
# # m.addConstr(quicksum(X1[n] for n in S) >= TotalDemand5)

# # m.addConstr(quicksum(X2[n] for n in S) >= TotalDemand10)

# Generator capacity constraint
for n in S:
    for t in T:
        m.addConstr(X[n,t] <= capacity[n] + quicksum(capUpgrades[n][u] * quicksum(SU[n,j,u] for j in T if j <= t) for u in [1,2,3]))
    
# Non-generator nodes
for n in N:
    for t in T:
        if n not in S:
            m.addConstr(X[n,t] == 0)


# Flow balance constraint
for n in N:
    t = 0
    m.addConstr(X[n,t] + quicksum(Y[p,t] for p in P if p[1] == n) == 
                demand5[n] + quicksum(Y[p,t] for p in P if p[0] == n))

    t = 1
    m.addConstr(X[n,t] + quicksum(Y[p,t] for p in P if p[1] == n) == 
                demand10[n] + quicksum(Y[p,t] for p in P if p[0] == n))
    

# Pipe constraints
for p in P:
    for t in T:
        m.addConstr(Y[p,t] <= (1+quicksum(PU[p,j] for j in T if j <= t)) * pipeCap)

m.setParam('MIPGap', 0)
m.optimize()

print("Total cost =", m.objval)

    