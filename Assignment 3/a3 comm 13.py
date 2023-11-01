# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pylab import *

# Hugo (me)
demand = [14, 13, 10, 14, 13, 6, 7, 11, 9, 10, 9, 9, 9, 9]
h_demand = [17, 17, 15, 21, 21, 14, 16, 17, 15, 19, 12, 16, 13, 13]
print(len(demand))
r = 120
b = 300
l = 50
M = 30
w = 45
first_day_w_cap = 1000
day_cap = 1000 // 45 # No more than 22 on the first day


# Anna

# demand = [10, 8, 14, 9, 15, 6, 12, 14, 15, 15, 6, 13, 11, 11]
# h_demand = [13, 12, 18, 13, 23, 10, 17, 20, 18, 18, 14, 18, 14, 20]
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
            for sell in range(min(h_demand[t], s + buy) + 1):
                if buy <= min(M - s + min(sell, demand[t]), day_cap): 
                    branches.append((
                            0.4*(r * sell - min(buy * b, b) - l * buy + V(t + 1, s - sell + buy)[0])
                            +
                            (1-0.4) * (r * min(sell,demand[t]) - min(buy * b, b) - l * buy + V(t + 1, s - min(sell,demand[t]) + buy)[0]), 
                            int(0.4 * (s - sell + buy) + (1-0.4) * (s - min(sell,demand[t]) + buy)), 
                            buy, 
                            int(0.4 * (sell) + (1-0.4) * (min(sell,demand[t]))))
                    )
        
        max_branch = max(branches)
        
    # store the result in the dictionary for future use
    memo[(t, s)] = max_branch
        
    return max_branch
    



    
def schedule(t):
    # return V(t,s)[2]
    s = 0
    while V(t,s)[2] != 0:
        s += 1
    return s
    # for s in range(30+1):
    #     if V(t, s, s2)[1] == 0:
    #         return s
        
    # return s


plt.plot(range(1,len(demand)+1),[schedule(t) for t in range(len(demand))])

plt.grid(visible=True)      # Enable grid on graph

#Axis labels
plt.xlabel('Day')
plt.ylabel('Number of 45kg Cylinders')

plt.xticks(np.arange(1, 15,1))
plt.yticks(np.arange(0,31,2))

plt.title('Number of 45kg cyls required to make optimal profit')

plt.show()


#####


Y = []
for s in range(0,31):
    z = []
    for t in range(len(demand)):                  
        prof,store, buy, sell = V(t,s)
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

#Axis labels
plt.xlabel('Day')
plt.ylabel('Number of 45kg cylinders in storage')
    
plt.title(f"Comm 13 - Num 45kg cyls to order")
plt.show()


###



# # Create meshgrid for x and y values
# X, Y = np.meshgrid(x, y)

# # Create the imshow plot
# plt.imshow(z, interpolation='none', aspect='auto', cmap='viridis',
#            extent=[x.min()-0.5, x.max()+0.5, y.min()-0.5, y.max()+0.5])

# # Add labels and title


#####






#print(V(0,0))
t = 0
s = 0
  
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
        "$ " + str(round(prof,2)),
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

