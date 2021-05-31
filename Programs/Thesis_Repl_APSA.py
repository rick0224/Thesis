# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

from collections import namedtuple

from docplex.mp.model import Model

import numpy as np

from itertools import tee

np.random.seed(1234)

C_i = 18
c_k = 6

N = 240
B = 30
K = B * 3

    
def init():
    
    ell = []
    u = []
    phi_cap = []
    N_array = []
    phi_small = []
    
    B_array = []
    
    f_k = []
    K_array = []
    shelf_seg = []
    
    lmbd = []
    numerator = 0
    denominator = 0
    
    for j in range(1,N+1):
        temp = np.round(np.random.uniform(1,C_i/6.0))
        ell.append(temp)
        temp_2 = np.round(np.random.uniform(temp, 6.0))
        u.append(temp_2)
        temp_3 = np.round(np.random.uniform(1,25),2)
        phi_cap.append(temp_3)
        N_array.append(j)
        phi_small.append(0.1)
        
    for i in range(1,B+1):
        B_array.append(i)
        
    for k in range(1,K+1):
        if (k<K/5.0):
            if (k%3==2):
                f_k_instance=np.random.uniform(0.05, 0.10)
            else:
                f_k_instance=np.random.uniform(0.11, 0.15)
        elif (k<2*K/5.0):
            if (k%3==2):
                f_k_instance=np.random.uniform(0.25, 0.30)
            else:
                f_k_instance=np.random.uniform(0.31, 0.35)            
        elif (k<3*K/5.0): 
            if (k%3==2):
                f_k_instance=np.random.uniform(0.45, 0.50)
            else:
                f_k_instance=np.random.uniform(0.51, 0.55)  
            
        elif (k<4*K/5.0):
            if (k%3==2):
                f_k_instance=np.random.uniform(0.65, 0.70)
            else:
                f_k_instance=np.random.uniform(0.71, 0.75)  
            
        else:
            if (k%3==2):
                f_k_instance=np.random.uniform(0.85, 0.90)
            else:
                f_k_instance=np.random.uniform(0.91, 0.95)  

        f_k.append(f_k_instance)
        shelf_seg.append(np.ceil(k/3.0))
        K_array.append(k)
        numerator = numerator + f_k_instance*c_k
        denominator = denominator + c_k
        if (k%3==0):
            lmbd.append(numerator/denominator)
            numerator = 0
            denominator = 0
        
    PRODUCTS = np.column_stack((N_array, ell, u, phi_cap, phi_small))
    SHELVES = np.column_stack(([B_array]))
    SEGMENTS = np.column_stack((K_array, shelf_seg,f_k))
    
    L = []
    H1 = []
    H2 = []
    H3 = []
    
    count = 0
    
    while count < 5:
        
        prod_1 = np.floor(np.random.uniform(0,N))
        prod_2 = np.floor(np.random.uniform(0,N))
        while (prod_1 == prod_2):
            prod_2 = np.floor(np.random.uniform(0,N))
        
        L.append((PRODUCTS[int(prod_1)],PRODUCTS[int(prod_2)]))
        
        prod_1 = np.floor(np.random.uniform(0,N))
        prod_2 = np.floor(np.random.uniform(0,N))
        while (prod_1 == prod_2):
            prod_2 = np.floor(np.random.uniform(0,N))
        
        H1.append((PRODUCTS[int(prod_1)],PRODUCTS[int(prod_2)]))
        
        prod_1 = np.floor(np.random.uniform(0,N))
        prod_2 = np.floor(np.random.uniform(0,N))
        while (prod_1 == prod_2):
            prod_2 = np.floor(np.random.uniform(0,N))
        
        H2.append((PRODUCTS[int(prod_1)],PRODUCTS[int(prod_2)]))
        
        prod_1 = np.floor(np.random.uniform(0,N))
        prod_2 = np.floor(np.random.uniform(0,N))
        while (prod_1 == prod_2):
            prod_2 = np.floor(np.random.uniform(0,N))
        
        H3.append((PRODUCTS[int(prod_1)],PRODUCTS[int(prod_2)]))   
        
        count = count + 1
             
    return PRODUCTS, SHELVES, SEGMENTS, lmbd, L, H1, H2, H3

class TProds(namedtuple("Prod", ["prod", "lower", "upper", "profit", "minreq"])):
    def __str__(self):
        return self.name
    
class TShelf(namedtuple("Shelf", ["shelf"])):
    def __str__(self):
        return self.name    
    
class TSegs(namedtuple("Seg", ["seg", "shelf", "attr"])):
    def __str__(self):
        return self.name    


def build_problem(products, shelves, segments, rel, first, ineq2, ineq3,SSP,L,H1,H2,H3,L_dummy, H1_dummy, H2_dummy, H3_dummy,products_total,x=0,y=0,s=0,q=0,z=0,**kwargs):
    
    mdl = Model(name='APSA', **kwargs)
    
    mdl.products = products
    mdl.segments = segments
    
    mdl.products = [TProds(*prod_row) for prod_row in products]
    mdl.segments = [TSegs(*seg_row) for seg_row in segments]
    mdl.shelves = [TShelf(*shelf_row) for shelf_row in shelves]
    
    mdl.products_total = products_total
    mdl.products_total = [TProds(*prod_row) for prod_row in products_total]
    
    all_products = mdl.products
    all_shelves = mdl.shelves
    all_segments = mdl.segments
    
    all_products_total = mdl.products_total
    
    L_array = []
    H1_array = []
    H2_array = []
    H3_array = []
    
    for j1 in all_products:
        for j2 in all_products:
            for Z in L:
                if (j1.prod ==  Z[0][0] and j2.prod==Z[1][0]):
                    L_array.append((j1,j2))
                if (j2.prod ==  Z[0][0] and j1.prod==Z[1][0]):
                    L_array.append((j1,j2))
            for Z in H1:
                if (j1.prod ==  Z[0][0] and j2.prod==Z[1][0]):
                    H1_array.append((j1,j2))  
                if (j2.prod ==  Z[0][0] and j1.prod==Z[1][0]):
                    H1_array.append((j1,j2)) 
            for Z in H2:
                if (j1.prod ==  Z[0][0] and j2.prod==Z[1][0]):
                    H2_array.append((j1,j2))
            for Z in H3:
                if (j1.prod ==  Z[0][0] and j2.prod==Z[1][0]):
                    H3_array.append((j1,j2))
                if (j2.prod ==  Z[0][0] and j1.prod==Z[1][0]):
                    H3_array.append((j1,j2))
    
    # --- decision variables ---
    if (rel==True):
        mdl.x = mdl.continuous_var_matrix(all_shelves, all_products, 0, 1)
        mdl.y = mdl.continuous_var_matrix(all_segments, all_products, 0, 1)
        mdl.s = mdl.continuous_var_matrix(all_segments, all_products)
        mdl.z = mdl.continuous_var_matrix(all_products, all_products, 0, 1)
        mdl.q = mdl.continuous_var_matrix(all_segments, all_products, 0, 1)
    else:
        mdl.x = mdl.binary_var_matrix(all_shelves, all_products)
        mdl.y = mdl.binary_var_matrix(all_segments, all_products)
        mdl.s = mdl.continuous_var_matrix(all_segments, all_products)
        mdl.z = mdl.binary_var_matrix(all_products, all_products)
        mdl.q = mdl.binary_var_matrix(all_segments, all_products)
        
    # --- objective ---
    obj = mdl.sum(mdl.sum(j[3]* k[2] * mdl.s[k,j] / c_k for k in all_segments) for j in all_products)
    
    # --- constraints ---
        
    # constraint 1c
    for k in all_segments:
        mdl.add_constraint(mdl.sum(mdl.s[k,j] for j in all_products)<= 6)
            
    # constraint 1d1
    for j in all_products:
        mdl.add_constraint(j.lower * mdl.sum(mdl.x[i,j] for i in all_shelves) <= mdl.sum(mdl.s[k,j] for k in all_segments))
    
    # constraint 1d2
    for j in all_products:
        mdl.add_constraint(mdl.sum(mdl.s[k,j] for k in all_segments) <= j.upper * mdl.sum(mdl.x[i,j] for i in all_shelves))
        
    # constraint 1e1
    for j in all_products:
        for k in all_segments:
            mdl.add_constraint(j.minreq * mdl.y[k,j] <= mdl.s[k,j])
            
    # constraint 1e2
    for j in all_products:
        for k in all_segments:
            mdl.add_constraint(mdl.s[k,j] <= min(c_k, j.upper) * mdl.y[k,j]) 
            
    # constraint 1g
    for i in all_shelves:
        for j in all_products:
            gen = (k for k in all_segments if k.shelf == i.shelf)
            for k in gen:
                mdl.add_constraint(mdl.y[k,j] <= mdl.x[i,j])     
                
   # constraint 1h
    for i in all_shelves:
        for j in all_products:
            gen = (k for k in all_segments if k.shelf == i.shelf)
            mdl.add_constraint(mdl.x[i,j] <= mdl.sum(mdl.y[k,j] for k in gen))
            
    # constraint 1i
    for i in all_shelves:
        for j in all_products:
            gen1 = (k for k in all_segments if k.shelf == i.shelf and k.seg%3!=0)
            gen2 = (k for k in all_segments if k.shelf == i.shelf and k.seg%3!=1)
            gen_total = ((k1,k2) for k1 in gen1 for k2 in gen2 if k1.shelf==k2.shelf)
            for (k1,k2) in gen_total:
                mdl.add_constraint(mdl.q[k1,j] >= mdl.y[k1,j] + mdl.y[k2,j] - 1)
    
    # constraint 1j
    for i in all_shelves:
        gen1 = (k for k in all_segments if k.shelf == i.shelf and k.seg%3!=2)
        for k in gen1:
            mdl.add_constraint(mdl.sum(mdl.q[k,j] for j in all_products)<=1)

    # constraint 1b
    for j in all_products:
        mdl.add_constraint(mdl.sum(mdl.x[i,j] for i in all_shelves) <= 1)
        
    if (ineq2==True):
        temp = ((k1,k2) for k1 in all_segments for k2 in all_segments if k1.seg<k2.seg and k1.shelf == k2.shelf)
        R = ((k1,k2,j) for (k1,k2) in temp for j in all_products if ((k2.seg-k1.seg-1)*6>j.upper-2*j.minreq))
        
        for (k1,k2,j) in R:
            mdl.add_constraint(mdl.y[k1,j]+mdl.y[k2,j]<=1)
            
        if (ineq3==True):
            
            gen = ((k1,k2,k3) for k1 in all_segments for k2 in all_segments for k3 in all_segments if k1.shelf == k2.shelf == k3.shelf and k1.seg<k2.seg<k3.seg)
                # constraint 1f
            for j in all_products:
                for (k1,k2,k3) in gen:
                    if (k1,k3,j) not in R:
                        mdl.add_constraint(mdl.s[k2,j] >= 6 * (mdl.y[k1,j] + mdl.y[k3,j] - 1))
    if (L_dummy==True):
        for (j1, j2) in L_array:
            for i in all_shelves:
                mdl.add_constraint(mdl.x[i,j1] + mdl.x[i,j2] <= 1)
                    
    if (H1_dummy==True):
        for (j1, j2) in H1_array:
            for i in all_shelves:
                mdl.add_constraint(mdl.x[i,j1] - mdl.x[i,j2] <= 0) 
                    
        for (j1, j2) in H1_array:
            for i in all_shelves:
                mdl.add_constraint(mdl.x[i,j1] - mdl.x[i,j2] >= 0) 
                    
    if (H2_dummy==True): 
        for (j1, j2) in H2_array:
            for i in all_shelves:
                mdl.add_constraint(mdl.x[i,j1] <= mdl.x[i,j2])  
  
    if (SSP==False):
        if (H3_dummy==True):
            for (j1, j2) in H3_array:
                for i in all_shelves:
                    mdl.add_constraint(mdl.x[i,j1] - mdl.x[i,j2] <= 1 - mdl.z[j1,j2])   

            for (j1, j2) in H3_array:
                for i in all_shelves:
                    mdl.add_constraint(mdl.x[i,j1] - mdl.x[i,j2] >= -1 + mdl.z[j1,j2])
        
            for (j1, j2) in H3_array:
                mdl.add_constraint(mdl.z[j1,j2]<=mdl.sum(mdl.x[i,j1] for i in all_shelves))
 
            for (j1, j2) in H3_array:
                mdl.add_constraint(mdl.z[j1,j2]<=mdl.sum(mdl.x[i,j2] for i in all_shelves))
            
            for (j1, j2) in H3_array:
                mdl.add_constraint(mdl.z[j1,j2] >= mdl.sum(mdl.x[i,j1] for i in all_shelves) + mdl.sum(mdl.x[i,j2] for i in all_shelves) - 1)

    mdl.maximize(obj)
    
    if (first==False):
        warmstart=mdl.new_solution()
        for j in mdl.products:
            for k in mdl.segments:
                warmstart.add_var_value(mdl.y[k,j],y[int(k.seg)-1,int(j.prod)-1])
                warmstart.add_var_value(mdl.s[k,j],s[int(k.seg)-1,int(j.prod)-1])
                warmstart.add_var_value(mdl.q[k,j],q[int(k.seg)-1,int(j.prod)-1])
            for i in mdl.shelves:
                warmstart.add_var_value(mdl.x[i,j],x[int(i.shelf)-1,int(j.prod)-1])
            for j2 in mdl.products:
                warmstart.add_var_value(mdl.z[j,j2],z[int(j.prod)-1,int(j2.prod)-1])
                
        mdl.add_mip_start(warmstart)    
    
    return mdl, L_array, H1_array, H2_array, H3_array

def solve(model, **kwargs):
    #model.parameters.timelimit = 
    model.parameters.mip.tolerances.absmipgap = 1e-7
    sol = model.solve(log_output=True, **kwargs)
    return sol

def haha(model, **kwargs):
    obj_array = np.zeros((K))
    obj_array_shelf = np.zeros((K))
    
    obj2=0
    
    for k in model.segments:
        obj2 = sum((j[3]* k[2] * model.s[k,j].solution_value / c_k) for j in model.products)
        obj_array[int(k.seg)-1] = obj2
    
    for i in model.shelves:
        obj_array_shelf[int(i.shelf)-1] =  sum(sum((j[3]* k[2] * model.s[k,j].solution_value / c_k) for k in model.segments if k.shelf==i.shelf) for j in model.products)
        
    return obj_array, obj_array_shelf