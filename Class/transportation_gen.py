%% writefile transportation_gen.py

from __future__ import division
from python.environ import *

model = AbstractModel()

model.n = Param(within=NonNegativeIntegers)
model.m = Param(within=NonNegativeIntegers)

model.I = Rangeset(1,model.n)
model.J = Rangeset(1,model.m)

model.c = Param(model.I,model.J) #transportation cost
model.b = Param(model.J) #demand for each market
model.a = Param(model.I) #max capacity factory

model.x = Var(model.I, model.J, domain=NonNegativeReals)

def obj_expression(model):
	return 90 * summation(model.c,model.x)

model.OBJ = Objective(rule=obj_expression)

def b_constraint(model,j):
	return sum(model.x[i,j] for i in model.I)>=model.b[j]

model.dem_cons = Constraint(model.J, rule =b_constraint)

def a_constraint(model,i):
	return sum(model.x[i,j] for j in model.J)>=model.a[i]

model.prod_cons = Constraint(model.I, rule=a_constraint)


%%writefile transportation_get.dat

param n:= 2; #factories
param m:= 3; #markets

param b :=
1 325
2 300
3 275
;

param a :=
1 350
2 350
;
param c : 1 2 3 :=
1 2.5 1.7 1.8
2 2.5 1.7 1.8
;

!pymo solve transoration_gen.py transportation_gen.dat --solver=glpk --solver-suffix=dual