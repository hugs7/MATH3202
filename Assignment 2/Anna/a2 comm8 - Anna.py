# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:46:19 2023

@author: Hugo Burton
"""

# Communication 5

from gurobipy import *
import pandas
import math

# Use read_csv to read the CSV data into a pandas DataFrame
nodes = pandas.read_csv("nodes3.csv")
pipelines = pandas.read_csv("pipelines.csv")     # Same as A1

N = range(len(nodes['Node']))
U = range(len([0,1,2,3]))    # Upgrades where 0 is no upgrade

# To show how a DataFrame can be accessed, extract a list of node demands
#print(nodes)
#print(type(nodes))
demand = nodes.loc[:, 'Year5':'Year10'].values.tolist()
# print(demand)
# print(len(demand))
# print(type(demand))

# capacity and cost for each generator node
# capacity = {15: 434, 
            # 31: 928, 
            # 35: 961, 
            # 43: 680}

new_capacity = {
    2: [462, 92, 238, 469],
    33: [955, 199, 471, 953],
    35: [957, 182, 476, 961],
    41: [704, 145, 353, 709]
}

upgrade_costs = {
    2: [0, 9208000,  22585000, 42199000],
    33: [0, 19380000, 46170000, 88701000],
    35: [0, 19106000, 45873000, 86905000],
    41: [0, 14341000, 32569000, 62730000]
}

pipeline_cost = 200000

discount = {0: 0.0, 1: 0.3}

pipe_capacity = 439 # MJ (base)

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
T = range(2)    # 5 years, 10 years

m = Model("PPC2")

lam = 0.01 # $ / (MJ KM) - cost to move gas per MJ KM
epsilon = 0.1 # $ / MJ - cost to store gas per MJ

# Variables

X = {} # Gas produced
for n in N:
    for t in T:
        X[(n, t)] = m.addVar()

Y = {} # Flow of gas
for p in P:
    for t in T:
        Y[(p, t)] = m.addVar()

Z = {}      # Upgrade supplier
for n in N:
    for t in T:
        for u in U:
            Z[(n, t, u)] = m.addVar(vtype=GRB.BINARY)

PU = {}     # Pipeline upgrade - 0 no upgrade, 1 upgade at 200,000 cost
for p in P:
    for t in T:
        PU[p, t] = m.addVar(vtype=GRB.BINARY)

# Objective
# m.setObjective(quicksum(
#     quicksum(upgrade_costs[n][u] * (1 - discount[t]) * Z[(n, t, u)] for n in N if n in upgrade_costs)
#     for t in T for u in U) + quicksum(pipeline_cost * (1 - discount[t]) * PU[p, t] * P[p] for p in P for t in T), 
#                GRB.MINIMIZE)

m.setObjective(quicksum(
        quicksum(upgrade_costs[n][u] * (1 - discount[t]) * Z[(n, t, u)] for n in N if n in upgrade_costs for u in U) + 
        quicksum(pipeline_cost * (1 - discount[t]) * PU[p, t] * P[p] for p in P) 
    for t in T), 
    GRB.MINIMIZE)

# Generator Upgrades
for n in N:
    if n in new_capacity.keys(): # if node is a generator
        m.addConstr(quicksum(Z[n, t, u] for u in U if u != 0 for t in T) <= 1)
        for t in T:
            m.addConstr(quicksum(Z[n, t, u] for u in U) == 1)
    else:
        m.addConstr(quicksum(Z[n, t, u] for u in U for t in T) == 0)

# Generator capacity
for n in N:
    for t in T:
        if n not in new_capacity:
            m.addConstr(X[(n,t)] <= 0)
        else:
            m.addConstr(X[(n,t)] <= new_capacity[n][0] 
                        + quicksum(
                            new_capacity[n][u] * 
                            quicksum(Z[n, t_star, u] for t_star in T if t_star <= t) 
                            for u in U if u != 0)
                        )
            # Base capacity + upgrade 1 2 or 3.

# Pipeline capacity upgrade
for p in P:
    for t in T:
        m.addConstr(Y[(p, t)] <= (1 + quicksum((PU[p, t_star]) for t_star in T if t_star <= t)) * pipe_capacity) # MJ / day limit
        
    m.addConstr(quicksum(PU[p, t] for t in T) <= 1)     # Can't upgrade pipe twice
 
# Demand at 5 and 10 years
for n in N:
    for t in T:
        m.addConstr(X[(n,t)] + quicksum(Y[(p,t)] for p in P if p[1] == n) == 
                    demand[n][t] + quicksum(Y[(p,t)] for p in P if p[0] == n))
    
m.setParam('MIPGap', 0)
m.optimize()

print("-" * 100)

print(m.objVal)

print("-" * 100)

for t in T:
    print(f"Year {(5 * (1 + t))}\n")
    print("Upgrades")
    print(f"| {'':<20} | {'':<23} |")
    
    # Print gas production for each node
    print(f"| {'Gas station (node)':<20} |",end='')
    for n in N:
        if X[(n,t)].x > 0:
            print(f" {n:<10} |", end='')
    print()
    print(f"| {'Gas Produced (MJ)':<20} |",end='')
    for n in N:
        if X[(n,t)].x > 0:
            print(f" {round(X[n,t].x, 3):<10} |", end='')
    print()
    print(f"| {'Capacity (MJ)':<20} |",end='')
    for n in N:
        if X[(n,t)].x > 0:
            cap = new_capacity[n][0] + sum(new_capacity[n][u] * Z[n, t, u].x for u in U if u != 0)
            print(f" {cap:<10} |", end='')
    print()
    print(f"| {'Upgrade Purchased':<20} |",end='')
    for n in N:
        for u in U:
            if Z[(n, t, u)].x > 0:
                print(f" {u:<10} |", end='')
    print()
    print(f"| {'Upgrade Price':<20} |",end='')
    for n in N:
        for u in U:
            if Z[(n, t, u)].x > 0:
                print(f" {round(upgrade_costs[n][u] * (1 - discount[t]) * Z[(n, t, u)].x,2):<10} |", end='')
    print()    
    print(f"| {'':<20} | {'':<23} |")
    
    C = 290
    # Print pipes
    print(f"| {'Pipe (x,y)':<10} | {'Gas Flow':<10} | {'Maximum flow':<12} | {'Upgrade':<10} | {'Cost ($)':<10}")
    for p in P:
        if Y[p,t].x > 0:
            print(f"| {str(p):<10} | {int(Y[p,t].x):<10} | {int(pipe_capacity * (1 + PU[p, t].x)):<12} | {str(int(PU[p, t].x)):<10} | {str(int(pipeline_cost * (1 - discount[t]) * PU[p, t].x * P[p])):<10} |")
    
    print()
    
    # print("Pipe upgrades")
    # print(f"| {'Pipe (x,y)':<15} | {'Upgrade':<15} | {'Cost ($)':<15}")
    # for p in P:
    #     if Y[p,t].x > 0:
    #         print(f"| {str(p):<15} | {str(int(PU[p, t].x)):<15} | {str(int(PU[p, t].x * pipeline_cost)):<15} |")

print("Pipeline total cost: $", int(sum(pipeline_cost * (1 - discount[t]) * PU[p, t].x * P[p] for p in P for t in T)), sep='')





