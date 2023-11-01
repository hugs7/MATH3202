# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 16:14:31 2023

@author: Hugo Burton
"""

# Data
p_init = 0.6
v = [[3,0],[5,1]]
acts = ["Cooperate", "Defect"]
COOP = 0
DEF = 1

def V(r,p):
    if r == 11:
        return 0,0,0
    
    return max((p * v[COOP][COOP] + (1-p)*v[COOP][DEF] + V(r+1,min(1,p+0.1))[0], COOP, min(1,p+0.1)),
               (p * v[DEF][COOP] + (1-p)*v[DEF][DEF] + V(r+1,max(0,p-0.2))[0], DEF, max(0,p-0.2)))


p = p_init
for r in range(11):
    val, act, p = V(r,p)
    print(f"| Round: {r:<2} | {round(val,2):<5} | {acts[act]:<15} | {round(p,2):<5} |")
    

