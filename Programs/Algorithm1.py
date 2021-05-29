#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 12:04:04 2021

@author: rickkessels
"""
import numpy as np
from SSP import SSP
import pyomo.environ as pyEnv
import ray

def algorithm_1(continuous_relaxation, model):
    
    # Initialize products
    
    model_algo1 = model.clone()
    model_algo1.S = pyEnv.Set()
    
    # Calculate sigma
    
    lmbd = np.zeros(len(model.B) + 1)
    for B in range(1,(len(model.B) + 1)):
        lmbd[B] = (continuous_relaxation.f_k[B*3]*continuous_relaxation.c_k[B*3]+continuous_relaxation.f_k[B*3-1]*continuous_relaxation.c_k[B*3-1]+continuous_relaxation.f_k[B*3-2]*continuous_relaxation.c_k[B*3-2]) / (continuous_relaxation.c_k[B*3]+continuous_relaxation.c_k[B*3-1]+continuous_relaxation.c_k[B*3-2])

    sigma = np.flip(np.argsort(lmbd))[:-1]
    
    r = np.zeros(len(model_algo1.B)+1)
    
    r_star = 0
    
    i = 0
    
    while (i != len(model_algo1.B) and len(model_algo1.S) != len(model.N)):
        model_algo1_instance = model_algo1.clone()
        
        # Step 2
        
        i_star = sigma[i]
        
        
        # Step 3
        
        res_SSP = SSP(model_algo1_instance, i_star)
        
        # Step 4
        
        l = list(res_SSP.w.keys())
        for k in l:
           if res_SSP.w[k]() != 0:
                model_algo1.S.add(k)
                
        model_algo1.N = model.N - model_algo1.S        
        
        r[i_star] = res_SSP.objective_SSP()
        r_star = r_star + res_SSP.objective_SSP()
        
        # Step 16
        
        i = i+1
    
    return r_star, r, model_algo1.x, model_algo1.y, model_algo1.s