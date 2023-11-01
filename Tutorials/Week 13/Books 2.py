# -*- coding: utf-8 -*-
"""
Spyder Editor

Practice exam 2 b
"""

# Hugo (me)
demand = [14, 8, 17, 22, 12, 6]
r = 12
b = 50 # for 10 books
sell_prof = 1
stor = 0.5

# create a dictionary to store results of previous function calls
memo = {}

def V(t, s, announc):
    # check if we have already computed the value for this t and s
    if (t, s) in memo:
        return memo[(t, s)]
    
    # otherwise, compute the value as usual
    # print(s)
    if s < 0:
        return 0, 0, 0
    if t == 6:
        # max_branch = max([(r * sell, 0) for sell in range(demand[t]+1)])
        max_branch = s, s, 0
    else:
        branches = []
        for buy in range(2 * demand[t]):
            prof1 = (r * min(demand[t], s+10*buy) - buy * b - stor * s + V(t + 1, s - min(demand[t], s+10*buy) + 10 * buy, 1)[0])
            prof2 = (r * min(2*demand[t], s+10*buy) - buy * b - stor * s + V(t + 1, s - min(2*demand[t], s+10*buy) + 10 * buy, 1)[0])
            if announc == 1:
                branches.append((prof2, s - min(demand[t], s+10*buy), buy))
            else:
                branches.append((0.7*prof1 + 0.3*prof2,
                0.7*(s - min(demand[t], s+10*buy))+0.7*(s - min(2*demand[t], s+10*buy)), 
                buy))
        max_branch = max(branches)
        
    # store the result in the dictionary for future use
    memo[(t, s)] = max_branch
        
    return max_branch
    
# print(V(0,0))
t = 0
s = 0
while True:
    #print(t,s)
    prof, s, buy = V(t, s, 0)
    # print("t, ": $", prof," | Store: ",s, " | Buy: ", buy, " | Sell: ", sell, sep='')
    print(f"t: {t:<2} | Prof: ${prof:>6} | Store: {s:<3} | Buy: {buy:>3} |")

    t += 1
    if t == 6:
        break
    