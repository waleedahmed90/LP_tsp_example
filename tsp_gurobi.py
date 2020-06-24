from gurobipy import *


#Problem definition
m = Model("TSP")

#Total Number of Cities
n=5

#Cities Names
CITIES = [1, 2, 3, 4, 5]

#Cost matrix
cost = {1 : {1 : GRB.INFINITY, 2 : 20,           3 : 30,           4 : 10,           5 : 11},
		2 : {1 : 15,           2 : GRB.INFINITY, 3 : 16,           4 : 4,            5 : 2},
		3 : {1 : 3,            2 : 5,            3 : GRB.INFINITY, 4 : 2,            5 : 4},
		4 : {1 : 19,           2 : 6,            3 : 18,           4 : GRB.INFINITY, 5 : 3},
		5 : {1 : 16,           2 : 4,            3 : 7,            4 : 16,           5 : GRB.INFINITY}}

#Xij
#x = LpVariable.dicts("indicator",[(i,j) for i in CITIES for j in CITIES],0,1,LpBinary)

x = m.addVars(CITIES, CITIES, vtype = GRB.BINARY)
m.update()
print(x)


d = [2,3,4,5] 
u = m.addVars(d, lb=0, vtype = GRB.CONTINUOUS)
m.update()
#print(u[3])

#OBJECTIVE_FUNCTION#
m.setObjective( quicksum(cost[i][j] * x[(i,j)] for i in CITIES for j in CITIES if(i!=j)) , GRB.MINIMIZE)
m.update()
#prob += lpSum( cost[i][j] * x[(i,j)] for i in CITIES for j in CITIES if(i!=j) )

#CONSTRAINTS#

#(1)
for i in CITIES:
	m.addConstr( 1 == quicksum(x[(i,j)] for j in CITIES if (i!=j)))
#	prob += lpSum( x[(i,j)] for j in CITIES if(i!=j) ) == 1
m.update()
#(2)
for j in CITIES:
	m.addConstr(1 == quicksum(x[(i,j)] for i in CITIES if (j!=i)))
#	prob += lpSum( x[(i,j)] for i in CITIES if(j!=i) ) == 1
m.update()

#(3)
for i in d:
	for j in d:
		if (i!=j):
			m.addConstr( (u[i] - u[j] + n*x[(i,j)]) <= (n-1) )
#			prob += (U[i] - U[j] + n*x[(i,j)]) <= (n-1)
m.update()
#(4)
for i in d:
	m.addConstr( u[i] <= (n-1) )
#	prob += U[i] <= (n-1)
m.update()
#Solving the Integer Linear Problem
#status = prob.solve()
#print(status)
#print(LpStatus[prob.status])
m.optimize()
m.printAttr('X')
#Tolerance
#TOL = 0.0001

#for v in prob.variables():
#	if v.value()>TOL:
#		print(v.name, " = ", v.value())

#print("Mininum Distance: ",prob.objective.value())



