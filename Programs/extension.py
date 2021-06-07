# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

from collections import namedtuple
from docplex.mp.model import Model
import numpy as np
from itertools import tee

np.random.seed(42)
 
def init(N, B, c_k, C_i):
    
    K = B * 3
    
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
        if (k<=K/5.0):
            if (k%3==2):
                f_k_instance=np.random.uniform(0.05, 0.10)
            else:
                f_k_instance=np.random.uniform(0.11, 0.15)
        elif (k<=2*K/5.0):
            if (k%3==2):
                f_k_instance=np.random.uniform(0.25, 0.30)
            else:
                f_k_instance=np.random.uniform(0.31, 0.35)            
        elif (k<=3*K/5.0): 
            if (k%3==2):
                f_k_instance=np.random.uniform(0.45, 0.50)
            else:
                f_k_instance=np.random.uniform(0.51, 0.55)  
            
        elif (k<=4*K/5.0):
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
    P = []
    Q = []
    R = []
    S = []
    
    count = 0
    
    products_chosen = []

    while count < 5:
        
        chosen = True
        while (chosen == True):
            prod_1 = np.floor(np.random.uniform(0,N))
            prod_2 = np.floor(np.random.uniform(0,N))
            
            while (prod_1 == prod_2):
                prod_2 = np.floor(np.random.uniform(0,N))
            
            if (prod_1 not in products_chosen and prod_2 not in products_chosen):
                chosen = False
                products_chosen.append(prod_1)
                products_chosen.append(prod_2)
        
        L.append((PRODUCTS[int(prod_1)],PRODUCTS[int(prod_2)]))
        
        chosen = True
        while (chosen == True):
            prod_1 = np.floor(np.random.uniform(0,N))
            prod_2 = np.floor(np.random.uniform(0,N))
            while (prod_1 == prod_2):
                prod_2 = np.floor(np.random.uniform(0,N))
                
            if (prod_1 not in products_chosen and prod_2 not in products_chosen):
                chosen = False    
                products_chosen.append(prod_1)
                products_chosen.append(prod_2)
        
        H1.append((PRODUCTS[int(prod_1)],PRODUCTS[int(prod_2)]))
        
        chosen = True
        while (chosen == True):
            prod_1 = np.floor(np.random.uniform(0,N))
            prod_2 = np.floor(np.random.uniform(0,N))
            while (prod_1 == prod_2):
                prod_2 = np.floor(np.random.uniform(0,N))
            
            if (prod_1 not in products_chosen and prod_2 not in products_chosen):
                chosen = False   
                products_chosen.append(prod_1)
                products_chosen.append(prod_2)
                
        H2.append((PRODUCTS[int(prod_1)],PRODUCTS[int(prod_2)]))
        
        chosen = True
        
        while (chosen == True):
            prod_1 = np.floor(np.random.uniform(0,N))
            prod_2 = np.floor(np.random.uniform(0,N))
            while (prod_1 == prod_2):
                prod_2 = np.floor(np.random.uniform(0,N))
        
            if (prod_1 not in products_chosen and prod_2 not in products_chosen):
                chosen = False  
                products_chosen.append(prod_1)
                products_chosen.append(prod_2)
                
        H3.append((PRODUCTS[int(prod_1)],PRODUCTS[int(prod_2)]))   
        
        chosen = True
        
        while (chosen == True):
            prod_1 = np.floor(np.random.uniform(0,N))
      
            if (prod_1 not in products_chosen):
                chosen = False  
                products_chosen.append(prod_1)
                
        P.append((PRODUCTS[int(prod_1)]))   
        
        chosen = True
        
        while (chosen == True):
            prod_1 = np.floor(np.random.uniform(0,N))

            if (prod_1 not in products_chosen):
                chosen = False  
                products_chosen.append(prod_1)
                
        Q.append((PRODUCTS[int(prod_1)]))           
        
        for k in range(1,K+1):
            if (k>3*K/5.0):
                S.append((SEGMENTS[int(k-1)]))   
        
        count = count + 1
             
    return PRODUCTS, SHELVES, SEGMENTS, lmbd, L, H1, H2, H3, P, Q, R, S

class TProds(namedtuple("Prod", ["prod", "lower", "upper", "profit", "minreq"])):
    def __str__(self):
        return self.name
    
class TShelf(namedtuple("Shelf", ["shelf"])):
    def __str__(self):
        return self.name    
    
class TSegs(namedtuple("Seg", ["seg", "shelf", "attr"])):
    def __str__(self):
        return self.name    


def build_problem(products, shelves, segments, relaxation, first, ineq2, ineq3, SSP, L, H1, H2, H3, L_dummy, H1_dummy, H2_dummy, H3_dummy, P_ar, Q_ar, R_ar, S_ar, CS1, CS2, CS3, CS4, CS5, products_total, c_k, x=0, y=0, s=0, q=0, z=0, **kwargs):
    
    # Initializing a model
    mdl = Model(name='APSA', **kwargs)
    
    if (CS5==True):
        for j in range(0,len(P_ar)):
            P_ar[j][1]=3
            P_ar[j][2]=6

    # Storing all "current" products, segments, shelves, and total products in sets that the model can utilize later.
    mdl.products = [TProds(*prod_row) for prod_row in products]
    mdl.segments = [TSegs(*seg_row) for seg_row in segments]
    mdl.shelves = [TShelf(*shelf_row) for shelf_row in shelves]
    mdl.products_total = [TProds(*prod_row) for prod_row in products_total]
    
    # For simplicity, we're storing the sets into variables.
    all_products = mdl.products
    all_shelves = mdl.shelves
    all_segments = mdl.segments
    
    # Initializing empty arrays that we can store the products in later.
    L_array = []
    H1_array = []
    H2_array = []
    H3_array = []
    P_array = []
    Q_array = []
    R_array = []
    S_array = []
    
    # Going through all product(s) (combinations) to store these into the right arrays.
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
    
    P_ar = np.array(P_ar)
    Q_ar = np.array(Q_ar)
    for j1 in all_products:                
        for h in range(0,len(P_ar)):
            if (j1.prod == P_ar[h][0]):
                P_array.append(j1)
        for h in range(0,len(Q_ar)):
            if (j1.prod == Q_ar[h][0]):
                Q_array.append(j1)
                
    S_ar = np.array(S_ar)
    R_ar = np.array(R_ar)
    # Storing the high-attraction shelves and low-attraction shelves in the R_array and S_array respectively.            
    for j1 in all_segments:
        for h in range(0,len(R_ar)):
            if (j1.seg == R_ar[h][0]):
                R_array.append(j1)       
        for h in range(0,len(S_ar)):
            if (j1.seg == S_ar[h][0]):
                S_array.append(j1)
                
    # --- decision variables ---
    if (relaxation==True): # If we need to do a relaxation, we want to make all binary variables continuous between 0 and 1.
        mdl.x = mdl.continuous_var_matrix(all_shelves, all_products, 0, 1)
        mdl.y = mdl.continuous_var_matrix(all_segments, all_products, 0, 1)
        mdl.s = mdl.continuous_var_matrix(all_segments, all_products)
        mdl.z = mdl.continuous_var_matrix(all_products, all_products, 0, 1)
        mdl.q = mdl.continuous_var_matrix(all_segments, all_products, 0, 1)
    else: # If no relaxation is required, we just want to keep the variables in the same "shape" as they are supposed to.
        mdl.x = mdl.binary_var_matrix(all_shelves, all_products)
        mdl.y = mdl.binary_var_matrix(all_segments, all_products)
        mdl.s = mdl.continuous_var_matrix(all_segments, all_products)
        mdl.z = mdl.binary_var_matrix(all_products, all_products)
        mdl.q = mdl.binary_var_matrix(all_segments, all_products)
        
    # --- objective function ---
    obj = mdl.sum(mdl.sum(j[3]* k[2] * mdl.s[k,j] / c_k for k in all_segments) for j in all_products)
    
    
    # --- constraints ---
    
    # constraint 1b
    if (CS4==True): # If the fourth health-related constraint needs to be added, we adjust constraint 1b a bit.
        for j in all_products:
            if j not in P_array:
                mdl.add_constraint(mdl.sum(mdl.x[i,j] for i in all_shelves) <= 1)
            else:
                mdl.add_constraint(mdl.sum(mdl.x[i,j] for i in all_shelves) <= 3)  
                
    else: # Else we just keep the original constraint formulation
        for j in all_products:
            mdl.add_constraint(mdl.sum(mdl.x[i,j] for i in all_shelves) <= 1)                   
                   
    # constraint 1c
    for k in all_segments:
        mdl.add_constraint(mdl.sum(mdl.s[k,j] for j in all_products)<= c_k)
            
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
    
    temp = ((k1,k2) for k1 in all_segments for k2 in all_segments if k1.seg<k2.seg and k1.shelf == k2.shelf)
    gen = ((k1,k2,k3) for k1 in all_segments for k2 in all_segments for k3 in all_segments if k1.shelf == k2.shelf == k3.shelf and k1.seg<k2.seg<k3.seg)
    R = ((k1,k2,j) for (k1,k2) in temp for j in all_products if ((k2.seg-k1.seg-1)*6>j.upper-2*j.minreq))                      
                 
    # constraint 1f              
    if (ineq3==True):
        for j in all_products:
            for (k1,k2,k3) in gen:
                if (k1,k3,j) not in R:
                    mdl.add_constraint(mdl.s[k2,j] >= c_k * (mdl.y[k1,j] + mdl.y[k3,j] - 1))
    else:
        for j in all_products:
            for (k1,k2,k3) in gen:
                mdl.add_constraint(mdl.s[k2,j] >= c_k * (mdl.y[k1,j] + mdl.y[k3,j] - 1))             
            
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
            gen_total = ((k1,k2) for k1 in gen1 for k2 in gen2 if k1.shelf==k2.shelf and k1.seg<k2.seg)
            for (k1,k2) in gen_total:
                mdl.add_constraint(mdl.q[k1,j] >= mdl.y[k1,j] + mdl.y[k2,j] - 1)
    
    # constraint 1j
    for i in all_shelves:
        gen1 = (k for k in all_segments if k.shelf == i.shelf and k.seg%3!=2)
        for k in gen1:
            mdl.add_constraint(mdl.sum(mdl.q[k,j] for j in all_products)<=1)

    if (ineq2==True):
        temp = ((k1,k2) for k1 in all_segments for k2 in all_segments if k1.seg<k2.seg and k1.shelf == k2.shelf)
        R = ((k1,k2,j) for (k1,k2) in temp for j in all_products if ((k2.seg-k1.seg-1)*6>j.upper-2*j.minreq))
        
        for (k1,k2,j) in R:
            mdl.add_constraint(mdl.y[k1,j]+mdl.y[k2,j]<=1)
            
    if (L_dummy == True): # If we want to include the affinity matrix L into the model.
        
        # constraint 1k
        for (j1, j2) in L_array:
            for i in all_shelves:
                mdl.add_constraint(mdl.x[i,j1] + mdl.x[i,j2] <= 1)

                    
    if (H1_dummy==True): # If we want to include the affinity matrix H1 into the model.
        
        # constraint 1l
        for (j1, j2) in H1_array:
            for i in all_shelves:
                mdl.add_constraint(mdl.x[i,j1] - mdl.x[i,j2] <= 0) 
                    
        for (j1, j2) in H1_array:
            for i in all_shelves:
                mdl.add_constraint(mdl.x[i,j1] - mdl.x[i,j2] >= 0) 
 
                   
    if (H2_dummy==True): # If we want to include the affinity matrix H2 into the model.
        
        # constraint 1m
        for (j1, j2) in H2_array:
            for i in all_shelves:
                mdl.add_constraint(mdl.x[i,j1] <= mdl.x[i,j2])  

  
    if (SSP==False): # We don't include any constraints on H3 when we're doing the SSP model.
       
        if (H3_dummy==True): # However, if we do not do the SSP model, and we want to include the affinity matrix H3 into the model...
            
            # constraint 1n
            for (j1, j2) in H3_array:
                for i in all_shelves:
                    mdl.add_constraint(mdl.x[i,j1] - mdl.x[i,j2] <= 1 - mdl.z[j1,j2])   
            
            # constraint 1o
            for (j1, j2) in H3_array:
                for i in all_shelves:
                    mdl.add_constraint(mdl.x[i,j1] - mdl.x[i,j2] >= -1 + mdl.z[j1,j2])
            
            # constraint 1p
            for (j1, j2) in H3_array:
                mdl.add_constraint(mdl.z[j1,j2]<=mdl.sum(mdl.x[i,j1] for i in all_shelves))
            
            # constraint 1q
            for (j1, j2) in H3_array:
                mdl.add_constraint(mdl.z[j1,j2]<=mdl.sum(mdl.x[i,j2] for i in all_shelves))
            
            # constraint 1r
            for (j1, j2) in H3_array:
                mdl.add_constraint(mdl.z[j1,j2] >= mdl.sum(mdl.x[i,j1] for i in all_shelves) + mdl.sum(mdl.x[i,j2] for i in all_shelves) - 1)

    if (CS1 == True):           
        for j in P_array:
            for k in all_segments:
                if k not in S_array:
                    mdl.add_constraint(mdl.y[k,j]>=0)
                    mdl.add_constraint(mdl.y[k,j]<=0)

    if (CS2 == True):            
        for j in P_array:
            mdl.add_constraint(mdl.sum(mdl.y[k,j] for k in S_array) >= 1)
    
    if (CS3 == True):
        for j in Q_array:
            for k in S_array:
                    mdl.add_constraint(mdl.y[k,j]>=0)
                    mdl.add_constraint(mdl.y[k,j]<=0)
                
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
    
    return mdl, L_array, H1_array, H2_array, H3_array, P_array, Q_array, R_array, S_array

def solve(model, time_limit=3600, **kwargs):
    model.parameters.timelimit = time_limit
    model.parameters.mip.tolerances.absmipgap = 1e-7
    sol = model.solve(log_output=True, **kwargs)
    return sol

from cplex._internal._subinterfaces import CutType

def get_cut_stats(mdl):
    """ Computes a dicitonary of cut name -> number of cuts used
    Args:
        mdl: an instance of `docplex.mp.Model`
    Returns:
        a dictionary of string -> int,, from cut type to number used (nonzero).
        Unused cut types ar enot mentioned
    Example:
        For delivered model "nurses"
        # {'cover': 88, 'GUB_cover': 9, 'flow_cover': 6, 'fractional': 5, 'MIR': 9, 'zero_half': 9, 'lift_and_project': 5}
    """
    cut_stats = {}
    cpx = mdl.cplex
    cut_type_instance = CutType()
    summation = 0
    for ct in cut_type_instance:
        num = cpx.solution.MIP.get_num_cuts(ct)
        summation = summation + num
        
        if num:
            cutname = cut_type_instance[ct]
            cut_stats[cutname] = num

    return summation