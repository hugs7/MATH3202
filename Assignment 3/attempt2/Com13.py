#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 16:07:57 2023

"""
Demand = {1: 15,
          2: 10,
          3: 9,
          4: 8,
          5: 15,
          6: 10,
          7: 14,
          8: 11,
          9: 11,
          10: 11,
          11: 7,
          12: 6,
          13: 11,
          14: 8}

DemandHigh = {1: 20,
          2: 18,
          3: 15,
          4: 14,
          5: 23,
          6: 16,
          7: 19,
          8: 15,
          9: 15,
          10: 14,
          11: 10,
          12: 15,
          13: 20,
          14: 13}

Required = {1: 3,
          2: 3,
          3: 4,
          4: 5,
          5: 2,
          6: 2,
          7: 4,
          8: 3,
          9: 4,
          10: 5,
          11: 4,
          12: 5,
          13: 3,
          14: 3}

price = 120
MaxStorage = 30 
CylinderCost = 50 
DeliveryCost = 300
LargeCylinderPrice = 230
LargeDeliveryCost = 80
LargeMaxStorage = 2

ProbNormal = 0.6 # Probability of normal demand
ProbHigh = 0.4 # Probability of high demand

# Stages 
T = range(len(Demand))

# State 

# Cost Function
cost_ = {}

def cost(a_sell, b_sell, a_buy, b_buy):
    if a_buy + b_buy == 0:
        return 0
    else:
        return price * a_sell + LargeCylinderPrice * b_sell - DeliveryCost - CylinderCost * a_buy - LargeCylinderCost * b_buy


def cost(a,b):
    if a == 0 and b == 0:
        return 0 
    else:
        cost_[a,b] = DeliveryCost + CylinderCost*a + LargeDeliveryCost*b
    return cost_[a,b]


profit_ = {}
totalprofit_ = {}

def V(t,s1,s2):
    if t == 15:
        return (0, 'Done')
    
    if (t,s1,s2) not in totalprofit_:
        totalprofit_[t,s1,s2] = max((ProbNormal*(price*min(s1+a, Demand[t]) - cost(a,b) 
                                                  + V(t+1, s1+a-min(s1+a,Demand[t]), s2+b-Required[t])[0]) +
                                 ProbHigh*(price*min(s1+a, DemandHigh[t]) - cost(a,b) 
                                           + V(t+1, s1+a-min(s1+a,DemandHigh[t]),s2+b-Required[t])[0]) +
                                 (LargeCylinderPrice*Required[t] - cost(a,b) + V(t+1,s1+a-min(s1+a,Demand[t]),s2+b-Required[t])[0]),a+b)
                                    for a in range(0,24) for b in range(0,6))
        
        branches = []
        for buy in range(MaxStorage - s1 + max(Demand.values()) + 1):
            for buy2 in range(LargeMaxStorage - s2 + DemandHigh[t] + 1):
                for sell in range(min(DemandHigh[t], s1 + buy) + 1):
                    if 45 * buy + 90 * buy2 <= 1000 and buy <= MaxStorage - s1 + min(sell, Demand[t]) and Required[t] <= s2 + buy2: 
                        branches.append((
                            ProbHigh * (cost(sell, Required[t], buy, buy2) + V(t + 1, s1 - sell + buy, s2 - b_demand[t] + buy2)[0])
                            +ProbNormal * (cost(min(sell,demand[t]), Required[t], buy, buy2) + 
                                        V(t + 1, s1 - min(sell, demand[t]) + buy, s2 - b_demand[t] + buy2)[0])
                            
                            int(expectation(ProbHigh, s1 - sell + buy, s - min(sell,demand[t]) + buy)),   # Store 1
                            s2 - Required[t] + buy2,                                                # Store 2
                            buy,                                                                    # Buy
                            buy2,                                                                   # Buy 2
                            int(expectation(ProbHigh, sell, min(sell,demand[t]))))                       # Sell
                        )
        
        max_branch = max(branches)
    return totalprofit_[t,s1,s2]



print(V(1,0,0))