# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 09:01:40 2023

@author: Hugo Burton
"""

# Data

emp = 2000
chg = 200
req = [155, 120, 140, 100, 155]

# State current employees

# Stage season, summer = 1, autum = 2, ..., summer = 5, finish = 6

cache = {}
def V(t, s):
    if (t,s) in cache:
        return cache[t,s]
    # Base case
    if t == 6:
        return 0
    cache[t,s] = min([chg*((a)**2) + 2000 * max(0,a +s-req[t-1]) + V(t+1, s+a) for a in range(req[t-1]-s, max(req)-s+1)])
    
    return cache[t,s]



t = 1
s = 0

print("Value", V(t, s))

