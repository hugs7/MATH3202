






from gurobipy import *
import random

# 100 candidate sites
S = range(100)
random.seed(20)

# Drill cost at each site
DrillCost = [random.randint(15000,60000) for s in S]

# 30 groups with between 5 and 10 elements in every group
Group = [sorted(random.sample(S, random.randint(5,10))) for i in range(30)]

G = range(len(Group))


m = Model("Wells")

# Variables

X = { s: m.addVar(vtype=GRB.BINARY) for s in S }
Y = { g: m.addVar(vtype=GRB.BINARY) for g in G }

# Objective

m.setObjective(quicksum(X[s]*DrillCost[s] for s in S) + 10000 * quicksum(Y[g] for g in G), GRB.MINIMIZE)

# Constraints

# must be 20 wells built
m.addConstr(quicksum(X[s] for s in S) == 20)

# for g in G:
#     # cannot build more than two wells from each group
#     m.addConstr(quicksum(X[s] for s in Group[g]) <= 2)
    
#     # linking X and Y. Penalty must be paid if two wells are chosen from 1 group
#     m.addConstr(quicksum(X[s] for s in Group[g]) - 1 <= Y[g])
    

for g in G:
    m.addConstr(quicksum(X[s] for s in Group[g]) <= 1 + Y[g])
    
m.optimize()

print("\nObjective value:", m.objVal)

#414746

print("Wells")
for s in S:
    if X[s].x > 0.9:
        print("Build", s)
        
print(sum(X[s].x for s in S), "Wells built")

print("Groups")
print("Penalty = $", sum(Y[g].x for g in G)*10000)

print()
# for i,g in enumerate(Group):
#     for s in S:
#         if s in g and X[s].x > 0.9:
#             print("Well", s, "built and from group", i)
#     print()