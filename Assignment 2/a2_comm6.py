# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:46:19 2023

@author: Hugo Burton
"""

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
    15: [434, 82,  220, 427],
    31: [928, 188, 462, 919],
    35: [961, 190, 486, 967],
    43: [680, 129, 339, 680]
}

upgrade_costs = {
    15: [0, 8587000,  20837000, 42339000],
    31: [0, 18346000, 44625000, 85722000],
    35: [0, 19243000, 45871000, 88655000],
    43: [0, 13418000, 32794000, 63811000]
}

pipeline_cost = 200000

cost = {15: 85, 
        31: 62, 
        35: 75, 
        43: 66}

pipe_capacity = 281 # MJ (base)

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


Z = {}
for n in N:
    for u in U:
        Z[(n, u)] = m.addVar(vtype=GRB.INTEGER)

# Objective
m.setObjective(quicksum(
    quicksum(upgrade_costs[n][u] * Z[(n, u)] for n in N if n in upgrade_costs)
    for u in U), 
               GRB.MINIMIZE)

# One upgrade only or no upgrades at all

for n in N:
    if n in new_capacity.keys():
        m.addConstr(quicksum(Z[n,u] for u in U) == 1)
    else:
        m.addConstr(quicksum(Z[n,u] for u in U) == 0)

# Generator capacity
for n in N:
    t = 1
    if n not in new_capacity:
        m.addConstr(X[(n,t)] <= 0)
    else:
        m.addConstr(X[(n,t)] <= new_capacity[n][0] 
                    + quicksum(new_capacity[n][u] * Z[n,u] for u in U if u != 0))
 
# Demand at 10 years

for n in N:
    # for t in T:
    t = 1
    m.addConstr(X[(n,t)] + quicksum(Y[(p,t)] for p in P if p[1] == n) == 
            demand[n][t] + quicksum(Y[(p,t)] for p in P if p[0] == n))
    
m.setParam('MIPGap', 0)
m.optimize()

print("-" * 100)

print(m.objVal)

print("Upgrades")
t = 1
print(f"| {'':<20} | {'':<24} |")

# Print gas production for each node
print(f"| {'Gas station (node)':<20} |",end='')
for n in N:
    if X[(n,t)].x > 0:
        print(f" {n:<6} |", end='')
print()
print(f"| {'Gas Produced (MJ)':<20} |",end='')
for n in N:
    if X[(n,t)].x > 0:
        print(f" {round(X[n,t].x, 3):<6} |", end='')
print()
print(f"| {'Capacity (MJ)':<20} |",end='')
for n in N:
    if X[(n,t)].x > 0:
        cap = new_capacity[n][0] + sum(new_capacity[n][u] * Z[n,u].x for u in U if u != 0)
        print(f" {cap:<6} |", end='')
print()
print(f"| {'Upgrade Purchased':<20} |",end='')
for n in N:
    for u in U:
        if Z[(n,u)].x > 0:
            print(f" {u:<6} |", end='')
print()    
print(f"| {'Upgrade Price':<20} |",end='')
for n in N:
    for u in U:
        if Z[(n, u)].x > 0:
            print(f" {round(upgrade_costs[n][u] * Z[(n, u)].x,2):<10} |", end='')
print()    
print(f"| {'':<20} | {'':<24} |")




