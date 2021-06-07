#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 08:02:18 2021

@author: rickkessels"""

from extension import build_problem, solve
from Check2 import check
from Algorithm_1 import algorithm_1
from Algorithm_2 import algorithm_2
import numpy as np
import csv

np.random.seed(42)

def heuristic(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total, H1_total, H2_total, H3_total, L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total, Q_total, R_total, S_total, CS1, CS2, CS3, CS4, CS5, products_total, c_k, lmbd, epsilon, tau, aff, CSString, t_start, bb):

    # Calculate associated relaxation
    model_instance, L_tot, H1_tot, H2_tot, H3_tot, P_tot, Q_tot, R_tot, S_tot = build_problem(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total, H1_total, H2_total, H3_total, L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total, Q_total, R_total, S_total, CS1, CS2, CS3, CS4, CS5, products_total, c_k)
    solve(model_instance)
    
    # Store objective value of relaxation into "upperbound". This is our upper bound as described in Step 1 of Algorithm 2.
    upperbound = model_instance.objective_value
    
    # Call algorithm 1
    allocation, r_star, x, y, s, q, z = algorithm_1(lmbd, products, shelves, segments, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total, Q_total, R_total, S_total, c_k, CS1, CS2, CS3, CS4, CS5)
    
    # Call algorithm 2
    gap, time,res, r, reason = algorithm_2(allocation, r_star, t_start, upperbound, epsilon, model_instance, tau, x, y, s, q, z, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total, Q_total, R_total, S_total, c_k, aff, products_total, CS1, CS2, CS3, CS4, CS5)
    
    # Store results into arrays
    description = "tau = "+str(tau)+', epsilon = '+str(epsilon)+', '+str(CSString)
    
    res_tot = np.hstack((description,res))
    
    sum_healthy = 0
    count_healthy_segs = 0
    count_healthy =  0
    for j in P_tot:
        for k in model_instance.segments:
            if model_instance.s[k,j].solution_value>0:
                count_healthy_segs = count_healthy_segs + 1
                sum_healthy = sum_healthy + (k.attr * model_instance.s[k,j].solution_value)/c_k
        if (sum(model_instance.s[k,j].solution_value for k in model_instance.segments)>0):
            count_healthy = count_healthy+1
    avg_healthy = sum_healthy / len(P_tot)
     
    sum_unhealthy = 0
    count_unhealthy_segs = 0
    count_unhealthy = 0
    for j in Q_tot:
        for k in model_instance.segments:
            if model_instance.s[k,j].solution_value>0:
                count_unhealthy_segs = count_unhealthy_segs + 1
                sum_unhealthy = sum_unhealthy + + (k.attr * model_instance.s[k,j].solution_value)/c_k
        if (sum(model_instance.s[k,j].solution_value for k in model_instance.segments)>0):
            count_unhealthy = count_unhealthy+1
    avg_unhealthy = sum_unhealthy / len(Q_tot)
    
    with open('Results.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow((res_tot))
    
    with open('Results.txt', 'a') as f:
        print('tau = '+str(tau)+', epsilon = '+str(epsilon)+', '+str(CSString)+': ', file=f)
        print('Gap with LP-upperbound: '+str(gap), file=f)
        print('Gap with CPLEX best bound: '+str((bb-r)/bb), file=f)
        print('Time: '+str(time), file=f)
        print('Reason: '+str(reason), file=f)
        #print('Healthy: '+str(count_healthy) + ', Segments: '+str(count_healthy_segs)+', Average: '+str(avg_healthy), file=f)
        #print('Unhealthy: '+str(count_unhealthy) + ', Segments: '+str(count_unhealthy_segs)+', Average: '+str(avg_unhealthy)+'\n', file=f)