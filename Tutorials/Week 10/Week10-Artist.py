costs = [
    [0, 143, 108, 118, 121, 88, 121, 57, 92],    # Home
    [143, 0, 35, 63, 108, 228, 182, 73, 162],    # A
    [108, 35, 0, 45, 86, 193, 165, 42, 129],     # B
    [118, 63, 45, 0, 46, 190, 203, 73, 105],     # C
    [121, 108, 86, 46, 0, 172, 224, 98, 71],     # D
    [88, 228, 193, 190, 172, 0, 174, 160, 108],  # E
    [121, 182, 165, 203, 224, 174, 0, 129, 212], # F
    [57, 73, 42, 73, 98, 160, 129, 0, 117],      # G
    [92, 162, 129, 105, 71, 108, 212, 117, 0]    # H
]

p = [
    [0.0, 0.0, 0.0], # Home
    [0.3, 0.4, 0.3], # A
    [0.2, 0.5, 0.3], # B
    [0.2, 0.7, 0.1], # C
    [0.3, 0.5, 0.2], # D
    [0.3, 0.6, 0.1], # E
    [0.4, 0.3, 0.3], # F
    [0.0, 0.3, 0.7], # G 
    [0.1, 0.1, 0.8]  # H
]

Home = 0
Price = 500
Cities = range(len(costs))
K = range(3)


sales = [sum(p[i][k]*k for k in K) for i in Cities]

def value(S):
    #print("here",S)
    if len(S) == 0:
        s_t = 0
    else:
        s_t = S[-1]
    if len(S) == 4:
        return - costs[s_t][0], 0
    else:
        return max([(Price * sales[a_t] - costs[s_t][a_t] + value(S + [a_t])[0],a_t) for a_t in Cities if a_t not in S])
    

CV = []
while True:
    pr, s_t = value(CV)
    CV += [s_t]
    print(pr, s_t)
    if CV[-1] == 0:
        break



def value_b(S, n):
    #print("here",S)
    if len(S) == 0:
        s_t = 0
    else:
        s_t = S[-1]
    if len(S) == 4 or n == 0:
        return - costs[s_t][0], 0, n
    else:
        
        return max([(- costs[s_t][a_t] +
                    sum(p[a_t][k] * 
                        (Price * min(n,k) + value_b(S + [a_t], n - min(n,k))[0]) for k in K),a_t,n)
                    for a_t in Cities if a_t not in S])
    

# CV = []
# av = 5
# while True:
#     pr, s_t, av = value_b(CV, av)
#     CV += [s_t]
#     print(pr, s_t, av)
#     if CV[-1] == 0:
#         break
