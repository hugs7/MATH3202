# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:46:19 2023

@author: Hugo Burton
"""

from gurobipy import *
import pandas
import math

# Use read_csv to read the CSV data into a pandas DataFrame
nodes = pandas.read_csv("nodes3lucy.csv")
pipelines = pandas.read_csv("pipelineslucy.csv")     # Same as A1

N = range(len(nodes['Node']))
U = range(len([0,1,2,3]))    # Upgrades where 0 is no upgrade
S = range(3)

# To show how a DataFrame can be accessed, extract a list of node demands
#print(nodes)
#print(type(nodes))
demand = nodes.loc[:, 'Year5':'Year10'].values.tolist()
print(demand)
# print(len(demand))
# print(type(demand))

# capacity and cost for each generator node

new_capacity = {
    5 :[397,86,199,386],
    36:[825,162,416,830],
    38:[788,152,391,783],
    45:[581,109,289,592]
}

upgrade_costs = {
    5 :[0,7866000,19717000,36454000],
    36:[0,15931000,39169000,78423000],
    38:[0,15439000,37763000,72511000],
    45:[0,11295000,28059000,53364000]
}

pipeline_cost = 200000

discount = {0: 0.0, 1: 0.3}

pipe_capacity = 327 # MJ (base)

# Scenarios (comm 9)

# Indexed by (year t, scenario s)
Scenarios = {
    (0, 0): 0.0,
    (0, 1): 0.0,
    (0, 2): 0.0,
    
    (1, 0): -0.2,
    (1, 1): 0.0,
    (1, 2): 0.2
}
# Scenario probabilities. Indexed by [year t][scenario s]
ScenarioProb = [1/3 for _ in S]
print(ScenarioProb)
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
T = range(2)    # Two weeks as a range in days

m = Model("PPG2")

# lam = 0.01 # $ / (MJ KM) - cost to move gas per MJ KM
# epsilon = 0.1 # $ / MJ - cost to store gas per MJ

# Variables

X = {} # Gas produced
for n in N:
    for t in T:
        for s in S:
            X[(n, t, s)] = m.addVar()

Y = {} # Flow of gas at y=5
for p in P:
    for t in T:
        for s in S:
            Y[p,t,s] = m.addVar()

Z = {}      # Upgrade supplier
for n in N:
    for t in T:
        for u in U:
            for s in S:
                Z[n, t, u, s] = m.addVar(vtype=GRB.BINARY)

PU = {}     # Pipeline upgrade - 0 no upgrade, 1 upgade at 200,000 cost
for p in P:
    for t in T:
        for s in S:
            PU[p, t, s] = m.addVar(vtype=GRB.BINARY)

# Objective
m.setObjective(quicksum(ScenarioProb[s] * (quicksum(
    quicksum(upgrade_costs[n][u] * (1 - discount[t]) * Z[n, t, u, s] for n in N if n in upgrade_costs for u in U) + 
    quicksum(pipeline_cost * (1 - discount[t]) * PU[p, t, s] * P[p] for p in P) for t in T)) for s in S), 
    GRB.MINIMIZE)

# Generator capacity
for n in N:
    for t in T:
        for s in S:
            if n not in new_capacity:
                m.addConstr(X[(n,t,s)] == 0)
            else:
                m.addConstr(X[(n,t,s)] <= new_capacity[n][0] 
                            + quicksum(
                                new_capacity[n][u] * 
                                quicksum(Z[n, t_star, u, s] for t_star in T if t_star <= t) 
                                for u in U if u != 0)
                            )
                # Base capacity + upgrade 1 2 or 3.

# Generator Upgrades
for n in N:
    for s in S:
        if n in new_capacity.keys(): # if node is a generator
            m.addConstr(quicksum(Z[n, t, u, s] for u in U if u != 0 for t in T) <= 1)
            for t in T:
                m.addConstr(quicksum(Z[n, t, u, s] for u in U) == 1)
        else:           # if node is not a generator
            m.addConstr(quicksum(Z[n, t, u, s] for u in U for t in T) == 0)
    
    # All decisions in time step 1 for each scenario need to match given we cannot
    # plan for what scenario will happen in time step 1
    for u in U:
        t = 0    
        m.addConstr(Z[n,t,u,0] == Z[n,t,u,1])
        m.addConstr(Z[n,t,u,1] == Z[n,t,u,2])

# Pipeline capacity upgrade
for p in P:
    for s in S:
        for t in T:
            m.addConstr(Y[p, t, s] <= (1 + quicksum((PU[p, t_star, s]) for t_star in T if t_star <= t)) * pipe_capacity) # MJ / day limit

        m.addConstr(quicksum(PU[p, t, s] for t in T) <= 1)     # Can't upgrade pipe twice
        
    # All decisions in time step 1 for each scenario need to match given we cannot
    # plan for what scenario will happen in time step 1
    t = 0
    m.addConstr(PU[p,t,0] == PU[p,t,1])
    m.addConstr(PU[p,t,1] == PU[p,t,2])
 
# Demand
for n in N:
    for s in S:
        for t in T:
            m.addConstr(X[n,t,s] + quicksum(Y[p,t,s] for p in P if p[1] == n) ==
                        demand[n][t] * (1 + Scenarios[t,s])
                        + quicksum(Y[p,t,s] for p in P if p[0] == n))
    
m.setParam('MIPGap', 0)
m.optimize()

print("-" * 100)

print(m.objVal)

# for s in S:
#     print("-" * 100)
#     print(f"Scenario {s}")
#     for t in T:
#         print(f"Year {(5 * (1 + t))}\n")
#         print("Upgrades")
#         print(f"| {'':<20} | {'':<23} |")
        
#         # Print gas production for each node
#         print(f"| {'Gas station (node)':<20} |",end='')
#         for n in N:
#             if X[(n,t,s)].x > 0:
#                 print(f" {n:<10} |", end='')
#         print()
#         print(f"| {'Gas Produced (MJ)':<20} |",end='')
#         for n in N:
#             if X[(n,t,s)].x > 0:
#                 print(f" {round(X[n,t,s].x, 3):<10} |", end='')
#         print()
#         print(f"| {'Capacity (MJ)':<20} |",end='')
#         for n in N:
#             if X[(n,t,s)].x > 0:
#                 cap = new_capacity[n][0] + sum(new_capacity[n][u] * Z[n, t, u, s].x for u in U if u != 0)

#                 print(f" {cap:<10} |", end='')
#         print()
#         print(f"| {'Upgrade Purchased':<20} |",end='')
#         for n in N:
#             for u in U:
#                 if Z[(n, t, u, s)].x > 0:
#                     print(f" {u:<10} |", end='')
#         print()
#         print(f"| {'Upgrade Price':<20} |",end='')
#         for n in N:
#             for u in U:
#                 if Z[(n, t, u, s)].x > 0:
#                     print(f" {round(upgrade_costs[n][u] * (1 - discount[t]) * Z[(n, t, u, s)].x,2):<10} |", end='')
#         print()    
#         print(f"| {'':<20} | {'':<23} |")
        
#         C = 290
#         # Print pipes
#         print(f"| {'Pipe (x,y)':<10} | {'Dist (km)':<10} | {'Gas Flw MJ':<10} | {'Max flow MJ':<12} | {'Upgrade':<10} | {'Cost ($)':<10}")
#         for p, d in P.items():
#             if Y[p,t,s].x > 0:
#                 print(f"| {str(p):<10} | {round(d,2):<10} | {int(Y[p,t,s].x):<10} | {int(pipe_capacity * (1 + PU[p, t, s].x)):<12} | {str(int(PU[p, t, s].x)):<10} | {str(int(pipeline_cost * (1 - discount[t]) * PU[p, t, s].x * P[p])):<10} |")
        
#         print()
        
#         print("Pipe upgrades")
#         print(f"| {'Pipe (x,y)':<15} | {'Upgrade':<15} | {'Cost ($)':<15}")
#         for p in P:
#             if Y[p,t].x > 0:
#                 print(f"| {str(p):<15} | {str(int(PU[p, t].x)):<15} | {str(int(PU[p, t].x * pipeline_cost)):<15} |")
    
#     print("Pipeline total cost: $", int(sum(pipeline_cost * (1 - discount[t]) * PU[p, t, s].x * P[p] for p in P for t in T)), sep='')
