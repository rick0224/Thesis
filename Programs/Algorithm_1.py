#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 23:04:02 2021

@author: rickkessels
"""

import numpy as np
from Thesis_Repl_APSA import build_problem, solve

def algorithm_1(lmbd, products_total, shelves_total, segments_total, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k):
    # Algorithm 1 starts here
        
    # Calculate sigma, and initialize other variables
    sigma = np.flip(np.argsort(lmbd))
    
    selected_products = []
    
    no_shelves = len(shelves_total)
    no_products = len(products_total)
    no_segments = len(segments_total)
    
    products = products_total
    
    r_star = np.zeros(no_shelves)
    
    x = np.zeros((no_shelves, no_products))
    y = np.zeros((no_segments, no_products))
    s = np.zeros((no_segments, no_products))
    q = np.zeros((no_segments, no_products))
    z = np.zeros((no_products, no_products))
    
    allocation = {}
    
    track = []
    
    x_track=[]
    y_track=[]
    s_track=[]
    q_track=[]
    z_track=[]
    
    for shelf_i in sigma: # Step 2, with stopping condition (Step 13) automatically included.
        if (len(products_total)==0): # Stopping condition (Step 13).
            break
        
        # Step 3
        shelf = [shelves_total[shelf_i]]
        segments = [segments_total[shelf_i*3], segments_total[shelf_i*3+1], segments_total[shelf_i*3+2]]
        model_SSP, L, H1, H2, H3 = build_problem(products, shelf, segments, False, True,True,True,True, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, products, c_k)
        solve(model_SSP)
        
        track.append(model_SSP)
        
        if(len(track)==18):
            print("yay")
        
        for m in model_SSP.shelves:
            for j1 in model_SSP.products:
                if (round(model_SSP.x[m,j1].solution_value)==1):
                    selected_products.append(j1)
                    x[int(m.shelf-1),int(j1.prod - 1)]=1
                    for j2 in model_SSP.products:
                        if (round(model_SSP.x[m,j2].solution_value)==1):
                            z[int(j1.prod- 1), int(j2.prod- 1)]=1
                
        
        for l in model_SSP.products:
            for k in model_SSP.segments:
                if (round(model_SSP.y[k,l].solution_value)==1):
                    y[int(k.seg - 1),int(l.prod- 1)]=1
                s[int(k.seg-1),int(l.prod-1)]=round(model_SSP.s[k,l].solution_value,5)
        
        for l in model_SSP.products:
            for k in model_SSP.segments:
                if(int(k.seg)<no_segments):
                    if(y[int(k.seg - 1),int(l.prod- 1)]==1 and y[int(k.seg),int(l.prod- 1)]==1):
                        q[int(k.seg - 1),int(l.prod- 1)]=1
                    else:
                        q[int(k.seg - 1),int(l.prod- 1)]=0
        
        # Step 5 until step 12
        for (j1,j2) in H3:
            if j1 in selected_products and j2 not in selected_products:
                selected_products.append(j2)
            elif j2 in selected_products and j1 not in selected_products:
                selected_products.append(j1)
                
        x_track.append(x.copy())
        y_track.append(y.copy())
        s_track.append(s.copy())
        q_track.append(q.copy())
        z_track.append(z.copy())
    
        # Step 4
        allocation[shelf_i+1] = selected_products
        products = diff(model_SSP.products, selected_products)
        
        for (j1,j2) in H2_tot:
            if j2 in selected_products:
                for k in products:
                    if k.prod==j1.prod:
                        products.remove(k)
                        
        r_star[shelf_i] = sum(sum(j[3]* k[2] * s[int(k.seg)-1,int(j.prod)-1] / 6.0 for k in model_SSP.segments if k.shelf==shelf_i+1) for j in model_SSP.products)
        selected_products = []
        
    return allocation, r_star, x, y, s, q, z

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]