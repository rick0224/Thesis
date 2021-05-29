#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 15:11:55 2021

@author: rickkessels
"""

from Thesis_Repl_APSA import init, build_problem, solve
from Thesis_Repl_SSP import build_problem_SSP, solve_SSP
import numpy as np

PRODUCTS, SHELVES, SEGMENTS, lmbd = init()
model = build_problem(PRODUCTS, SHELVES, SEGMENTS, True)
solve(model)

sigma = np.flip(np.argsort(lmbd))
products = PRODUCTS
selected_products = []

r_star = []

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]

for i in sigma:
    if (len(products)==0):
        break
    shelf = [SHELVES[i]]
    segments = [SEGMENTS[i], SEGMENTS[i+1], SEGMENTS[i+2]]
    model2 = build_problem_SSP(products, shelf, segments)
    solve_SSP(model2)
    for j in model2.products:
        if (model2.w[j].solution_value==1):
            selected_products.append(j)
    print(len(selected_products))
    products = diff(model2.products, selected_products)
    r_star.append(model2.objective_value)

r = np.sum(r_star)

i_ar = []

tau = 4

tempset = SHELVES

count = 0

while (count < 5):
    
    while (len(tempset) > len(SHELVES) % tau):
        delta = np.flip(np.argsort(r_star))
        
        omega = np.round(len(delta)/tau)
        
        for k in range(1, tau+1):
            i = int(np.round(np.floor(np.random.uniform(((k-1)*omega+1),k*omega+1)),0))
            for l in model2.products:
                if (i not in i_ar):
                    if (i == l.prod):
                        i_ar.append(l) 
            
        b_set = []   
        for j in range(1,len(model.B)+1):
            for l in model2.products:
                if (j == l.prod and l.prod not in i_ar and l.prod not in b_set):
                    b_set.append(l)
        
        # tempset = b_set
        
        model_APSA = build_problem(PRODUCTS, tempset, SEGMENTS)
        solve(model_APSA)
        
        r_star_prev = r_star
        r_star = model_APSA.objective_value()
        
        x = model_APSA.x
        y = model_APSA.y
        s = model_APSA.s
        
        count = count + 1
        
        
        
        
            