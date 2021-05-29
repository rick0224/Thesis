
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from collections import namedtuple

from docplex.mp.model import Model

C_i = 18
c_k = 6

class TProds(namedtuple("Prod", ["prod", "lower", "upper", "profit", "minreq"])):
    def __str__(self):
        return self.name
    
class TShelf(namedtuple("Shelf", ["shelf"])):
    def __str__(self):
        return self.name    
    
class TSegs(namedtuple("Seg", ["seg", "shelf", "attr"])):
    def __str__(self):
        return self.name    


def build_problem_SSP(all_products, all_shelves, all_segments, **kwargs):
    
    mdl = Model(name='SSP', **kwargs)
    
    mdl.products = [TProds(*prod_row) for prod_row in all_products]
    mdl.shelves = [TShelf(*shelf_row) for shelf_row in all_shelves]
    mdl.segments = [TSegs(*seg_row) for seg_row in all_segments]
    
    all_products = mdl.products
    all_shelves = mdl.shelves
    all_segments = mdl.segments

    # --- decision variables ---
    mdl.w = mdl.binary_var_dict(all_products)
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
        mdl.add_constraint(j.lower * mdl.w[j] <= mdl.sum(mdl.s[k,j] for k in all_segments))
    
    # constraint 1d2
    for j in all_products:
        mdl.add_constraint(mdl.sum(mdl.s[k,j] for k in all_segments) <= j.upper * mdl.w[j])
    
        # constraint 1e1
    for j in all_products:
        for k in all_segments:
            mdl.add_constraint(j.minreq * mdl.y[k,j] <= mdl.s[k,j])
            
    # constraint 1e2
    for j in all_products:
        for k in all_segments:
            mdl.add_constraint(mdl.s[k,j] <= min(6, j.upper) * mdl.y[k,j]) 

            
 # constraint 1g
    for j in all_products:
        for k in all_segments:
            mdl.add_constraint(mdl.y[k,j] <= mdl.w[j])      

   # constraint 1h
    for j in all_products:
        for k in all_segments:
            mdl.add_constraint(mdl.w[j] <= mdl.sum(mdl.y[k,j]))
            
    # constraint 1i
    for j in all_products:
        gen1 = (k for k in all_segments if k.seg%3==1)
        gen2 = (k for k in all_segments if k.seg%3==2)
        gen_total = ((k1,k2) for k1 in gen1 for k2 in gen2)
        for (k1,k2) in gen_total:
            mdl.add_constraint(mdl.q[k1,j] >= mdl.y[k1,j] + mdl.y[k2,j]-1)
    
    # constraint 1j
    for i in all_shelves:
        gen1 = (k for k in all_segments if k.shelf == i.shelf and k.seg%3!=0)
        for k in gen1:
            mdl.add_constraint(mdl.sum(mdl.q[k,j] for j in all_products)<=1)
    
    temp = ((k1,k2) for k1 in all_segments for k2 in all_segments if k1.seg<k2.seg)
    R = ((k1,k2,j) for (k1,k2) in temp for j in all_products if ((k2.seg-k1.seg-1)*6>j.upper-2*j.minreq))

    # constraint 1f
    for j in all_products:
        for k1 in all_segments:
            for k2 in all_segments:
                for k3 in all_segments:
                    if (k1,k3,j) not in R:
                        if k1.seg < k2.seg < k3.seg:
                            mdl.add_constraint(mdl.s[k2,j] >= 6 * (mdl.y[k1,j] + mdl.y[k3,j] - 1))
    mdl.maximize(obj)
    
    return mdl

def solve_SSP(model, **kwargs):
    sol = model.solve(log_output=False, **kwargs)
    return sol