
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

model.AT = Param(model.J,model.I)  
model.c = Param(model.J)          
model.b = Param(model.I)          

#Definition of the variables
model.y = Var(model.I, domain=NonPositiveReals)


#Objective function
#first we define previously a function that will be called after, when definig the objective function
def obj_expression(model):
    return summation(model.b,model.y)

model.OBJ = Objective(rule=obj_expression,sense=maximize)

#The total expenses of one enterprise in advertisement cannot be higher than the total budget that it has
def A_constraint(model,j):
    return sum(model.AT[j,i]*model.y[i] for i in model.I) <= model.c[j]

model.cons = Constraint(model.J, rule=A_constraint)