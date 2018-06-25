
from __future__ import division
from pyomo.environ import *

# Using the abstact model we will need to specify the index of the model, the variables, the parameters, 
# the equations of the model etc.
model = AbstractModel()

# Definition of the indices
model.i = Param(within=NonNegativeIntegers)
model.j = Param(within=NonNegativeIntegers)

# Definition of the sets
model.N = RangeSet(1,model.i)
model.M = RangeSet(1,model.j)

# Definition of the parameters
model.c = Param(model.N,model.M) # average revenue for company i and query j
model.b = Param(model.N) # budget for company i
model.d = Param(model.M) # estimated requests for query j

# Definition of the variables
model.x = Var(model.N, model.M, domain=NonNegativeReals)
model.z = Var(model.N, domain=NonNegativeReals)
model.y = Var(model.M, domain=NonNegativeReals)

# The objective function
def obj_expression(model):
    return (-1)*summation(model.c,model.x)

model.OBJ = Objective(rule=obj_expression,sense=minimize)

# The budget constraints
def b_constraint(model,i):
    return sum(model.c[i,j]*model.x[i,j] for j in model.M) + model.z[i] == model.b[i]

model.budget_constraint = Constraint(model.N, rule =b_constraint)

# The estimated request contraints
def d_constraint(model,j):
    return sum(model.x[i,j] for i in model.N) + model.y[j] == model.d[j]

model.request_constraint = Constraint(model.M, rule=d_constraint)