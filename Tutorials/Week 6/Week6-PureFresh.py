from gurobipy import *
import numpy as np
# Sets
Quarters = ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8"]
Juices = ["Orange","Orange and Mango", "Breakfast", "Tropical", "Guava Delight", "Orchard Medley", "Strawberry Surpise" ]
Fruits = ["Orange","Apple","Mango", "Pineapple", "Passionfruit", "Guava", "Strawberry"]
Gourmet = Juices[-3:]

T = range(len(Quarters))
J = range(len(Juices))
F = range(len(Fruits))
G = range(len(Juices) - 3, len(Juices))



# Data

# Maximum demand (kL) [Q][J]
Demand = [
        [538,174,370,243,244,1098,662],
        [895,373,780,531,479,622,744],
        [1412,538,1096,846,576,652,541],
        [1102,407,900,624,309,860,432],
        [576,229,447,376,246,1168,543],
        [1005,409,924,622,420,640,720],
        [1330,569,1146,833,497,585,516],
        [1160,400,793,679,306,870,478]
         ]
Demand = np.array(Demand).T.tolist()
# Cost of fruit ($/kL) [F]
Cost = [946,620,1300,800,1500,710,1370]

# Quantity of fruit needed for juice [J][F]
Blend = [
     [1,0,0,0,0,0,0],
     [0.9,0,0.1,0,0,0,0],
     [0.15,0.55,0.02,0.28,0,0,0],
     [0.04,0.65,0,0.3,0.01,0,0],
     [0,0.8,0,0.1,0,0.1,0],
     [0.45,0.5,0.05,0,0,0,0],
     [0,0.9,0,0,0,0.02,0.08]
      ]
      
# Orange juice availability (kL) [Q]
FCOJ = [1000,2000,2600,2500,1300,2200,2650,2300]

# Selling price ($/kL)
Price = 1500


m = Model("Fresh Juice")


X = {(j,t): m.addVar() for j in J for t in T}
Y = {(f,t): m.addVar(vtype=GRB.INTEGER) for f in F for t in T}
Z = {(j,t): m.addVar(vtype=GRB.BINARY) for j in J for t in T}

# m.setObjective(quicksum(Price*X[j,t] - quicksum(Cost[f]*Blend[j][f]*X[j,t] for f in F) 
                        # for j in J for t in T), GRB.MAXIMIZE)
m.setObjective(quicksum(quicksum(Price*X[j,t] 
                        - quicksum(Cost[f]*Blend[j][f]*X[j,t] for f in F if f == 0) for j in J)
                        - quicksum(Cost[f]*10*Y[f,t] for f in F if f != 0) 
                        for t in T), GRB.MAXIMIZE)

for t in T:
    m.addConstr(quicksum(Blend[j][0]*X[j,t] for j in J) <= FCOJ[t])
    for j in J:
        m.addConstr(X[j,t] <= Demand[j][t])
    for g in G:
        m.addConstr(X[g,t] <= Demand[g][t] * Z[g,t])
        
    for f in F:
        if f != 0:    
            m.addConstr(quicksum(Blend[j][f]*X[j,t] for j in J) <= 10 * Y[f,t])
    
    m.addConstr(quicksum(Z[g,t] for g in G) <= 2)

for g in G:
    m.addConstr(quicksum(Z[g,t] for t in T) >= 3)

m.optimize()

print("Maximum profit: $", m.objval)

print("Sales")
t = 1
print(f"| {'':<20} |")
print(f"| {'Juice produced':20} |")
# Print gas production for each node
print(f"| {'Quarter / Juice':<15} |",end='')
for j in Juices:
    print(f" {j[:6]:<8} |",end='')
print()

for q, t in enumerate(T):
    print(f"| {Quarters[q]:<15} |",end='')
    for j in J:
        print(f" {int(X[j,t].x):<8} |", end='')
    print()
print()



print(f"| {'Trucks':<20} |")
print(f"| {'Quarter / Fruit':<15} |",end='')
for f in Fruits:
    print(f" {f[:6]:<8} |",end='')
print()

for q, t in enumerate(T):
    print(f"| {Quarters[q]:<15} |",end='')
    for f in F:
        print(f" {int(Y[f,t].x):<8} |", end='')
    print()
print()

print(f"| {'FCOJ':<20} |")
for t in T:
    print(f"| {FCOJ[t]:<10} |",end='')
    print(f" {round(sum(Blend[j][0]*X[j,t].x for j in J), 2):<7} |", end='')
    print()
print()

print(f"| {'':<20} | {'':<24} |")







