# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pylab import *

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
                        branches.append((
                            expectation(p, 
                                        cost(sell, b_demand[t], buy, buy2) + V(t + 1, s - sell + buy, s2 - b_demand[t] + buy2)[0],
                                        cost(min(sell,demand[t]), b_demand[t], buy, buy2) + 
                                        V(t + 1, s - min(sell, demand[t]) + buy, s2 - b_demand[t] + buy2)[0]),
                            
                            int(expectation(p, s - sell + buy, s - min(sell,demand[t]) + buy)),   # Store 1
                            s2 - b_demand[t] + buy2,                                                # Store 2
                            buy,                                                                    # Buy
                            buy2,                                                                   # Buy 2
                            min(sell,demand[t]),            # Low Demand sell
                            sell)                            # High Demand Sell
                        )
        
        max_branch = max(branches)
        
    # store the result in the dictionary for future use
    memo[(t, s, s2)] = max_branch
        
    return max_branch

    
# 45

for s2 in range(2+1):
    Y = []
    for s in range(0,31):
        z = []
        for t in range(len(demand)):
            prof, s_new, s2_new, buy, buy2, low_sell, high_sell = V(t,s,s2)
            z.append(buy)
            
            
        Y.append(z)
    print(Y)
        
        
    x_low = 1
    x_high = 14
    y_low = 0
    y_high= 30

    # Generate x, y, and color data
    x = np.arange(x_low, x_high+1)  # x values
    y = np.arange(y_low, y_high+1)   # y values
        
    plt.imshow(Y, interpolation = 'none', aspect='auto', cmap='viridis', origin='lower', extent=[x.min()-0.5, x.max()+0.5, y.min()-0.5, y.max()+0.5])
    cbar = plt.colorbar(ticks=np.arange(0,23,2))
    cbar.set_label('Number of 45kg cylinders to order')

    # Grid
    # plt.pcolormesh(Y, cmap='viridis')

    # Add grid lines between values
    # plt.grid(color='gray', linestyle='-', linewidth=0.5)

    # Set the extent to shift grid lines to boundaries
    plt.gca().set_xticks(np.arange(x.min()+0.5, x.max()+0.5, 1), minor=True)
    plt.gca().set_yticks(np.arange(y.min()+0.6, y.max()+0.5, 1), minor=True)
    plt.gca().grid(True, which='minor', color='gray', linestyle='-', linewidth=0.5)

    # Set the x-axis ticks
    plt.xticks(np.arange(x_low, x_high+1,1))
    plt.yticks(np.arange(y_low, y_high+1,2))
    plt.title(f"Comm 14 - Num 45kg cyls to order \n based on current storage for each type, 90kg store={s2}")
    
    plt.xlabel('Day')
    plt.ylabel('Number of 45kg cylinders in storage')
        
    plt.show()
    
    
# 90

for s2 in range(2+1):
    Y = []
    for s in range(0,31):
        z = []
        for t in range(len(demand)):
            prof, s_new, s2_new, buy, buy2, low_sell, high_sell = V(t,s,s2)
            z.append(buy2)
            
            
        Y.append(z)
    print(Y)
        
        
    x_low = 1
    x_high = 14
    y_low = 0
    y_high= 30

    # Generate x, y, and color data
    x = np.arange(x_low, x_high+1)  # x values
    y = np.arange(y_low, y_high+1)   # y values
        
    plt.imshow(Y, interpolation = 'none', aspect='auto', cmap='viridis', origin='lower', extent=[x.min()-0.5, x.max()+0.5, y.min()-0.5, y.max()+0.5])
    cbar = plt.colorbar(ticks=np.arange(0,8+1,1))
    cbar.set_label('Number of 90kg cylinders to order')

    # Set the extent to shift grid lines to boundaries
    plt.gca().set_xticks(np.arange(x.min()+0.5, x.max()+0.5, 1), minor=True)
    plt.gca().set_yticks(np.arange(y.min()+0.6, y.max()+0.5, 1), minor=True)
    plt.gca().grid(True, which='minor', color='gray', linestyle='-', linewidth=0.5)

    # Set the x-axis ticks
    plt.xticks(np.arange(x_low, x_high+1,1))
    plt.yticks(np.arange(y_low, y_high+1,2))
    plt.title(f"Comm 14 - Num 90kg cyls to order \n based on current storage for each type, 90kg store={s2}")
    plt.xlabel('Day')
    plt.ylabel('Number of 45kg cylinders in storage')
        
    plt.show()





def schedule(t, s2):
    s = 0
    while V(t,s,s2)[3] != 0:
        s += 1
        if s == 30:
            break
    return s
    # for s in range(30+1):
    #     if V(t, s, s2)[1] == 0:
    #         return s
        
    # return s

def schedule_0(t,s2):
    s = 0
    while V(t,s,s2)[4] != 0:
        s += 1
        if s == 30:
            break
    return s
    # for s in range(30+1):
    #     if V(t, s, s2)[1] == 0:
    #         return s
        
    # return s
    




# plt.plot(range(1, len(demand)+1),[schedule(t, 0)+0.15 for t in range(len(demand))], color='blue', label='s2=0', alpha=0.75)
# plt.plot(range(1, len(demand)+1),[schedule(t, 1)-0.15 for t in range(len(demand))], color='green', label='s2=1', alpha=0.75)
# plt.plot(range(1, len(demand)+1),[schedule(t, 2) for t in range(len(demand))], color='red', label='s2=2', alpha=0.5)

# plt.legend(loc='lower left', fontsize=10)

# plt.grid(visible=True)      # Enable grid on graph

# #Axis labels
# plt.xlabel('Day')
# plt.ylabel('Number of 45kg cyls required')

# # Set the x-axis ticks
# xticks = np.arange(1, 15)  # Generate ticks from 1 to 14, inclusive, with a step of 2
# plt.xticks(xticks)  # Set the tick positions

# plt.yticks(np.arange(4,32,2))

# plt.title("Comm 14 - Num 45kg cyls required to optimise profit given num 90kg cyls")
# plt.show()

# 45kg
# for s2 in range(0,2+1):
#     for s in range(0, 30+1,10):
#         print(s,s2)
#         plt.plot(range(1, len(demand)+1),[V(t,s, s2)[3] for t in range(len(demand))], label=f's={s},s2={s2}', alpha=0.75)
#         # plt.plot(range(1, len(demand)+1),[schedule_0(t, 1)-0.15 for t in range(len(demand))], color='green', label='s2=1', alpha=0.75)
#         # plt.plot(range(1, len(demand)+1),[schedule_0(t, 2) for t in range(len(demand))], color='red', label='s2=2', alpha=0.5)
        
#     plt.legend(loc='upper right', fontsize=7)
    
#     plt.grid(visible=True)      # Enable grid on graph
    
#     #Axis labels
#     plt.xlabel('Day')
#     plt.ylabel('Number of 45kg cyls to order')
    
#     # Set the x-axis ticks
#     xticks = np.arange(1, 15)  # Generate ticks from 1 to 14, inclusive, with a step of 2
#     plt.xticks(xticks)  # Set the tick positions
    
#     plt.yticks(np.arange(0,32,2))
    
#     plt.title(f"Comm 14 - Num 45kg cyls to order based on current storage for each type, 90kg store={s2}")
#     plt.show()
    
# # 90kg
# for s in range(0, 30+1,10):
#     for s2 in range(0,2+1):
#         print(s,s2)
#         plt.plot(range(1, len(demand)+1),[V(t,s, s2)[4] for t in range(len(demand))], label=f's={s},s2={s2}', alpha=0.75)
#     plt.plot(range(1, len(demand)+1),b_demand, 'o', color='red', label='90kg Demand')
        
#     plt.legend(loc='upper right', fontsize=7)
    
#     plt.grid(visible=True)      # Enable grid on graph
    
#     #Axis labels
#     plt.xlabel('Day')
#     plt.ylabel('Number of 90kg cyls to order')
    
#     # Set the x-axis ticks
#     xticks = np.arange(1, 15)  # Generate ticks from 1 to 14, inclusive, with a step of 2
#     plt.xticks(xticks)  # Set the tick positions
    
#     plt.yticks(np.arange(0,9,1))
    
#     plt.title(f"Comm 14 - Num 90kg cyls to order based on current storage for each type, 45ks store={s}")
#     plt.show()


# # 45kg sell optimal

# for i, demand_type in enumerate([demand, h_demand]):
#     if i == 0:
#         lab = "45kg Low demand"
        
#         plt.plot(range(1,len(demand)+1),[V(t,20,2)[5] for t in range(len(demand))],label=f'Optimal # 45kg to sell')
#         plt.plot(range(1, len(demand)+1),demand_type, 'o', color='red', label=lab)
        
#         plt.legend(loc='upper right', fontsize=7)
        
#         plt.grid(visible=True)      # Enable grid on graph
        
#         #Axis labels
#         plt.xlabel('Day')
#         plt.ylabel('Number of 45kg cyls to sell')
        
#         # Set the x-axis ticks
#         xticks = np.arange(1, 15)  # Generate ticks from 1 to 14, inclusive, with a step of 2
#         plt.xticks(xticks)  # Set the tick positions
        
#         plt.yticks(np.arange(0,31,2))
        
#         plt.title(f"Comm 14 - Num 45kg cyls to sell with low demand")
#         plt.show()
#     else:
#         lab = "45kg High demand"
        
#         for s2 in range(0,2+1):
#             for s in range(0, 30+1,10):
#                 print(s,s2)
#                 plt.plot(range(1, len(demand)+1),[V(t,s, s2)[5+i] for t in range(len(demand))], label=f's={s},s2={s2}', alpha=0.75)
#             plt.plot(range(1, len(demand)+1),demand_type, 'o', color='red', label=lab)
                
#             plt.legend(loc='upper right', fontsize=7)
            
#             plt.grid(visible=True)      # Enable grid on graph
            
#             #Axis labels'
#             plt.xlabel('Day')
#             plt.ylabel('Number of 45kg cyls to sell')
            
#             # Set the x-axis ticks
#             xticks = np.arange(1, 15)  # Generate ticks from 1 to 14, inclusive, with a step of 2
#             plt.xticks(xticks)  # Set the tick positions
            
#             plt.yticks(np.arange(0,31,2))
            
#             plt.title(f"Comm 14 - Num 45kg cyls to sell with high demand and 90kg store={s2}")
#             plt.show()


    
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
    prof, s, s2, buy, buy2, low_sell, high_sell = V(t, s, s2)
    vals = [
        t,
        "$ " + str(round(prof,2)),
        buy,
        buy2,
        round(dot(weights, [buy, buy2])),
        low_sell,
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
    