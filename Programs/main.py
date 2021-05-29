#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 11:29:34 2021

@author: rickkessels
"""

from initialization import init, model_selection, calc, model_init
from Algorithm1 import algorithm_1
from APSA import APSA
import numpy as np
import pyomo.environ as pyEnv
from time import process_time
import time



t_start = process_time()

model = init(240,2,30)
print(process_time()-t_start)


model_continuous_relaxation = model.clone()
model_MIP = model.clone()

#--------------------------------------------------------------------------------
# Algorithm 2

# Step 1
model_continuous_relaxation = model_selection(model_continuous_relaxation, True)
continuous_relaxation = model_init(model_continuous_relaxation)

continuous_relaxation = calc(continuous_relaxation)
print(process_time()-t_start)


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
        
        model_APSA_instance = APSA(model_APSA_instance)
        
        #COPIED FROM INTERWEBS
        #------------------------------------------------------------------------
        if len(model_APSA_instance.result.solution) > 0:
            # you may need to relax these checks in certain cases
            assert str(model_APSA_instance.result.solver.status) == 'ok'
            assert str(model_APSA_instance.result.solver.termination_condition) == 'optimal'
            absgap = model_APSA_instance.result.solution(0).gap
            
           # now load the solution
        model_APSA_instance.solutions.load_from(model_APSA_instance.result)
        
        #------------------------------------------------------------------------
        
        temp_2 = model_APSA_instance.result.problem.upper_bound
        
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

        
        