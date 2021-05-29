#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 11:31:36 2021

@author: rickkessels
"""

import pyomo.environ as pyEnv
import numpy as np

def init(n, f_max, m):
    
    model = pyEnv.ConcreteModel()
    
    # There are three segments per shelf
    seg = m * 3
    
    model.N = pyEnv.RangeSet(n)
    model.F = pyEnv.RangeSet(f_max)
    model.I = pyEnv.RangeSet(f_max+1,n)
    
    model.B = pyEnv.RangeSet(1,m)
    model.K = pyEnv.RangeSet(1,seg)
      
    model.C_i = pyEnv.Param(model.B, initialize=18)
    model.c_k = pyEnv.Param(model.K, initialize=6)
    model.c_max = pyEnv.Param(initialize=6)
    model.phi_small = pyEnv.Param(model.N, initialize=0.1)

    ell = [0]
    u = [0]
    phi_cap = [0]

    for j in model.N:
        rnd = np.round(np.random.uniform(1,3))
        ell.append(rnd)
        rnd2 = np.round(np.random.uniform(rnd,6))
        u.append(rnd2)
        rnd3 = np.round(np.random.uniform(1,25),2)
        phi_cap.append(rnd3)
        
        
    f_k = np.zeros(seg+1)
    count = 0
    for k in model.K:
        rnd4 = int(np.random.uniform(0,5))
        t = 0.05 + rnd4*0.20
        if (count==1):
            f = np.random.uniform(t, t+0.05)
        else:
            f = np.random.uniform(t+0.06, t+0.10)
        f_k[k] = f
        
    model.ell = pyEnv.Param(model.N, initialize=lambda model, j: ell[j])
    model.u = pyEnv.Param(model.N, initialize=lambda model, j: u[j])
    
    model.phi_cap = pyEnv.Param(model.N, initialize=lambda model, j: phi_cap[j])
    model.f_k = pyEnv.Param(model.K, initialize=lambda model, k: f_k[k])
        
    return model

def model_selection(model, cont):
    if (cont==True):
        model.x = pyEnv.Var(model.B, model.N, within=pyEnv.NonNegativeReals, bounds=(0,1))
        model.y = pyEnv.Var(model.K, model.N, within=pyEnv.NonNegativeReals, bounds=(0,1))
        model.s = pyEnv.Var(model.K, model.N, within=pyEnv.NonNegativeReals)
        model.z = pyEnv.Var(model.N, model.N, within=pyEnv.NonNegativeReals, bounds=(0,1))
        model.q = pyEnv.Var(model.K, model.N, within=pyEnv.NonNegativeReals, bounds=(0,1))
    else:
        model.x = pyEnv.Var(model.B, model.N, within=pyEnv.Binary)
        model.y = pyEnv.Var(model.K, model.N, within=pyEnv.Binary)
        model.s = pyEnv.Var(model.K, model.N, within=pyEnv.NonNegativeReals)
        model.z = pyEnv.Var(model.N, model.N, within=pyEnv.Binary)
        model.q = pyEnv.Var(model.K, model.N, within=pyEnv.Binary)
    
    return model        
        
def calc(model):
    
    model.temp = pyEnv.Var(model.B, within=pyEnv.NonNegativeReals)
    def obj_func(model):
        return sum(model.phi_cap[j] * (model.f_k[k] * model.s[k,j])/model.c_k[k] for k in model.K for j in model.N)
    
    model.objective = pyEnv.Objective(rule=obj_func,sense=pyEnv.maximize)
    
    def rule_const1(model,N):
        return sum(model.x[i,N] for i in model.B) <= 1
    
    model.const1 = pyEnv.Constraint(model.N,rule=rule_const1)
    
    def rule_const2(model,K):
        return sum(model.s[K,j] for j in model.N) <= model.c_k[K]
    
    model.const2 = pyEnv.Constraint(model.K,rule=rule_const2)
    
    def rule_const3A(model,N):
        return (model.ell[N] * sum(model.x[i,N] for i in model.B)) <= sum(model.s[k,N] for k in model.K) #<= (model.u[N] * sum(model.x[i,N] for i in model.B))
    
    model.const3A = pyEnv.Constraint(model.N,rule=rule_const3A)
    
    def rule_const3B(model,N):
        return sum(model.s[k,N] for k in model.K) <= (model.u[N] * sum(model.x[i,N] for i in model.B))
    
    model.const3B = pyEnv.Constraint(model.N,rule=rule_const3B)
    
    def rule_const4A(model,N,K):
        return model.phi_small[N] * model.y[K,N] <= model.s[K,N]
    
    model.const4A = pyEnv.Constraint(model.N, model.K,rule=rule_const4A)
    
    def rule_const4B(model,N,K):
        return model.s[K,N] <= min(model.c_k[K], model.u[N]) * model.y[K,N]
    
    model.const4B = pyEnv.Constraint(model.N, model.K,rule=rule_const4B)
    
    def rule_const5A(model,N,B,K):
        if K==B*3:
            return model.s[K-1,N] >= model.c_k[K-1] * (model.y[K-2,N]+model.y[K,N]-1)
        else:
            return (model.temp[B]==1)
    
    model.const5A = pyEnv.Constraint(model.N,model.B, model.K,rule=rule_const5A)
    
    def rule_const6(model,N,B,K):
        if K==B*3 or K==B*3-1 or K==B*3-2:
            return (model.y[K,N] <= model.x[B,N])
        else:
            return (model.temp[B]==1)
    
    model.const6 = pyEnv.Constraint(model.N,model.B,model.K,rule=rule_const6)
    
    def rule_const7(model,N,B,K):
        if K==B*3:
            return model.x[B,N] <= model.y[K,N]+model.y[K-1,N]+model.y[K-2,N]
        else:
            return (model.temp[B]==1)
    
    model.const7 = pyEnv.Constraint(model.N,model.B,model.K,rule=rule_const7)
    
    def rule_const8(model,N,B,K):
        if K==B*3-1 or K==B*3-2:
            return model.q[K,N] >= model.y[K,N] + model.y[K+1,N] - 1
        else:
            return (model.temp[B]==1)
    
    model.const8 = pyEnv.Constraint(model.N,model.B,model.K,rule=rule_const8)
    
    def rule_const9(model,B,K):
        if K==B*3-1 or K==B*3-2:
            return sum(model.q[K,j] for j in model.N) <= 1
        else:
            return (model.temp[B]==1)
    
    model.const9 = pyEnv.Constraint(model.B,model.K,rule=rule_const9)
    
    #Solves
    solver = pyEnv.SolverFactory('cplex_direct')
    solver.options['timelimit'] = 3600
    result = solver.solve(model)
    
    #Prints the results
    print(result)
    
    l = list(model.y.keys())
    for k in l:
       if model.s[k]() != 0:
            print(k,'--', model.s[k]())
            
    return model        
    
    