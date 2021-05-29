#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 15:07:01 2021

@author: rickkessels
"""

import pyomo.environ as pyEnv

def APSA(model):
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
            return (model.y[K,N]>=0)
    
    model.const5A = pyEnv.Constraint(model.N,model.B, model.K,rule=rule_const5A)
    
    def rule_const6(model,N,B,K):
        if K==B*3 or K==B*3-1 or K==B*3-2:
            return (model.y[K,N] <= model.x[B,N])
        else:
            return (model.y[K,N]>=0)
    
    model.const6 = pyEnv.Constraint(model.N,model.B,model.K,rule=rule_const6)
    
    def rule_const7(model,N,B,K):
        if K==B*3:
            return model.x[B,N] <= model.y[K,N]+model.y[K-1,N]+model.y[K-2,N]
        else:
            return (model.y[K,N]>=0)
    
    model.const7 = pyEnv.Constraint(model.N,model.B,model.K,rule=rule_const7)
    
    def rule_const8(model,N,B,K):
        if K==B*3-1 or K==B*3-2:
            return model.q[K,N] >= model.y[K,N] + model.y[K+1,N] - 1
        else:
            return (model.y[K,N]>=0)
    
    model.const8 = pyEnv.Constraint(model.N,model.B,model.K,rule=rule_const8)
    
    def rule_const9(model,B,K):
        if K==B*3-1 or K==B*3-2:
            return sum(model.q[K,j] for j in model.N) <= 1
        else:
            return sum(model.q[K,j] for j in model.N) >= 0
    
    model.const9 = pyEnv.Constraint(model.B,model.K,rule=rule_const9)
    
    return model
    
    