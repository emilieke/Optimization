
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
model.c = Param(model.N,model.M) #revenue
model.b = Param(model.N) #budget for company
model.d = Param(model.M) #estimated requests for query

# Definition of the dual variables
model.alpha = Var(model.N)
model.beta = Var(model.M)

# The objective function
def obj_expression(model):
    return (summation(model.b,model.alpha) + summation(model.d,model.beta))

model.OBJ = Objective(rule=obj_expression,sense=maximize)

# The dual constraints
def d_constraint(model,i,j):
    return model.c[i,j]*model.alpha[i]+model.beta[j]<= (-1)*model.c[i,j]

model.dual_constraint = Constraint(model.N,model.M, rule =d_constraint)