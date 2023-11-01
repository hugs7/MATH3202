# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 18:14:51 2023

@author: Hugo Burton
"""

# Data

N = range(10)
depot = 0
demand = [0, 3, 1, 2, 1, 2, 2, 2, 3, 2]

# dist[i][j] gives the travel time (mins) between i and j
dist = [
	[0, 30, 50, 120, 140, 180, 120, 210, 160, 100],
	[30, 0, 50, 100, 110, 160, 120, 190, 140, 70],
	[50, 50, 0, 70, 100, 130, 70, 160, 110, 60],
	[120, 100, 70, 0, 60, 60, 60, 90, 40, 30],
	[140, 110, 100, 60, 0, 120, 120, 150, 100, 40],
	[180, 160, 130, 60, 120, 0, 100, 30, 50, 90],
	[120, 120, 70, 60, 120, 100, 0, 130, 50, 90],
	[210, 190, 160, 90, 150, 30, 130, 0, 80, 120],
	[160, 140, 110, 40, 100, 50, 50, 80, 0, 70],
	[100, 70, 60, 30, 40, 90, 90, 120, 70, 0]
]

maxTime = 6 * 60


"""
Value function
Takes current customer (integer between 0 and 9), cumulative time so far on the trip and list of visited customers
Returns number of cylinders to deliver at current customer plus future value
"""
def V(currentCustomer, cumTime, visited):
    # Base case
    
    # if we have exceeded the time limit, there is no futher value: return massive negative value
    if cumTime >= maxTime:
        return -100000,cumTime, visited
    
    
    branches = []
    # Loop over possible next actions
    for a in N:
        # Exclude customers we have already visited
        if a not in visited:
            # Value of choosing to visit customer a next is demand at current customer plus value of going to customer a next
            branches.append((demand[currentCustomer] + V(a, cumTime + dist[currentCustomer][a], visited + [a])[0], cumTime + dist[currentCustomer][a], visited + [a]))
        elif a == depot:
            # Include going back to the depot at every stage so we always have the option of returning home
            branches.append((demand[currentCustomer], cumTime+dist[currentCustomer][a], visited+[a]))

    return max(branches)


# Setup variables
vi = []
vi += [depot]
time = 0
val = 0

# print("Can deliver", V(depot, 0, vi)[0], "Cylinders")

# While loop to step through each customer
while True:
    val, time, vi = V(depot, time, vi)
    if len(vi) >= 1 and vi[-1] == 0:
        break

# Sum up demand for customers visited
s = 0
for l in vi:
    s += demand[l]
    
# Print results
print("Delivered ", s, " cylinders")

print("Customers visited", vi, "(including depot at both ends), taking", time, "minutes")





