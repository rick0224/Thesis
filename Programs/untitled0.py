#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 29 23:20:18 2021

@author: rickkessels
"""

flag = True
all_segments = model_fin.segments
all_shelves = model_fin.shelves
all_products = model_fin.products
L_array = 
H1_array = H1_total[0]
H2_array = H2_total[0]
H3_array = H3_total[0]

# constraint 1c
for k in all_segments:
    if sum(s_prev[int(k.seg-1),int(j.prod)-1] for j in all_products) > 6:
        print("1")
            
# constraint 1d1
for j in all_products:
    if (j.lower * sum(x_prev[int(i.shelf)-1,int(j.prod)-1] for i in all_shelves) > sum(s_prev[int(k.seg)-1,int(j.prod)-1] for k in all_segments)):
        print("2")
        print(j.lower * sum(x_prev[int(i.shelf)-1,int(j.prod)-1] for i in all_shelves) - sum(s_prev[int(k.seg)-1,int(j.prod)-1] for k in all_segments))
    
# constraint 1d2
for j in all_products:
    if (sum(s_prev[int(k.seg)-1,int(j.prod)-1] for k in all_segments) > j.upper * sum(x_prev[int(i.shelf)-1,int(j.prod)-1] for i in all_shelves)):
        print("3")
        
# constraint 1e1
for j in all_products:
    for k in all_segments:
        if(j.minreq * y_prev[int(k.seg)-1,int(j.prod)-1] > s_prev[int(k.seg)-1,int(j.prod)-1]):
            print("4")
            
# constraint 1e2
for j in all_products:
    for k in all_segments:
        if (s_prev[int(k.seg)-1,int(j.prod)-1] > min(6.0, j.upper) * y_prev[int(k.seg)-1,int(j.prod)-1]):
            print("5")
            
# constraint 1g
for i in all_shelves:
    for j in all_products:
        gen = (k for k in all_segments if k.shelf == i.shelf)
        for k in gen:
            if (y_prev[int(k.seg)-1,int(j.prod)-1]>x_prev[int(i.shelf)-1,int(j.prod)-1]):
                print(y_prev[int(k.seg)-1,int(j.prod)-1])
                print(x_prev[int(i.shelf)-1,int(j.prod)-1])
                
# constraint 1h
for i in all_shelves:
    for j in all_products:
        gen = (k for k in all_segments if k.shelf == i.shelf)
        if (x_prev[int(i.shelf)-1,int(j.prod)-1] > sum(y_prev[int(k.seg)-1,int(j.prod)-1] for k in gen)):
            print("7")
            
# constraint 1i
for i in all_shelves:
    for j in all_products:
        gen1 = (k for k in all_segments if k.shelf == i.shelf and k.seg%3!=0)
        gen2 = (k for k in all_segments if k.shelf == i.shelf and k.seg%3!=1)
        gen_total = ((k1,k2) for k1 in gen1 for k2 in gen2 if k1.shelf==k2.shelf)
        for (k1,k2) in gen_total:
            if(q_prev[int(k1.seg)-1,int(j.prod)-1] < y_prev[int(k1.seg)-1,int(j.prod)-1] + y_prev[int(k2.seg)-1,int(j.prod)-1] - 1):
                print("8")
    
# constraint 1j
for i in all_shelves:
    gen1 = (k for k in all_segments if k.shelf == i.shelf and k.seg%3!=2)
    for k in gen1:
        if(sum(q_prev[int(k.seg)-1,int(j.prod)-1] for j in all_products)>1):
            print('9')

# constraint 1b
for j in all_products:
    if(sum(x_prev[int(i.shelf)-1,int(j.prod)-1] for i in all_shelves) > 1):
        print('10')
        
temp = ((k1,k2) for k1 in all_segments for k2 in all_segments if k1.seg<k2.seg and k1.shelf == k2.shelf)
R = ((k1,k2,j) for (k1,k2) in temp for j in all_products if ((k2.seg-k1.seg-1)*6>j.upper-2*j.minreq))
        
for (k1,k2,j) in R:
    if(y_prev[int(k1.seg)-1,int(j.prod)-1]+y_prev[int(k2.seg)-1,int(j.prod)-1]>1):
        print("11")
            
gen = ((k1,k2,k3) for k1 in all_segments for k2 in all_segments for k3 in all_segments if k1.shelf == k2.shelf == k3.shelf and k1.seg<k2.seg<k3.seg)
                # constraint 1f
for j in all_products:
    for (k1,k2,k3) in gen:
        if (k1,k3,j) not in R:
            if(s_prev[int(k2.seg)-1,int(j.prod)-1] < 6 * (y_prev[int(k1.seg)-1,int(j.prod)-1] + y_prev[int(k3.seg)-1,int(j.prod)-1] - 1)):
                print('12')
                
for (j1, j2) in L_array:
    for i in all_shelves:
        if(x_prev[int(i.shelf)-1,int(j1.prod)-1] + x_prev[int(i.shelf)-1,int(j2.prod)-1] > 1):
            print('13')
        
for (j1, j2) in H1_array:
    for i in all_shelves:
        if(x_prev[int(i.shelf)-1,int(j1.prod)-1] - x_prev[int(i.shelf)-1,int(j2.prod)-1] > 0):
            print('14')
    
for (j1, j2) in H1_array:
    for i in all_shelves:
        if(x_prev[int(i.shelf)-1,int(j1.prod)-1] - x_prev[int(i.shelf)-1,int(j2.prod)-1] < 0):
            print('15')
        
for (j1, j2) in H2_array:
    for i in all_shelves:
        if(x_prev[int(i.shelf)-1,int(j1.prod)-1] > x_prev[int(i.shelf)-1,int(j2.prod)-1]):
            print('16')
            
for (j1, j2) in H3_array:
    for i in all_shelves:
        if(x_prev[int(i.shelf)-1,int(j1.prod)-1] - x_prev[int(i.shelf)-1,int(j2.prod)-1] > 1 - z_prev[int(j1.prod)-1,int(j2.prod)-1]):
            print('17')
    
for (j1, j2) in H3_array:
    for i in all_shelves:
        if(x_prev[int(i.shelf)-1,int(j1.prod)-1] - x_prev[int(i.shelf)-1,int(j2.prod)-1] < -1 + z_prev[int(j1.prod)-1,int(j2.prod)-1]):
            print('18')
        
for (j1, j2) in H3_array:
    if(z_prev[int(j1.prod)-1,int(j2.prod)-1]>sum(x_prev[int(i.shelf)-1,int(j1.prod)-1] for i in all_shelves)):
        print('19')
    
        
for (j1, j2) in H3_array:
    if(z_prev[int(j1.prod)-1,int(j2.prod)-1]>sum(x_prev[int(i.shelf)-1,int(j2.prod)-1] for i in all_shelves)):
        print('20')
                
for (j1, j2) in H3_array:
    if(z_prev[int(j1.prod)-1,int(j2.prod)-1]>= sum(x_prev[int(i.shelf)-1,int(j2.prod)-1] for i in all_shelves) + sum(x_prev[int(i.shelf)-1,int(j1.prod)-1] for i in all_shelves) - 1):
        print('21')
