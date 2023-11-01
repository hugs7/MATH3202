from gurobipy import *
import pandas
import math

# ******Data******
# read the CSV data into a pandas DataFrame
nodes = pandas.read_csv("nodes3.csv")
grid = pandas.read_csv("pipelines.csv")

#Create data frame for number of days (fortnight) 
Fortnight = ["Year5", "Year10"]

#Length of number of days in Fortnight
T = range(len(Fortnight))

#Number of nodes 
N = range(len(nodes['Node']))

Upgrades  = { "No Upgrade", "Upgrade 1", "Upgrade 2", "Upgrade 3"}

U = range(len(Upgrades))

#Extracting data frame for demand over fortnight then transforming into list form 
demand = nodes.iloc[:,3:5]
demand.T
demand = demand.values.tolist()

# Capacity and cost for each generator node
# capacity = { 37: 360, 41: 726, 42: 749, 49: 556}
# cost = { 37: 83, 41: 82, 42: 66, 49: 68}

#Capacity Upgrade [n][u]
C = {37: [360, 429, 536, 719],
     41: [726, 871, 1094, 1454], 
     42: [749, 896, 1124, 1492], 
     49: [ 556, 666, 835, 1108]}

#Cost Upgrade [n][u]
M = {37: [0, 7071000, 18062000, 33468000], 
     41: [0, 14481000, 36704000, 66513000],
     42: [0, 14777000, 36298000, 66218000],  
     49: [0, 11406000, 26611000,  50037000]}

# P[i,j] gives the distance (km) of pipelines from node i to node j
P = {}
for j in range(len(grid['Pipeline'])):
    n1 = grid['Node1'][j]
    n2 = grid['Node2'][j]
    distance = math.hypot(nodes['X'][n1]-nodes['X'][n2],
                          nodes['Y'][n1]-nodes['Y'][n2])
    P[n1,n2] = distance

# ****** Assigning model name ******

m = Model("Pacific Paradise Gas")

# ****** Variables ******

#Amount of Gas flowing at each pipeline each day 
X = {(p,t): m.addVar() for p in P for t in T}
#Amount of Gas generated at each node for each day
Y = {(n,t): m.addVar() for n in N for t in T}
#Upgrade of Capacity at ech node for each year 
Z = {(n,u): m.addVar(vtype=GRB.BINARY)  for n in N for u in U}


# ******Objective******
m.setObjective(quicksum(M[n][u] * Z[(n, u)] for n in N if n in M.keys() for u in U), GRB.MINIMIZE)
# ******Constraints******

# 1. Generator capacity
     
for n in N:
    for t in T:
        if n in C:
            m.addConstr(Y[n,t] <= C[n][0] + quicksum(Z[n,u]*C[n][u] for u in U if u != 0))
        else:
            m.addConstr((Y[n,t] <= 0))

# 2. Flow Balance constraint
# Ensure that the imbalance is considered when meeting the demand for the day
for n in N:
    # for t in T:
    t = 1
    m.addConstr(Y[n,t] + quicksum(X[p,t] for p in P if p[1] == n) == 
          demand[n][t] + quicksum(X[p,t] for p in P if p[0] == n))


#Upgrade Constrants 

for n in N:
    if n in M.keys():
        m.addConstr(quicksum(Z[n,u] for u in U) == 1)
    else:
        m.addConstr(quicksum(Z[n,u] for u in U) == 0)
        





# 7. Non-Negativity Constraints (Don't need to specify these in Gurobi)
# for t in T:
#     for p in P:
#         m.addConstr(X[p,t] >= 0)
# for t in T:
#     for n in N:
#         m.addConstr(Y[n,t] >= 0)
# for u in U:
#    for n in N:
       
#         m.addConstr(quicksum( Z[n,u]) >= 0)


#Optimise model
m.optimize()

print("Total cost =", m.objval)

# Amount of Gas generated at each node for each day
for n in N:
    for t in T:
        if Y[n, t].x > 0:
            print("Generator",n,"=",Y[n, t].x);