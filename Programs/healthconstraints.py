#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 11:23:13 2021

@author: rickkessels
"""

from extension import init, build_problem, solve, get_cut_stats
from Check2 import check
from Algorithm_1 import algorithm_1, diff
from Algorithm_2 import algorithm_2
from heuristic import heuristic
from solToExcel import solToExcel
import numpy as np
import timeit
import sys
import csv

np.random.seed(42)

def healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total, H1_total, H2_total, H3_total, L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total, Q_total, R_total, S_total, CS1, CS2, CS3, CS4, CS5, products_total, c_k, CSString):
    
    model_instance, L_tot, H1_tot, H2_tot, H3_tot, P_tot, Q_tot, R_tot, S_tot = build_problem(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total, H1_total, H2_total, H3_total, L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total, Q_total, R_total, S_total, CS1, CS2, CS3, CS4, CS5, products_total, c_k)
    
    # Solve APSA, and store all information we need into arrays
    solve(model_instance, 1000)
    
    solToExcel(model_instance, CSString)
    
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
    
    with open('Results.txt', 'a') as f:
        print('APSA with the two inequalities and '+str(CSString)+": ", file=f)
        print('B&B/C: '+str(model_instance.solve_details.nb_nodes_processed), file=f)
        print("Objective: "+str(model_instance.objective_value), file=f)
        print("Best bound: "+str(model_instance.solve_details.best_bound), file=f)
        print('Gap: '+str(model_instance.solve_details.gap), file=f)
        print('Time: '+str(model_instance.solve_details.time), file=f)
        #print('Healthy: '+str(count_healthy) + ', Segments: '+str(count_healthy_segs)+', Average: '+str(avg_healthy), file=f)
        #print('Unhealthy: '+str(count_unhealthy) + ', Segments: '+str(count_unhealthy_segs)+', Average: '+str(avg_unhealthy)+'\n', file=f)
        