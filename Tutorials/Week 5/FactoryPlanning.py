from gurobipy import *

# Data
profit = [10, 6, 8, 4, 11, 9, 3]
P = range(len(profit))

Machines = ["Grinding","VDrilling","HDrilling","Boring","Planing"]
n = [4, 2, 3, 1, 1]
M = range(len(n))

# usage[P][M]
usage = [
    [0.5, 0.1, 0.2, 0.05, 0.00],
    [0.7, 0.2, 0.0, 0.03, 0.00],
    [0.0, 0.0, 0.8, 0.00, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.00],
    [0.3, 0.0, 0.0, 0.10, 0.05],
    [0.2, 0.6, 0.0, 0.00, 0.00],
    [0.5, 0.0, 0.6, 0.08, 0.05]
    ]

# months
T = range(6)

# maintenance[T][M]
maint = [
    [1, 0, 0, 0, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 1]
    ]

# market[P][T]
market = [
    [ 500, 600, 300, 200,   0, 500],
    [1000, 500, 600, 300, 100, 500],
    [ 300, 200,   0, 400, 500, 100],
    [ 300,   0,   0, 500, 100, 300],
    [ 800, 400, 500, 200,1000,1100],
    [ 200, 300, 400,   0, 300, 500],
    [ 100, 150, 100, 100,   0,  60]
    ]

maxstore = 100
storecost = 0.5
endstore = 50
monthhours = 16*24


m = Model("Factory Planning")

X = {}
Y = {}
S = {}
Z = {}
for t in T:
    for p in P:
        X[p,t] = m.addVar()
        Y[p,t] = m.addVar()
        S[p,t] = m.addVar()
    for mach in M:
        Z[mach,t] = m.addVar(vtype=GRB.INTEGER)


# Objective
m.setObjective(quicksum(profit[p] * Y[p,t] for p in P for t in T) - 
               quicksum(storecost * S[p,t] for p in P for t in T),
               GRB.MAXIMIZE)



# Consraints
for t in T:
    for mach in M:
        m.addConstr(quicksum(usage[p][mach] * X[p,t] for p in P) <= 
                    monthhours * (n[mach] - Z[mach,t]))
    
    for p in P:
        m.addConstr(Y[p,t] <= market[p][t])
        if t == 6 - 1:
            m.addConstr(S[p,t] >= endstore)
            
        if t > 0:
            m.addConstr(S[p,t] == S[p,t-1] + X[p,t] - Y[p,t])
        else:
            m.addConstr(S[p,t] <= X[p,1-1] - Y[p, 1-1])
        m.addConstr(S[p,t] <= maxstore)
        
        
        # m.addConstr(X[p,t] >= 0)
        # m.addConstr(Y[p,t] >= 0)
        # m.addConstr(S[p,t] >= 0)
    

for mach in M:
    m.addConstr(quicksum(Z[mach,t] for t in T) == sum(maint[t][mach] for t in T))

for t in T:
    m.addConstr(quicksum(Z[mach, t] for mach in M) <= 2)
    m.addConstr(quicksum(Z[mach, t] for mach in M) >= 1)

m.optimize()

print("-" * 50)

print("Objective:", m.objval)

    

print("Production")
print(f"| {'Month #':<10} |", end='')
for t in T:
    print(f" {t+1:<10} |", end='')
print()
for p in P:
    print(f"| {'Product '+str(p):<10} |", end='')
    for t in T:
        print(f" {round(X[p,t].x,2):<10} |",end='')
    print()
print()
print("Sold")
print(f"| {'Month #':<10} |", end='')
for t in T:
    print(f" {t+1:<10} |", end='')
print()
for p in P:
    print(f"| {'Product '+str(p):<10} |", end='')
    for t in T:
        print(f" {round(Y[p,t].x,2):<10} |",end='')
    print()

print()
print("Storage")
print(f"| {'Month #':<10} |", end='')
for t in T:
    print(f" {t+1:<10} |", end='')
print()
for p in P:
    print(f"| {'Product '+str(p):<10} |", end='')
    for t in T:
        print(f" {round(S[p,t].x,2):<10} |",end='')
    print()
print()
print("Maintenance")
print(f"| {'Month #':<18} |", end='')
for t in T:
    print(f" {t+1:<4} |", end='')
print()
for mach in M:
    print(f"| {'Machine '+Machines[mach]:<18} |", end='')
    for t in T:
        print(f" {int(Z[mach,t].x):<4} |",end='')
    print()