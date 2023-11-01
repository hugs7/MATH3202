# 2022 Q1

from gurobipy import *
	
Factories = ["A","B","C"]
Months = ["Jul","Aug","Sep","Oct","Nov","Dec"]
Grains = ["Wheat","Corn"]

F = range(len(Factories))
T = range(len(Months))
G = range(len(Grains))

Capacity = 4000
StoreCost = 1.5
Starting = [600,300]

# Demand[f][t][g]
Demand = [[[565, 290], [695, 285], [385, 315], [500, 245], [785, 270], [540, 275]], [[1050, 300], [585, 325], [510, 205], [1050, 270], [810, 210], [545, 285]], [[720, 315], [545, 465], [520, 315], [475, 465], [415, 480], [985, 525]]]

# Cost[t][g]
Cost = [[95, 43], [97, 50], [89, 76], [65, 70], [82, 49], [79, 48]]

m = Model("Factories Q1")

# Purchase
X = { (f,t,g): m.addVar(vtype=GRB.INTEGER) for f in F for t in T for g in G }

# Inventory
Y = { (f,t,g): m.addVar(vtype=GRB.INTEGER) for f in F for t in T for g in G }


m.setObjective(quicksum((quicksum(StoreCost * Y[f,t,g] + Cost[t][g] * X[f,t,g] 
                                  for f in F for g in G)) for t in T), GRB.MINIMIZE)

# Constraints

for f in F:
    for g in G:
        m.addConstr(Y[f,0,g] == Starting[g])
        m.addConstr(Y[f,5,g] == Starting[g])

for t in T:
    m.addConstr(quicksum(X[f,t,g] for f in F for g in G) <= Capacity)
    
    for f in F:
        for g in G:
            if t > 0:
                # m.addConstr(Y[f,t,g] + X[f,t,g] >= Demand[f][t][g])
            
                m.addConstr(Y[f,t,g] == Y[f,t-1,g] + X[f,t,g] - Demand[f][t][g])
                m.addConstr(Y[f,t,g] >= 0)
                
            else:
                # t == 0. First month
                m.addConstr(Y[f,t,g] + X[f,t,g] >= Demand[f][t][g])
            
    

m.optimize()

print("Objective value", m.objVal)

for t in T:
    print("\nMonth", t)
    for f in F:
        print("factory", f)
        for g in G:
            print(f"| {round(X[f,t,g].x,2):<10} | {round(Y[f,t,g].x,2):<10} | {Demand[f][t][g]:<5} |")
            
            