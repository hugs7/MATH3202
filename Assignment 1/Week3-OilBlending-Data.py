from gurobipy import *

# Sets
Oils = ["Veg 1", "Veg 2", "Oil 1", "Oil 2", "Oil 3"]
O = range(len(Oils))
V = [i for i in O if Oils[i][0]=='V']
N = [i for i in O if Oils[i][0]!='V']
Months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
T = range(len(Months))

# Data
h = [8.8, 6.1, 2.0, 4.2, 5.0]
c = [[110, 130, 110, 120, 100,  90], 
     [120, 130, 140, 110, 120, 100],
     [130, 110, 130, 120, 150, 140], 
     [110,  90, 100, 120, 110,  80], 
     [115, 115,  95, 125, 105, 135]]
MaxV = 200
MaxN = 250
Sell = 150
MinH = 3
MaxH = 6
MaxStore = 1000
CStore = 5
Initial = 500


# Model
m = Model("Oil blending")

E = 0.01 # $ / MJ / h

# Variables
X = {}
Y = {}
S = {}
for i in O:
    for t in T:
        X[i,t] = m.addVar()
        Y[i,t] = m.addVar()
        S[i,t] = m.addVar()


# Objective
m.setObjective(quicksum(Sell * X[i,t] - c[i][t] * Y[i,t] 
                                  - CStore * S[i,t] for i in O
                                 for t in T), GRB.MAXIMIZE)


# Constraints

for t in T:
    m.addConstr(quicksum(X[i,t] for i in V) <= MaxV)
    m.addConstr(quicksum(X[i,t] for i in N) <= MaxN)
    
    m.addConstr(quicksum((MinH - h[i]) * X[i,t] for i in O) <= 0)
    m.addConstr(quicksum((h[i] - MaxH) * X[i,t] for i in O) <= 0)
    for i in O:
        m.addConstr(S[i,t] <= MaxStore)
        if t == 0:
            m.addConstr(S[i,t] == Initial + Y[i,t] - X[i,t])
        else:
            m.addConstr(S[i,t] == S[i,t - 1] + Y[i,t] - X[i,t])

# Storage left over
for i in O:
    m.addConstr(S[i,T[-1]] >= Initial)

m.optimize()

print()
# Solution
print("Objective is", m.objVal)
for t in T:
    print("Month:", Months[t])
    print("Hardnesss", sum(h[i]*X[i,t].x for i in O)/sum(X[i,t].x for i in O)) 
    for i in O:
        print(Oils[i], X[i,t].x)
    
    print()
    

print("Refined")
for t in T:
    print([round(X[i,t].x,2) for i in O])

print()
print("Purchased")
for t in T:
    print([round(Y[i,t].x,2) for i in O])

print()
print("Storage")
for t in T:
    print([round(S[i,t].x,2) for i in O])

        
print("Done")