# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:34:35 2023

@author: Hugo Burton
"""

# Data

actions = {"Sing", "Forage", "Rest"}
p_sing = 0.004
p_food = 0.6
r = 3.6
E = 32
s_0 = 10

def f_sing(s):
    return 12 + 0.002 * s

def f_forage(s):
    return 8 + 0.007 * s

def V_d(t,x,m):
    s = int(x)
    p = x-s
    return p * V_old(t,s+1,m)[0] + (1-p) * V_old(t,s,m)[0]
    

def V(t,s,m):
    return 0.25 * V_d(t,s-6.4,m) + 0.5 * V_d(t,s,m) + 0.25 * V_d(t,s+6.4,m)

cache = {}
def V_old(t,s,m):
    if s <= 0:
        return 0, 'Dead', s
    if t == 150:
        if s > 0:
            if m == 1:
                return 2, 'Mate', s
            else:
                return 1, 'Lonely', s
        else:
            return 0, 'Dead', s
    
    if (t,s,m) not in cache:
        cases = []
        cases.append((V(t+1,s-r,m),'Rest', s-r))
        if t < 75:
            cases.append((p_sing * V(t+1,s-f_sing(s),1) + (1-p_sing) * V(t+1,s-f_sing(s),m), 'Sing', s-f_sing(s)))
            cases.append((p_food * V(t+1,s-f_forage(s)+E,m) + (1-p_food) * V(t+1,s-f_forage(s),m), 'Forage', p_food*(s-f_forage(s)+E) + (1-p_food)*(s-f_forage(s))))
        
        max_cases = max(cases)
        cache[t,s,m] = max_cases
        return max_cases
    
    return cache[t,s,m]


t = 0
m = 0
s = s_0
while True:
    v, a, s_new = V_old(t,s,m)
    # print(s_new)
    print(f"| {round(s):<5} | {a:<10} |")
    t += 1
    s = s_new
    if t == 150:
        break
    
# print(V_old(0,s_0,0))
