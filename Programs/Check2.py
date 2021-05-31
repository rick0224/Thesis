#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 17:56:31 2021

@author: rickkessels
"""
def check(s_prev, x_prev, y_prev, z_prev, q_prev, model_fin, L, H1, H2, H3):
    flag = True
    all_segments = model_fin.segments
    all_shelves = model_fin.shelves
    all_products = model_fin.products
    L_array = L
    H1_array = H1
    H2_array= H2
    H3_array = H3
        # constraint 1c
    for k in all_segments:
        if (sum(s_prev[int(k.seg-1),int(j.prod-1)] for j in all_products)<= 6)==False:
            print((sum(s_prev[int(k.seg-1),int(j.prod-1)] for j in all_products)<= 6))
            print(int(k.seg-1))
            flag = False
        # constraint 1d1
    for j in all_products:
        if (j.lower * sum(x_prev[int(i.shelf-1),int(j.prod-1)] for i in all_shelves) <= sum(s_prev[int(k.seg-1),int(j.prod-1)] for k in all_segments))==False:
            print(j.lower * sum(x_prev[int(i.shelf-1),int(j.prod-1)] for i in all_shelves) <= sum(s_prev[int(k.seg-1),int(j.prod-1)] for k in all_segments))
            flag = False
        # constraint 1d2
    for j in all_products:
        if(sum(s_prev[int(k.seg-1),int(j.prod-1)] for k in all_segments) <= j.upper * sum(x_prev[int(i.shelf-1),int(j.prod-1)] for i in all_shelves))==False:
            print(sum(s_prev[int(k.seg-1),int(j.prod-1)] for k in all_segments) <= j.upper * sum(x_prev[int(i.shelf-1),int(j.prod-1)] for i in all_shelves))
            flag = False
        # constraint 1e1
    for j in all_products:
        for k in all_segments:
            if(j.minreq * y_prev[int(k.seg-1),int(j.prod-1)] <= s_prev[int(k.seg-1),int(j.prod-1)])==False:
                print(([int(k.seg-1),int(j.prod-1)]))
                print(y_prev[int(k.seg-1),int(j.prod-1)])
                print(s_prev[int(k.seg-1),int(j.prod-1)])
                flag = False
        # constraint 1e2
    for j in all_products:
        for k in all_segments:
                if(s_prev[int(k.seg-1),int(j.prod-1)] <= min(6.0, j.upper) * y_prev[int(k.seg-1),int(j.prod-1)]) ==False:
                    print("haha")
                    flag = False
        # constraint 1g
    for i in all_shelves:
        for j in all_products:
            gen = (k for k in all_segments if k.shelf == i.shelf)
            for k in gen:
                if(y_prev[int(k.seg-1),int(j.prod-1)] <= x_prev[int(i.shelf-1),int(j.prod-1)])  == False:
                    print(y_prev[int(k.seg-1),int(j.prod-1)] <= x_prev[int(i.shelf-1),int(j.prod-1)])  
                    flag = False
       # constraint 1h
    for i in all_shelves:
        for j in all_products:
            gen = (k for k in all_segments if k.shelf == i.shelf)
            if(x_prev[int(i.shelf-1),int(j.prod-1)] <= sum(y_prev[int(k.seg-1),int(j.prod-1)] for k in gen))==False:
                print(x_prev[int(i.shelf-1),int(j.prod-1)] <= sum(y_prev[int(k.seg-1),int(j.prod-1)] for k in gen))
                flag = False
        # constraint 1i
    for i in all_shelves:
        for j in all_products:
            gen1 = (k for k in all_segments if k.shelf == i.shelf and k.seg%3==0)
            gen2 = (k for k in all_segments if k.shelf == i.shelf and k.seg%3==1)
            gen_total = ((k1,k2) for k1 in gen1 for k2 in gen2 if k1.shelf==k2.shelf)
            for (k1,k2) in gen_total:
                if(q_prev[int(k1.seg-1),int(j.prod-1)]>= y_prev[int(k1.seg-1),int(j.prod-1)] + y_prev[int(k2.seg-1),int(j.prod-1)]-1)==False:
                    print(q_prev[int(k1.seg-1),int(j.prod-1)]>= y_prev[int(k1.seg-1),int(j.prod-1)] + y_prev[int(k2.seg-1),int(j.prod-1)]-1)
                    flag = False
        # constraint 1j
    for i in all_shelves:
        gen1 = (k for k in all_segments if k.shelf == i.shelf and k.seg%3!=2)
        for k in gen1:
            if(sum(q_prev[int(k.seg-1),int(j.prod-1)] for j in all_products)<=1)==False:
                print(sum(q_prev[int(k.seg-1),int(j.prod-1)] for j in all_products)<=1)
                flag = False
        # constraint 1b
    for j in all_products:
        if(sum(x_prev[int(i.shelf-1),int(j.prod-1)] for i in all_shelves) <= 1)==False:
            print((sum(x_prev[int(i.shelf-1),int(j.prod-1)] for i in all_shelves) <= 1))
            flag = False
    temp = ((k1,k2) for k1 in all_segments for k2 in all_segments if k1.seg<k2.seg and k1.shelf == k2.shelf)
    R = ((k1,k2,j) for (k1,k2) in temp for j in all_products if ((k2.seg-k1.seg-1)*6>j.upper-2*j.minreq))
        
    gen = ((k1,k2,k3) for k1 in all_segments for k2 in all_segments for k3 in all_segments if k1.shelf == k2.shelf == k3.shelf)
            # constraint 1f
    for j in all_products:
        for (k1,k2,k3) in gen:
            if (k1,k3,j) not in R:
                if k1.seg < k2.seg < k3.seg:
                    if(s_prev[int(k2.seg-1),int(j.prod-1)] >= 6 * (y_prev[int(k1.seg-1),int(j.prod-1)]+y_prev[int(k3.seg-1),int(j.prod-1)] - 1))==False:
                        print(s_prev[int(k2.seg-1),int(j.prod-1)] >= 6 * (y_prev[int(k1.seg-1),int(j.prod-1)]+y_prev[int(k3.seg-1),int(j.prod-1)] - 1))
                        flag = False
    for (k1,k2,j) in R:
        if(y_prev[int(k1.seg-1),int(j.prod-1)]+y_prev[int(k2.seg-1),int(j.prod-1)]<=1):
            print(j)
            
    for (j1, j2) in L_array:
        for i in all_shelves:
            if (x_prev[int(i.shelf-1),int(j1.prod-1)] + x_prev[int(i.shelf-1),int(j2.prod-1)] > 1 ):
                print(j1)
                flag = False
        
    for (j1, j2) in H1_array:
        for i in all_shelves:
            if(x_prev[int(i.shelf-1),int(j1.prod-1)] - x_prev[int(i.shelf-1),int(j2.prod-1)] > 0):
                print(j1.prod)
                flag = False
        
    for (j1, j2) in H2_array:
        for i in all_shelves:
            if(x_prev[int(i.shelf-1),int(j1.prod-1)] > x_prev[int(i.shelf-1),int(j2.prod-1)]):
                print(j1.prod)
                print(i.shelf)
                flag = False
                
    for (j1, j2) in H3_array:
        for i in all_shelves:
            if(x_prev[int(i.shelf-1),int(j1.prod-1)] - x_prev[int(i.shelf-1),int(j2.prod-1)] > 1 - z_prev[int(j1.prod-1),int(j2.prod-1)]):
                print(j1.prod)
                flag= False
        
    for (j1, j2) in H3_array:
        for i in all_shelves:
            if(x_prev[int(i.shelf-1),int(j1.prod-1)] - x_prev[int(i.shelf-1),int(j2.prod-1)] < -1 + z_prev[int(j1.prod-1),int(j2.prod-1)]):
                print(j1.prod)
                flag = False
            
    for (j1, j2) in H3_array:
        if(z_prev[int(j1.prod-1),int(j2.prod-1)]>sum(x_prev[int(i.shelf-1),int(j1.prod-1)] for i in all_shelves)):
           print(j1.prod)
           flag = False
        
            
    for (j1, j2) in H3_array:
        if(z_prev[int(j1.prod-1),int(j2.prod-1)]>sum(x_prev[int(i.shelf-1),int(j2.prod-1)] for i in all_shelves)):
            print(j1.prod)
            flag = False
                    
            
    for (j1, j2) in H3_array:
        if(z_prev[int(j1.prod-1),int(j2.prod-1)] < sum(x_prev[int(i.shelf-1),int(j1.prod-1)] for i in all_shelves) + sum(x_prev[int(i.shelf-1),int(j2.prod-1)] for i in all_shelves) - 1):
            print(j1.prod)
            flag = False
    
    return flag
                    
