# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 16:46:44 2023

@author: Hugo Burton
"""
# Communication 5

from gurobipy import *
import pandas
import math

# Use read_csv to read the CSV data into a pandas DataFrame
nodes = pandas.read_csv("nodes2.csv")
pipelines = pandas.read_csv("pipelines.csv")

N = range(len(nodes['Node']))

# To show how a DataFrame can be accessed, extract a list of node demands
#print(nodes)
#print(type(nodes))
demand = nodes.loc[:, 'D0':'D13'].values.tolist()
#print(demand)
#print(len(demand))
#print(type(demand))

# capacity and cost for each generator node
capacity = {15: 434, 
            31: 928, 
            35: 961, 
            43: 680}
cost = {15: 85, 
        31: 62, 
        35: 75, 
        43: 66}

M = 487
G = 11606

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
T = range(14)    # Two weeks as a range in days

m = Model("PPC")

lam = 0.01 # $ / (MJ KM) - cost to move gas per MJ KM
epsilon = 0.1 # $ / MJ - cost to store gas per MJ

# Variables

X = {} # Gas produced
for n in N:
    for t in T:
        X[(n, t)] = m.addVar()

Y = {} # Flow of gas in
Z = {} # flow of gas out.
delta = {}   # Delta in flow per pipe for day
for p in P:
    for t in T:
        Y[(p, t)] = m.addVar()
        Z[(p, t)] = m.addVar()
        delta[(p, t)] = m.addVar()

# Objective
# Revised in communication 3 to sum over days
# Revised in communication 5 for flow inbalance
m.setObjective(quicksum(quicksum(cost[n] * X[(n, t)] for n in N if n in cost) + 
               quicksum(lam * P[p] * Y[(p,t)] + epsilon * delta[(p, t)] for p in P) for t in T), 
               GRB.MINIMIZE)

# Flow balance constraint
# Communication 3 - Revised for 2 week forecast
for n in N:
    for t in T:
        # m.addConstr(X[(n,t)] + quicksum(Y[(p,t)] for p in P if p[1] == n) == 
        #         demand[n][t] + quicksum(Y[(p,t)] for p in P if p[0] == n))
        m.addConstr(X[(n,t)] + quicksum(Z[(p,t)] for p in P if p[1] == n) == 
                demand[n][t] + quicksum(Y[(p,t)] for p in P if p[0] == n))
    
# Generator capacity
for n in N:
    for t in T:
        if n not in capacity:
            m.addConstr(X[(n,t)] <= 0)
        else:
            m.addConstr(X[(n,t)] <= capacity[n])

# Communication 2
# Pipelines have a maximum capacity of M (487) MJ per day
for p in P:
    for t in T:
        m.addConstr(Y[(p,t)] <= M) # MJ / day limit
        m.addConstr(Z[(p,t)] <= M) # MJ / day limit

# Communication 4
# Each supplier limited to G MJ gas over two week periodfor p in P
for n in N:
    m.addConstr(quicksum(X[n, t] for t in T) <= G)

# --- Communication 5 ---
# Flow inbalance
constrts = {}
for p in P:
    for t in T:
        constrts[(p,t,0)] = m.addConstr(delta[p, t] >= Y[p, t] - Z[p, t])
        constrts[(p,t,1)] = m.addConstr(delta[p, t] >= - (Y[p, t] - Z[p, t]))
        #m.addConstr(delta[p, t] <= 50)
        
# Net flow delta is zero
for p in P:
    m.addConstr(quicksum(Y[p, t] for t in T) == 
                quicksum(Z[p, t] for t in T))
 

m.optimize()

print("-" * 100)

large_imbalances = []

print("Total cost = ", round(m.objval, 5))
print()

# Print total cost
print(f"| {'Total cost':<20} | {round(m.objval, 5):<20} |")
print(f"| {'':<20} | {'':<20} |")
print("-"*47)
print()
global thresh
thresh = 50
saved = 0
def printPipe(Y, Z, d, c1, c2):
    return (Y.x > 0 or Z.x > 0) and d.x > thresh

# Print gas production, inflow, outflow, and delta for each day
for t in T:
    print(f"| {'':<20} | {'':<6} |")
    print(f"| {'Day':<20} | {t+1:<6} |")
    print(f"| {'':<20} | {'':<6} |")

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
    print(f"| {'':<20} | {'':<24} |")
    print("-"*47)
    ###############
    # Flows
    print(f"| {'Pipe':<12} |",end='')
    pipe_id = 0
    for p, dist in P.items():
        coord = str(p)
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            #print(f" {coord+' ('+str(round(dist,0))+' km)':<5} |", end='')
            print(f" {str(pipe_id):<6} |", end='')
            pipe_id += 1
            if delta[(p,t)].x > thresh:
                if p not in large_imbalances:
                    large_imbalances.append(p)
    print()
    print(f"| {'Inflow (MJ)':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(Y[p,t].x, 3):<6} |", end='')
    print()    
    print(f"| {'Outflow (MJ)':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(Z[p,t].x, 3):<6} |", end='')
    print()    
    print(f"| {'Delta (MJ)':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(Y[p,t].x - Z[p,t].x, 3):<6} |", end='')
    print()    
    print()
    
    # Constrant sensitivity
    print(f"| {'DV (pi)':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,0].pi,4):<6} |", end='')
    print()
    """
    print(f"| {'Slack (MJ)':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,0].Slack,4):<6} |", end='')
    print()
    print(f"| {'SARHSLow':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,0].SARHSLow,4):<6} |", end='')
    print()
    print(f"| {'RHS':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,0].RHS,4):<6} |", end='')
    print()
    print(f"| {'SARHSUp':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,0].SARHSUp,4):<6} |", end='')
    print()

    print()
    """
    print(f"| {'DV (pi)':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,1].pi,4):<6} |", end='')
    print()
    print()
    """
    print(f"| {'Slack (MJ)':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,1].Slack,4):<6} |", end='')
    print()
    print(f"| {'SARHSLow':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,1].SARHSLow,4):<6} |", end='')
    print()
    print(f"| {'RHS':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,1].RHS,4):<6} |", end='')
    print()
    print(f"| {'SARHSUp':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,1].SARHSUp,4):<6} |", end='')
    print()
    
    print(f"| {'DV (pi)':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,1].pi,4):<6} |", end='')
    print()
    print()
    """
    print(f"| {'SARHSLow':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            if delta[p,t].x > 0:
                print(f" {round(constrts[p,t,0].SARHSLow,4):<6} |", end='')
            else:
                print(f" {round(constrts[p,t,1].SARHSLow,4):<6} |", end='')
    print()
    print(f"| {'RHS':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round(constrts[p,t,1].RHS,4):<6} |", end='')
    print()
    print(f"| {'SARHSUp':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            if delta[p,t].x < 0:
                print(f" {round(constrts[p,t,0].SARHSUp,4):<6} |", end='')
            else:
                print(f" {round(constrts[p,t,1].SARHSUp,4):<6} |", end='')
    print()
    print(f"| {'$ Save':<12} |",end='')
    for p, dist in P.items():
        if printPipe(Y[(p,t)], Z[(p,t)], delta[p,t], constrts[p,t,0], constrts[p,t,1]):
            print(f" {round((delta[p,t].x - thresh) * 0.1,4):<6} |", end='')
            saved += (delta[p,t].x - thresh) * 0.1
    print()
    print("-"*80)



print("\n")
print("#", len(large_imbalances), " pipes with large imbalances more than ", 
      thresh, " MJ: \n", large_imbalances, sep='')
print()
print("Extra costs if this limit was set on imbalances are $", round(saved, 2), sep='')
print()      
print("Done")