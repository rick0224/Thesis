#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 00:06:07 2021

@author: rickkessels
"""

from extension import build_problem, solve
from Check2 import check
from Algorithm_1 import diff
import numpy as np
import timeit

np.random.seed(42)

def algorithm_2(allocation, r_star, t_start, upperbound, epsilon, model, tau, x, y, s, q, z, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, P_tot, Q_tot, R_tot, S_tot, c_k, aff, products_total, CS1, CS2, CS3, CS4, CS5):
    
    t_end = 0
        # Step 2
    r = np.sum(r_star)
    
    i_ar = []
    
    count = 0
    
    res = []
    
    differ = []
    
    flag2=False
    
    file_sol=0
    
    track2 = []
    
    x_track2=[]
    y_track2=[]
    s_track2=[]
    q_track2=[]
    z_track2=[]
    
    prev_r_star_matrix = []
    
    no_shelves = len(model.shelves)
    no_segments = len(model.segments)
    
    time_lim = 1000
    # Stopping conditions (Step 6 and 20)
    if (tau==2 or tau==3):
        time_lim = 1000
    if (aff==True):
        time_lim = 450
        
    while (t_end-t_start<time_lim and count < 50 and (upperbound-r)/upperbound>epsilon):
        
        prev_obj = (upperbound-r)/upperbound
        # Step 7
        tempset = model.shelves
        
        delta = np.flip(np.argsort(r_star))
    
        # Step 8
        while (len(tempset) > no_shelves % tau):
            
            shelves_fin = []
            products_fin = []
            segments_fin = []
            i_ar_instance = []
            
            # Step 10
            omega = np.floor(len(delta)/tau)
            
            remainder = len(delta) % tau
            
            # Step 11 and 12
            for k in range(1, tau+1):
                if (k>=tau-remainder+1):
                    i = int(np.round(np.floor(np.random.uniform(((k-1)*omega+1+(k-tau+remainder-1)),k*omega+1+(k-tau+remainder))),0))
                else:
                    i = int(np.round(np.floor(np.random.uniform(((k-1)*omega+1),k*omega+1)),0))
                print(i)
                for l in model.shelves:
                    if (delta[i-1]+1 == l.shelf):
                        i_ar.append(i-1)
                        i_ar_instance.append(l)
            
            # Delete shelf value from delta
            for i in i_ar_instance:
                delta = np.delete(delta, np.where(delta==(i.shelf-1)))
            
            # Step 13
            tempset = diff(tempset, i_ar_instance)
            
            for k in range(0,len(i_ar_instance)):
                shelves_fin.append(i_ar_instance[k].shelf)
                
                
            for k in range(0,len(shelves_fin)):
                if (shelves_fin[k] in allocation):
                    products_fin.append(allocation[shelves_fin[k]])
                            
            merged_list = []
    
            for l in products_fin:
                merged_list += l
                
            products_fin = merged_list
            
            products_fin_test = products_fin.copy()
        
        
            temp_list = list(allocation.values())
            
            merged_list = []
    
            for l in temp_list:
                merged_list += l
                
            products_allocated = merged_list
            
            for k in diff(model.products, products_allocated):
                products_fin.append(k)
            
            flag_remove = True

            while (flag_remove==True):
                flag_remove=False
                for (j1,j2) in H1_tot:
                    if ((j1 in products_fin and j2 not in products_fin)):
                        products_fin.remove(j1)     
                        flag_remove=True
                
                for (j1,j2) in H2_tot:
                    if j2 in products_allocated and j2 not in products_fin and j1 not in products_allocated:
                        for k in products_fin:
                            if k.prod==j1.prod:
                                products_fin.remove(k)
                                flag_remove=True
                                
                for (j1,j2) in H3_tot:
                    if ((j1 in products_fin and j1 not in products_fin_test and j2 in products_fin and j2 not in products_fin_test) or (j1 in products_fin_test and j2 in products_fin_test)):
                        hi = True
                    elif (j1 in products_fin):
                        products_fin.remove(j1)
                        flag_remove = True
                        
            for k in products_fin_test:
                if k not in products_fin:
                    products_fin.append(k)

            for k in model.segments:
                for l in shelves_fin:
                    if k.shelf == l:
                        segments_fin.append(k)
            
            shelves_fin = [[i] for i in shelves_fin]
            
            # Step 15
            model_fin, L, H1, H2, H3, P, Q, R, S = build_problem(products_fin, shelves_fin, segments_fin, False, False,True,True,False, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, P_tot, Q_tot, R_tot, S_tot, CS1, CS2, CS3, CS4, CS5, products_total,c_k,x,y,s,q, z)

            if flag2==True:
                model_fin.add_mip_start(file_sol)
            else:
                flag2==True
                
            sol = solve(model_fin)
            track2.append(model_fin)
            file_sol = sol.export_as_mst()
            
            x_prev = x.copy()
            y_prev = y.copy()
            s_prev = s.copy()
            q_prev = q.copy()
            z_prev = z.copy()
            
            if check(s_prev, x_prev, y_prev, z_prev, q_prev, model_fin, L, H1, H2, H3, L_dummy, H1_dummy, H2_dummy, H3_dummy)==False:                            
                exit
            
            x_track2.append(x_prev)
            y_track2.append(y_prev)
            s_track2.append(s_prev)
            q_track2.append(q_prev)
            z_track2.append(z_prev)
            
            # Step 17 and 18
            for j in model_fin.products:
                for i in model_fin.shelves:
                    x[int(i.shelf - 1),int(j.prod - 1)]=round(model_fin.x[i,j].solution_value,5)
                for k in model_fin.segments:
                    y[int(k.seg-1),int(j.prod-1)]=round(model_fin.y[k,j].solution_value,5)
                    s[int(k.seg-1),int(j.prod-1)]=round(model_fin.s[k,j].solution_value,5)
                    
            for l in model_fin.products:
                for k in model_fin.segments:
                    if(int(k.seg)<no_segments):
                        if(y[int(k.seg - 1),int(l.prod- 1)]==1 and y[int(k.seg),int(l.prod- 1)]==1):
                            q[int(k.seg - 1),int(l.prod- 1)]=1
                        else:
                            q[int(k.seg - 1),int(l.prod- 1)]=0
            
            for j1 in model_fin.products:
                for j2 in model_fin.products:
                    z[int(j1.prod-1),int(j2.prod-1)]=round(model_fin.z[j1,j2].solution_value,5)

            prev = 0
            new = 0
            prev_r_star = r_star.copy()
            
            prev_r_star_matrix.append(prev_r_star)
            
            print(r_star)
            
            # Step 16
            for i in model_fin.shelves:
                prev = prev + prev_r_star[int(i.shelf-1)]
                new = new + sum(sum(j[3]* k[2] * s[int(k.seg)-1,int(j.prod)-1] / c_k for k in model_fin.segments if k.shelf==i.shelf) for j in model_fin.products)
                r_star[int(i.shelf-1)] = sum(sum(j[3]* k[2] * s[int(k.seg)-1,int(j.prod)-1] / 6.0 for k in model_fin.segments if k.shelf==i.shelf) for j in model_fin.products)
            if (prev - sum(sum(j[3]* k[2] * s_prev[int(k.seg)-1,int(j.prod)-1] / c_k for k in model_fin.segments) for j in model_fin.products)) > 1e-7 or (prev - sum(sum(j[3]* k[2] * s_prev[int(k.seg)-1,int(j.prod)-1] / 6.0 for k in model_fin.segments) for j in model_fin.products) < -1e-7):
                exit
            differ.append(new-prev)
            if (new-prev<-1e-7):
                exit
                
            allocation = {}
            
            for i in model.shelves:
                prod_shelf = []
                for j in model.products:
                    if x[int(i.shelf - 1),int(j.prod - 1)]==1:
                        print(str(int(i.shelf - 1))+","+str(int(j.prod - 1)))
                        prod_shelf.append(j)
                allocation[int(i.shelf)] = prod_shelf 
                        
            r = np.sum(r_star)
            
            if ((upperbound-r)/upperbound < epsilon):
                break
            
        print((upperbound-r)/upperbound)
        res.append(((upperbound-r)/upperbound))
        if (prev_obj == (upperbound-r)/upperbound):
            count = count + 1
        else:
            count = 0
            
        t_end = timeit.default_timer()
        print(t_end-t_start)
    

    time = t_end-t_start
    gap = (upperbound-r)/upperbound
    
    if (time > time_lim):
        reason = "Time limit reached"
    elif (count >= 50):
        reason = "No improvement in 50 iterations"
    elif ((upperbound-r)/upperbound<=epsilon):
        reason = "Gap < Epsilon!"
    
    return gap, time, res, r, reason