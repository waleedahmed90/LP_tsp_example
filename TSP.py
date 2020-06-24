from pulp import *
from gurobipy import *

#Problem definition
prob = LpProblem("TSP",LpMinimize)

# Defining a positive infinite integer 
pos_inf = float('inf')
#Total Number of Cities
n=5

#Cities Names
CITIES = [1, 2, 3, 4, 5]

#Cost matrix
cost = {1 : {1 : pos_inf, 2 : 20,      3 : 30,     4 : 10,     5 : 11},
		2 : {1 : 15,      2 : pos_inf, 3 : 16,     4 : 4,      5 : 2},
		3 : {1 : 3,       2 :5,        3 :pos_inf, 4 :2,       5 : 4},
		4 : {1 : 19,      2 :6,        3 :18,      4 :pos_inf, 5 : 3},
		5 : {1 : 16,      2 :4,        3 :7,       4 :16,      5 : pos_inf}}

#Xij
x = LpVariable.dicts("indicator",[(i,j) for i in CITIES for j in CITIES],0,1,LpBinary)

d = [2,3,4,5] 
U = LpVariable.dicts("dummy", d, 0, cat = 'Integer')

#OBJECTIVE_FUNCTION#
prob += lpSum( cost[i][j] * x[(i,j)] for i in CITIES for j in CITIES if(i!=j) )

#CONSTRAINTS#

#(1)
for i in CITIES:
	prob += lpSum( x[(i,j)] for j in CITIES if(i!=j) ) == 1

#(2)
for j in CITIES:
	prob += lpSum( x[(i,j)] for i in CITIES if(j!=i) ) == 1

#(3)
for i in d:
	for j in d:
		if (i!=j):
			prob += (U[i] - U[j] + n*x[(i,j)]) <= (n-1)

#(4)
for i in d:
	prob += U[i] <= (n-1)

#Solving the Integer Linear Problem
status = prob.solve()
print(status)
print(LpStatus[prob.status])

#Tolerance
TOL = 0.0001

for v in prob.variables():
	if v.value()>TOL:
		print(v.name, " = ", v.value())

print("Mininum Distance: ",prob.objective.value())



