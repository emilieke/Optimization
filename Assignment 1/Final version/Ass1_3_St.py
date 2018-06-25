
from __future__ import division 
from pyomo.environ import *
#Using the abstact model we will need to specify the index of the model, the variables ,the parameters, 
#the equations of the model, etc.
model = AbstractModel()

#We specify that both parameters n and m are Non Negative Integers

model.n = Param(within = NonNegativeIntegers)  #Total number of average revenues per user (j=1,...,n)
model.m = Param(within = NonNegativeIntegers)  #Total number of constraints (i=1,...,m)

#Definition of the indexes
#The index i will go from 1 to m 
#The index j will go from 1 to n

model.I = RangeSet(1,model.m)    
model.J = RangeSet(1,model.n)    

model.A = Param(model.I,model.J)  
model.c = Param(model.J)          
model.b = Param(model.I)          

#Definition of the variables
model.x = Var(model.J, domain=NonNegativeReals)
#Definition of slack variables
model.z = Var(model.I, domain=NonNegativeReals)

#Objective function
#first we define previously a function that will be called after, when defining the objective function
def obj_expression(model):
    return summation(model.c,model.x)

model.OBJ = Objective(rule=obj_expression)

#The total expenses of one enterprise in advertisement cannot be higher than the total budget that it has
def A_constraint(model,i):
    return sum(model.A[i,j]*model.x[j] for j in model.J) + model.z[i] == model.b[i]

model.cons = Constraint(model.I, rule=A_constraint)