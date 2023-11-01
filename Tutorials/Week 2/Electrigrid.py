from gurobipy import *
import pandas
import math

# Use read_csv to read the CSV data into a pandas DataFrame
nodes = pandas.read_csv("nodes.csv")
grid = pandas.read_csv("grid.csv")

N = range(len(nodes['Node']))

# To show how a DataFrame can be accessed, extract a list of node demands
demand = [nodes['Demand'][j] for j in N]

# capacity and cost for each generator node
capacity = { 3: 210, 9: 306, 12: 439 }
cost = { 3: 81, 9: 81, 12: 68 }

# E[i,j] gives the distance (km) from node i to node j
E = {}
for j in range(len(grid['Arc'])):
    n1 = grid['Node1'][j]
    n2 = grid['Node2'][j]
    distance = math.hypot(nodes['X'][n1]-nodes['X'][n2],nodes['Y'][n1]-nodes['Y'][n2])
    E[n1,n2] = distance
    # create an edge in both directions
    #E[n2,n1] = distance


m = Model("Electrigrid")
h = 24

# Variables
X = {}
for e in E:
    X[e] = m.addVar()

Y = {}
for n in N:
    Y[n] = m.addVar()


# Objective

m.setObjective(quicksum(h * cost[n] * Y[n] for n in N if n in cost), GRB.MINIMIZE)

# Flow balance constraint
for n in N:
    m.addConstr(Y[n] + quicksum((1-0.001*E[e]) * X[e] for e in E if e[1] == n) == 
                demand[n] + quicksum(X[e] for e in E if e[0] == n))
    
# Generator capacity
for n in N:
    if n not in capacity:
        m.addConstr(Y[n] <= 0)
    else:
        m.addConstr(Y[n] <= capacity[n])

m.optimize()

print("Total cost = ", m.objval)
for n in N:
    if Y[n].x > 0:
        print("Generator", n, "=", round(Y[n].x, 3))
print()
for e in E:
    if X[e].x > 0:
        print("Flow", e, "=", round(X[e].x, 3))

print()
import os
print("PythonPATH",os.environ.get('PYTHONPATH'))
        
        
print("Done")