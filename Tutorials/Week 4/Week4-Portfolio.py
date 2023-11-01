from gurobipy import *

conNames = ["Cars Ger", "Cars Jap", "Comp USA", "Comp Sing", "App Eur", 
            "App Asia", "Ins Ger", "Ins USA", "Short Bonds", "Medium Bonds"]
"""R = {
     "Cars Ger": 10.3,
     "Cars Jap": 10.1,
     "Comp USA": 11.8,
     "Comp Sing": 11.4,
     "App Eur": 12.7,
     "App Asia": 12.2,
     "Ins Ger": 9.5,
     "Ins USA": 9.9,
     "Short Bonds": 3.6,
     "Medium Bonds": 4.2
    }
"""
R = [10.3, 10.1, 11.8, 11.4, 12.7, 12.2, 9.5, 9.9, 3.6, 4.2]

P = range(len(R))
m = Model("Portfolio")

X = {}
for i in P:
    X[i] = m.addVar()

m.setObjective(quicksum(R[p]* X[p]/100 for p in P), 
               GRB.MAXIMIZE)
    
con = {}
con["cars"] = m.addConstr(X[0] + X[1] <= 30000)
con["comp"] = m.addConstr(X[2] + X[3] <= 30000)
con["app"] = m.addConstr(X[4] + X[5] <= 20000)
con["ins"] = m.addConstr(X[6] + X[7] >= 20000)
con["bonds"] = m.addConstr(X[8] + X[9] >= 25000)
con["shmd"] = m.addConstr(X[8] >= 0.4 * X[9])
con["ger"] = m.addConstr(X[0] + X[6] <= 50000)
con["usa"] = m.addConstr(X[2] + X[7] <= 40000)
con["tot"] = m.addConstr(quicksum(X[p] for p in P) <= 100000)

    
m.optimize()

print()
print("---Return---")
for p in P:
    print(conNames[p], X[p].x)
print("\n")
    
print("---Constrant sensitivity---")
for c in con:
    print(c, conNames[p], ":", round(con[c].pi, 4), round(con[c].slack, 4),
          round(con[c].SARHSLow, 4), round(con[c].SARHSUp, 4))
    

print()    
print("---Variable sensitivity---")
for p in P:
    print(p, conNames[p], ":", round(X[p].rc, 4), round(X[p].SAObjLow, 4), round(X[p].SAObjUp, 4))
