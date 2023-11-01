# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 18:14:51 2023

@author: Hugo Burton
"""

# Data


cache = {}
def V(t, s):
    if (t,s) in cache:
        return cache[t,s]
    # Base case
    if t == 10:
        return None

    cache[t,s] = max(... + V(t+1,...))
    return cache[t,s]

t = 1
s = 0
print(V(t, s))

