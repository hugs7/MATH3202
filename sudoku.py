# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 14:51:03 2023

@author: Hugo Burton
"""

import gurobipy as gp
from gurobipy import GRB

# Define the Sudoku problem instance
puzzle = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

# Create a new Gurobi model
model = gp.Model("Sudoku")

# Create decision variables for each cell in the Sudoku puzzle
cells = []
for i in range(9):
    row = []
    for j in range(9):
        col = []
        for k in range(1, 10):
            col.append(model.addVar(vtype=GRB.BINARY, name=f"x_{i}{j}{k}"))
        row.append(col)
    cells.append(row)

# Add constraints to ensure that each cell contains exactly one number
for i in range(9):
    for j in range(9):
        model.addConstr(gp.quicksum(cells[i][j]) == 1)

# Add constraints to ensure that each row contains each number exactly once
for i in range(9):
    for k in range(1, 10):
        model.addConstr(gp.quicksum(cells[i][j][k-1] for j in range(9)) == 1)

# Add constraints to ensure that each column contains each number exactly once
for j in range(9):
    for k in range(1, 10):
        model.addConstr(gp.quicksum(cells[i][j][k-1] for i in range(9)) == 1)

# Add constraints to ensure that each 3x3 sub-grid contains each number exactly once
for k in range(1, 10):
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            model.addConstr(gp.quicksum(cells[a][b][k-1] for a in range(i, i+3) for b in range(j, j+3)) == 1)

# Add constraints to enforce the initial numbers in the Sudoku puzzle
for i in range(9):
    for j in range(9):
        if puzzle[i][j] != 0:
            model.addConstr(cells[i][j][puzzle[i][j]-1] == 1)

# Set objective to zero (Sudoku is a constraint satisfaction problem)
model.setObjective(0, GRB.MINIMIZE)

# Optimize the model
model.optimize()

# Print the solution
for i in cells:
    for j in i:
        for k in j:
            print(k.x)
