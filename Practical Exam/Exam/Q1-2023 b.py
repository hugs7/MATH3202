

"""
Hugo Burton

q1 b

"""



from gurobipy import *

# Data

# Lanes
L = range(5)
LaneLength = [40,40,40,40,35]

# Truck types
Trucks = ["Van","Small Truck","Medium Truck","Large Truck"]
T = range(len(Trucks))
Value = [450, 600, 1000, 1800]
Length = [4.5, 7, 10, 15] # metres
Mass = [1.5, 2.5, 5, 9] # tonnes
Total = [6, 8, 7, 9] # maximum number of truck type to load

MaxWeight = 120 # Tonnes (capacity of ferry)


# Model

m = Model("Q1b")

# Variables
# number of trucks t in lane l on first ferry
X = { (t,l): m.addVar(vtype=GRB.INTEGER) for t in T for l in L }

# New variable for balance
Y = { (p): m.addVar(vtype=GRB.SEMICONT) for p in [0,1] }

# Objective Function

m.setObjective(quicksum(X[t,l] * Value[t] for t in T for l in L), GRB.MAXIMIZE)


# Constraints
# Number of trucks

for t in T:
    # For each truck type, number of trucks across all lanes must be less than total
    m.addConstr(quicksum(X[t,l] for l in L) <= Total[t])

# Lane Length
for l in L:
    # Sum of trucks in lane must be less than the length of the lane
    m.addConstr(quicksum(X[t,l]*Length[t] for t in T) <= LaneLength[l])
    
# Mass
# Sum mass of trucks in all lanes must be less than 120 tonnes
m.addConstr(quicksum(X[t,l] * Mass[t] for t in T for l in L) <= MaxWeight)


# Balance constraint
p = 0 # Left side (lanes 0 and 1)
m.addConstr(Y[p] == 2 * quicksum(X[t,0]*Mass[t] for t in T) + quicksum(X[t,1]*Mass[t] for t in T))

p = 1 # Right side (lanes 3 and 4)
m.addConstr(Y[p] == quicksum(X[t,3]*Mass[t] for t in T) + 2 * quicksum(X[t,4]*Mass[t] for t in T))

# 5% tolerance using semicontinuous variables
m.addConstr(Y[0] <= Y[1] * 1.05)
m.addConstr(Y[1] <= Y[0] * 1.05)

m.optimize()

print()
print("Objective Value: ", m.objVal)

print("Lanes")
for l in L:
    print()
    print("Lane", l)
    for t in T:
        print(int(X[t,l].x), " trucks of type", Trucks[t], "in lane")
        
        
print("Weight on left side")
print(round(Y[0].x,2))

print("Weight on Right side")
print(round(Y[1].x,2))

