# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Hugo (me)
demand = [14, 13, 10, 14, 13, 6, 7, 11, 9, 10, 9, 9, 9, 9]
print(len(demand))
r = 120
b = 300
l = 50
M = 30
w = 45

# Anna

# demand = [10, 8, 14, 9, 15, 6, 12, 14, 15, 15, 6, 13, 11, 11]
# print(len(demand))
# r = 120
# b = 300
# l = 50
# M = 30

# create a dictionary to store results of previous function calls
memo = {}

def V(t, s):
    # check if we have already computed the value for this t and s
    if (t, s) in memo:
        return memo[(t, s)]
    
    # otherwise, compute the value as usual
    # print(s)
    if s < 0 or s > 30:
        return (0, 0, 0, 0)
    if t == 14:
        # max_branch = max([(r * sell, 0) for sell in range(demand[t]+1)])
        max_branch = 0, s, 0, 0
    else:
        branches = []
        for buy in range(M - s + 1 + max(demand)):
            for sell in range(min(demand[t], s + buy) + 1):
                if buy <= M - s + sell:
                    branches.append((
                        r * sell - min(buy * b, b) - l * buy + V(t + 1, s - sell + buy)[0], 
                        s - sell + buy, 
                        buy, 
                        sell
                    ))
        
        max_branch = max(branches)
        
    # store the result in the dictionary for future use
    memo[(t, s)] = max_branch
        
    return max_branch
    
#print(V(0,0))
t = 0
s = 0
# while True:
#     #print(t,s)
#     prof, s, buy, sell = V(t, s)
#     # print("t, ": $", prof," | Store: ",s, " | Buy: ", buy, " | Sell: ", sell, sep='')
#     print(f"t: {t:<2} | Prof: ${prof:>6} | Store: {s:<3} | Buy: {buy:>3} | Sell: {sell:>3}")

#     t += 1
#     if t == 14:
#         break
    
spacing = [("Day", 3), ("Profit", 10), ("Buy", 3), ("Weight", 6), ("Sell", 4), ("Store", 6)]
print("|", end='')
for col in spacing:
    header, sp = col
    print(f" {header:^{sp}} |", end='')
print()

while True:
    #print(t,s)
    prof, s, buy, sell = V(t, s)
    vals = [
        t,
        "$" + str(round(prof,2)),
        buy,
        round(w * buy, 2),
        sell,
        round(s,2)
        ]
    print("|", end='')
    for i, val in enumerate(vals):
        print(f" {val:<{spacing[i][1]}} |", end='')
    print()

    t += 1
    if t == 14:
        break    
    
# price = 17160 - 7150
# price = 11130
# for i in range(14):
#     print(price - i * 300)