# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 18:14:51 2023

@author: Hugo Burton
"""


# Data
nums = [0,1,2,3,4,5,6,7,8,9]
P = [0,1,2,3]

def V(b,s,n):
    # if b == 3:
    #     print(b,s,n)
    if b == 5:
        return (10*n[0] + n[1]) * (10*n[2] + n[3])
    
    branches = []
    for j in P:      # for each position
        if s[j] == 1:
            continue        # Position has already been filled
        prs = []
        for i in list(set(nums) - set(n)):      # For each number that hasn't been used
            # Update used positions
            new_s = [k for k in s]
            new_s[j] = 1
            # Update numbers filled
            new_n = [k for k in n]
            new_n[j] = i
            
            
            prs.append(1/(len(nums)-s.count(1)) * V(b+1, new_s, new_n))
                
        branches.append(sum(prs))

    # So branches will be a list of at most four actions - one for each position
    # We don't get to choose the number, only the 
    return min(branches)



print(V(1,[0,0,0,0], [-1, -1, -1, -1]))    

