# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Hugo (me)
demand = [14, 13, 10, 14, 13, 6, 7, 11, 9, 10, 9, 9, 9, 9]
h_demand = [17, 17, 15, 21, 21, 14, 16, 17, 15, 19, 12, 16, 13, 13]
b_demand = [2, 3, 2, 2, 3, 2, 2, 2, 2, 5, 2, 3, 4, 5]   # Always need to meet demand
print(len(demand))

rev = [120, 230]
b = 300     # Base delivery fee
cyl_cost = [50, 80]
max_store = [30, 2]
weights = [45, 90]
day_w_cap = 1000
p = 0.4

# Anna

# demand = [10, 8, 14, 9, 15, 6, 12, 14, 15, 15, 6, 13, 11, 11]
# h_demand = [13, 12, 18, 13, 23, 10, 17, 20, 18, 18, 14, 18, 14, 20]
# print(len(demand))
# r = 120
# b = 300
# l = 50
# M = 30

def cost(sell, sell2, buy, buy2):
    return dot(rev, [sell, sell2]) - min((buy + buy2) * b, b) - dot(cyl_cost, [buy, buy2])


def expectation(p, x1, x2):
    return p * x1 + (1 - p) * x2


def dot(A, B):
    dp = 0
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            if i == j:
                dp += a * b
                
    return dp

# create a dictionary to store results of previous function calls
memo = {}

def V(t, s, s2):
    # check if we have already computed the value for this t and s
    if (t, s, s2) in memo:
        return memo[(t, s, s2)]
    
    # otherwise, compute the value as usual
    # print(s)
    if s < 0 or s > max_store[0] or s2 < 0 or s2 > max_store[1]:
        return (0, max(0, min(max_store[0], s)), max(0, min(max_store[1], s2)), 0, 0, 0)
    if t == 14:
        # max_branch = max([(r * sell, 0) for sell in range(demand[t]+1)])
        max_branch = 0, s, s2, 0, 0, 0
    else:
        branches = []
        for buy in range(max_store[0] - s + max(demand) + 1):
            for buy2 in range(max_store[1] - s2 + b_demand[t] + 1):
                for sell in range(min(h_demand[t], s + buy) + 1):
                    if dot(weights, [buy, buy2]) <= day_w_cap and buy <= max_store[0] - s + min(sell, demand[t]) and b_demand[t] <= s2 + buy2: 
                        # branches.append((
                        #     expectation(p, 
                        #                 cost(sell, b_demand[t], buy, buy2) + V(t + 1, s - sell + buy, s2 - b_demand[t] + buy2)[0],
                        #                 cost(min(sell,demand[t]), b_demand[t], buy, buy2) + 
                        #                 V(t + 1, s - min(sell, demand[t]) + buy, s2 - b_demand[t] + buy2)[0]),
                            
                        #     int(expectation(p, s - sell + buy, s - min(sell,demand[t]) + buy)),     # Store 1
                        #     s2 - b_demand[t] + buy2,                                                # Store 2
                        #     buy,                                                                    # Buy
                        #     buy2,                                                                   # Buy 2
                        #     int(expectation(p, sell, min(sell,demand[t]))))                         # Sell
                        # )
                        
                        # Substitution of 90 kg cylinder for 2 * 45 kg cylinders
                        for r in range(b_demand[t] + 1):
                            sell2 = b_demand[t] - r
                            sell_new = sell + 2 * r
                            if s + buy - sell_new < 0 or s2 + buy2 - sell2 > max_store[1]:
                                continue
                        
                            branches.append((
                                expectation(p, 
                                            cost(sell_new, b_demand[t], buy, buy2) + V(t + 1, s - sell_new + buy, s2 - sell2 + buy2)[0],
                                            cost(min(sell_new,demand[t]), sell2, buy, buy2) + 
                                            V(t + 1, s - min(sell_new, demand[t]) + buy, s2 - sell2 + buy2)[0]) - 10 * r,
                                
                                int(expectation(p, s - sell_new + buy, s - min(sell_new,demand[t]) + buy)),     # Store 1
                                s2 - sell2 + buy2,                                                      # Store 2
                                buy,                                                                    # Buy
                                buy2,                                                                   # Buy 2
                                int(expectation(p, sell_new, min(sell_new,demand[t]))))                         # Sell
                            )
        
        max_branch = max(branches)
        
    # store the result in the dictionary for future use
    memo[(t, s, s2)] = max_branch
        
    return max_branch
    
#print(V(0,0))
t = 0
s = 0
s2 = 0

spacing = [("Day", 3), ("Profit", 10), ("Buy", 3), ("Buy2", 4), ("Weight", 6), ("Sell", 4), ("Sell2", 5), ("Store", 6), ("Store2", 6)]
print("|", end='')
for col in spacing:
    header, sp = col
    print(f" {header:^{sp}} |", end='')
print()

while True:
    #print(t,s)
    prof, s, s2, buy, buy2, sell = V(t, s, s2)
    vals = [
        t,
        "$ " + str(round(prof,2)),
        buy,
        buy2,
        round(dot(weights, [buy, buy2])),
        sell,
        b_demand[t],
        round(s,2),
        round(s2,2)
        ]
    print("|", end='')
    for i, val in enumerate(vals):
        print(f" {val:<{spacing[i][1]}} |", end='')
    print()

    t += 1
    if t == 14:
        break
    
    
