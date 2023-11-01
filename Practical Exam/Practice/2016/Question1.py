from gurobipy import *
import random

# Data and ranges
nHospitalSites = 30
nSuburbs = 55
MaxSuburbsPerHospital = 7
MaxPopulation = 500000

H = range(nHospitalSites)
S = range(nSuburbs)
L = H
random.seed(3)

FixedCost = [random.randint(5000000,10000000) for h in H]
Population = [random.randint(60000,90000) for s in S]

# Travel distance - multiply by population moved to get travel cost
Dist = [[random.randint(0,50) for s in S] for h in H]

# Set up model and set the gap on the answer to 0
m = Model()

X = { (l): m.addVar(vtype=GRB.BINARY) for l in L }
Y = { (s,l): m.addVar(vtype=GRB.BINARY) for s in S for l in L }

m.setObjective(quicksum(FixedCost[l]*X[l] + quicksum(Population[s]*Dist[l][s]*Y[s,l] for s in S) for l in L), GRB.MINIMIZE)

# Constraints

for l in L:
    for s in S:
        m.addConstr(Y[s,l] <= X[l])

for s in S:
    m.addConstr(quicksum(Y[s,l] for l in L) == 1)
    
for l in L:
    m.addConstr(quicksum(Y[s,l] for s in S) <= MaxSuburbsPerHospital)
    m.addConstr(quicksum(Y[s,l] * Population[s] for s in S) <= MaxPopulation)


m.setParam('MIPGap', 0)

m.optimize()
print("\n")

print("Objective value =", m.objVal)


print("Build Hospitals")
for l in L:
    if X[l].x > 0.9:
        print("Hospital:",l, "at a cost of $" + str(FixedCost[l]))
        
print()
print("Suburbs for hospital")
for l in L:
    if X[l].x < 0.5:
        continue
    for s in S:
        if Y[s,l].x > 0.9:
            print("Suburb", s, "assigned to hospital", l, "at a cost of", round(Dist[l][s]*Population[s],2))
    print()
            
        