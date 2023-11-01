# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 10:06:33 2023

@author: Hugo Burton
"""

# Factorial

def factorial(i):
    if i == 1:
        return 1
    else:
        return factorial(i - 1) * i
    
    
print(factorial(5))

# Minimal studying
# Data

prs = {
       "Algebra": [0.2, 0.3, 0.35, 0.38, 0.4],
       "Calculus": [0.25, 0.3, 0.33, 0.35, 0.38], 
       "Statistics": [0.1, 0.3, 0.4, 0.45, 0.5]
       }

# Min prob of failing failing subjects j, ..., 2 with s hours of study available
def Value(j, s, prs):
    print(prs)
    if j == 3:
        return 1
    else:
        inner = []
        for i, a in enumerate(range(s)):
            inner.append((1 - prs[i][j]) * Value(j+1, s-a,prs))
        return min(inner)






#print(Value(0,4,prs))

# Knapsack problem

sizes = {1: 7,
         2: 4,
         3: 3
    }

values = {1 : 25,
          2 : 12,
          3 : 8}

def knapsack(j,s):
    if j not in sizes:
        return (0,None)
    else:
        return max([(values[j]*a + knapsack(j+1,s-sizes[j]*a)[0],a,s-sizes[j]*a) for a in range((s//sizes[j])+1)])
    


print(knapsack(1,20))
print(knapsack(2,6))
print(knapsack(3,6))
print(knapsack(1,100))

# Maximum value of packing items into a voliume of s
# def knapsack2(s):
#     if s < min(sizes[a] for a in sizes):
#         return (0,None)
#     else:
#         return max([(values[a] + knapsack2(s-sizes[a])[0],a,s-sizes[a]) for a in sizes if sizes[a] <= s])

def knapsack2(s, cache={}):
    if s in cache:
        return cache[s]
    elif s < min(sizes[a] for a in sizes):
        result = (0,None)
    else:
        result = max([(values[a] + knapsack2(s-sizes[a], cache)[0],a,s-sizes[a]) for a in sizes if sizes[a] <= s])
    cache[s] = result
    return result

print()

print(knapsack2(8))
print(knapsack2(100))

def fib(n, computed = {0: 0, 1: 1}):
     if n not in computed:
         computed[n] = fib(n-1, computed) + fib(n-2, computed)
     return computed[n]

print("hi")
print(fib(20))
