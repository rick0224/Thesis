#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 16:59:44 2021

@author: rickkessels
"""

import numpy as np

def solToExcel(model, descr):
    
    no_shelves = len(model.shelves)
    no_products = len(model.products)
    no_segments = len(model.segments)
    
    x_sol = np.zeros((no_shelves, no_products))
    y_sol = np.zeros((no_segments, no_products))
    s_sol = np.zeros((no_segments, no_products))
    q_sol = np.zeros((no_segments, no_products))
    z_sol = np.zeros((no_products, no_products))
    
    # Step 17 and 18
    for j in model.products:
        for i in model.shelves:
            x_sol[int(i.shelf - 1),int(j.prod - 1)]=round(model.x[i,j].solution_value,5)
        for k in model.segments:
            y_sol[int(k.seg-1),int(j.prod-1)]=round(model.y[k,j].solution_value,5)
            s_sol[int(k.seg-1),int(j.prod-1)]=round(model.s[k,j].solution_value,5)
            
    for l in model.products:
        for k in model.segments:
            if(int(k.seg)<len(model.segments)):
                if(y_sol[int(k.seg - 1),int(l.prod- 1)]==1 and y_sol[int(k.seg),int(l.prod- 1)]==1):
                    q_sol[int(k.seg - 1),int(l.prod- 1)]=1
                else:
                    q_sol[int(k.seg - 1),int(l.prod- 1)]=0
    
    for j1 in model.products:
        for j2 in model.products:
            z_sol[int(j1.prod-1),int(j2.prod-1)]=round(model.z[j1,j2].solution_value,5)

    np.savetxt('Results_'+descr+'_x.csv', x_sol, delimiter=",")
    np.savetxt('Results_'+descr+'_y.csv', y_sol, delimiter=",")
    np.savetxt('Results_'+descr+'_s.csv', s_sol, delimiter=",")
    np.savetxt('Results_'+descr+'_q.csv', q_sol, delimiter=",")
    np.savetxt('Results_'+descr+'_z.csv', z_sol, delimiter=",")
    