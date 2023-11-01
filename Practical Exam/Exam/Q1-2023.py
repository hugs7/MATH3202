"""
Hugo Burton

q1

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

m = Model("Q1")

# Variables
# number of trucks t in lane l on first ferry
X = { (t,l): m.addVar(vtype=GRB.INTEGER) for t in T for l in L }


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



m.optimize()

print()
print("Objective Value: ", m.objVal)

print("Lanes")
for l in L:
    print()
    print("Lane", l)
    for t in T:
        print(int(X[t,l].x), " trucks of type", Trucks[t], "in lane")