from gurobipy import *

P = {
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

m = Model("Portfolio")

X = { p: m.addVar() for p in P }

m.setObjective(quicksum(P[p]*X[p]/100 for p in P),GRB.MAXIMIZE)

C = {}
C["Tot"] = m.addConstr(quicksum(X[p] for p in P) == 100000)
C["Cars"] = m.addConstr(quicksum(X[p] for p in P if 'Cars' in p)<=30000)
C["Comp"] = m.addConstr(quicksum(X[p] for p in P if 'Comp' in p)<=30000)
C["App"] = m.addConstr(quicksum(X[p] for p in P if 'App' in p)<=20000)
C["Ins"] = m.addConstr(quicksum(X[p] for p in P if 'Ins' in p)>=20000)
C["Bonds"] = m.addConstr(quicksum(X[p] for p in P if 'Bonds' in p)>=25000)
C["Short/Med"] = m.addConstr(X["Short Bonds"]>=0.4*X["Medium Bonds"])
C["Ger"] = m.addConstr(quicksum(X[p] for p in P if 'Ger' in p)<=50000)
C["USA"] = m.addConstr(quicksum(X[p] for p in P if 'USA' in p)<=40000)

m.optimize()

print("Earnings =", m.objVal)
print('Average earnings', m.objVal/1000)
print("### Portfolio ###")
for p in P:
    print(p,X[p].x)
print()
print("### Duals and constraint sensitivity ###")
for k in C:
    print(k, round(C[k].pi,4), round(C[k].Slack,4), 
          round(C[k].SARHSLow,4), round(C[k].RHS,4), round(C[k].SARHSUp,4))
print()
print("### Variable sensitivity #####")
for p in P:
    print(p, round(X[p].rc,4), round(X[p].SAObjLow,4), 
          round(X[p].obj,4), round(X[p].SAObjUp,4))
    
