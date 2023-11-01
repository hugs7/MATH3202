# 2022 Q1

from gurobipy import *
	
Factories = ["A","B","C"]
Months = ["Jul","Aug","Sep","Oct","Nov","Dec"]
Grains = ["Wheat","Corn"]

F = range(len(Factories))
T = range(len(Months))
G = range(len(Grains))

Capacity = 4000
StoreCost = 1.5
Starting = [600,300]

# Demand[f][t][g]
Demand = [[[565, 290], [695, 285], [385, 315], [500, 245], [785, 270], [540, 275]], [[1050, 300], [585, 325], [510, 205], [1050, 270], [810, 210], [545, 285]], [[720, 315], [545, 465], [520, 315], [475, 465], [415, 480], [985, 525]]]

# Cost[t][g]
Cost = [[95, 43], [97, 50], [89, 76], [65, 70], [82, 49], [79, 48]]
