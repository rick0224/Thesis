#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 11:29:34 2021

@author: rickkessels
"""

from initialization import init, model_selection, calc
from Algorithm1 import algorithm_1
from APSA import APSA
import numpy as np
import pyomo.environ as pyEnv
from time import process_time

t_start = process_time()

model = init(30, 5, 10)

model_continuous_relaxation = model.clone()
model_MIP = model.clone()

#--------------------------------------------------------------------------------
# Algorithm 2

# Step 1
model_continuous_relaxation = model_selection(model_continuous_relaxation, True)
continuous_relaxation = calc(model_continuous_relaxation)
print(continuous_relaxation.objective())

# Step 2, 3 and 4

model_MIP = model_selection(model_MIP, False)
r_star, r, x, y, s = algorithm_1(continuous_relaxation, model_MIP)

# Step 5

r_star_prev = 0

tau = 4

counter = 1

model_APSA = model.clone()
model_APSA.tempset = pyEnv.RangeSet(1,len(model.B),1)
temp = len(model_APSA.tempset)

epsilon = 0.5

i_ar = []

count = 0

absgap = 1.00

temp_2 = 1.00

while (absgap/temp_2 > epsilon):
    
    while (temp > len(model_MIP.B) % tau):
        
        delta = np.flip(np.argsort(r))[:count*tau]
        
        omega = round(len(delta)/tau)
        
        model_APSA_instance = model_APSA.clone()
        model_APSA_instance = model_selection(model_APSA_instance, False)
        
        model_APSA_instance.i = pyEnv.Set()
        
        for k in range(1, tau+1):
            i = int(np.round(np.floor(np.random.uniform(((k-1)*omega+1),k*omega+1)),0))
            if (i not in i_ar):
                i_ar.append(i)
            
        b_set = []   
        for j in range(1,len(model.B)+1):
            if (j not in i_ar and j not in b_set):
                b_set.append(j)
        
        model_APSA_instance.B = pyEnv.Set(initialize=b_set)
        temp = len(b_set)
        
        APSA(model_APSA_instance)
        
            #Solves
        solver = pyEnv.SolverFactory('cplex_direct')
        solver.options['timelimit'] = 3600
        results = solver.solve(model_APSA_instance, tee=True, load_solutions=False)
        #COPIED FROM INTERWEBS
        #------------------------------------------------------------------------
        if len(results.solution) > 0:
            # you may need to relax these checks in certain cases
            assert str(results.solver.status) == 'ok'
            assert str(results.solver.termination_condition) == 'optimal'
            absgap = results.solution(0).gap
            
           # now load the solution
        model_APSA_instance.solutions.load_from(results)
        
        #------------------------------------------------------------------------
        
        temp_2 = results.problem.upper_bound
        
        r_star_prev = r_star
        r_star = model_APSA_instance.objective()
        
        print(r_star_prev)
        print(r_star)
        
        print(absgap)
        
        x = model_APSA_instance.x
        y = model_APSA_instance.y
        s = model_APSA_instance.s
        
        count = count + 1
        
t_stop = process_time()

print(t_stop - t_start)

        
        