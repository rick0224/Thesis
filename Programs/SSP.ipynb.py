#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 10:41:10 2021

@author: rickkessels
"""
import pyomo.environ as pyEnv

def SSP(model, i_star):
    
    model.w = pyEnv.Var(model.N, within=pyEnv.Binary)
    
    model.K_i_star = pyEnv.Set(initialize=[i_star*3, i_star*3-1, i_star*3-2])

    model.R_tot = model.K_i_star * model.K_i_star * model.N
    
    def R_construct(m):
        return ((k1,k2,j) for k1 in model.K_i_star for k2 in model.K_i_star for j in model.N if ((k1<k2) and ((sum(model.c_k[h]) for h in range(k1+1,k2))>model.u[j]-2*model.phi[j] for j in model.N)))
    model.R = pyEnv.Set(dimen=3, initialize=R_construct)
    
    def obj_func_SSP(model):
        return sum(model.phi_cap[j] * (model.f_k[k] * model.s[k,j])/model.c_k[k] for k in model.K_i_star for j in model.N)

    model.objective_SSP = pyEnv.Objective(rule=obj_func_SSP,sense=pyEnv.maximize)

    def rule_const2_SSP(model,K_i_star):
        return (sum(model.s[K_i_star,j] for j in model.N) <= model.c_k[K_i_star])

    model.const2_SSP = pyEnv.Constraint(model.K_i_star,rule=rule_const2_SSP)

    def rule_const3A_SSP(model,N):
        return (model.ell[N] * model.w[N]) <= sum(model.s[k,N] for k in model.K_i_star) 

    model.const3A_SSP = pyEnv.Constraint(model.N,rule=rule_const3A_SSP)

    def rule_const3B_SSP(model,N):
        return sum(model.s[k,N] for k in model.K_i_star) <= (model.u[N] * model.w[N])

    model.const3B_SSP = pyEnv.Constraint(model.N,rule=rule_const3B_SSP)
    
    def rule_const4A_SSP(model,N,K_i_star):
        return model.phi_small[N] * model.y[K_i_star,N] <= model.s[K_i_star,N]
    
    model.const4A_SSP = pyEnv.Constraint(model.N, model.K_i_star,rule=rule_const4A_SSP)
    
    def rule_const4B_SSP(model,N,K_i_star):
        return model.s[K_i_star,N] <= min(model.c_k[K_i_star], model.u[N]) * model.y[K_i_star,N]
    
    model.const4B_SSP = pyEnv.Constraint(model.N, model.K_i_star,rule=rule_const4B_SSP)
    

    def rule_const5_SSP(model,N,B,K_i_star):
        if K_i_star==B*3 and ((K_i_star-2, K_i_star,N) not in model.R):
            return model.s[K_i_star-1,N] >= model.c_k[K_i_star-1] * (model.y[K_i_star-2,N]+model.y[K_i_star,N]-1)
        else:
            return (model.y[K_i_star,N]>=0)
    
    model.const5_SSP = pyEnv.Constraint(model.N, model.B, model.K_i_star, rule=rule_const5_SSP)
    
    def rule_const6_SSP(model,N,K_i_star):
        return (model.y[K_i_star,N] <= model.w[N])
    
    model.const6_SSP = pyEnv.Constraint(model.N,model.K_i_star,rule=rule_const6_SSP)
    
    def rule_const7_SSP(model,N,K_i_star):
        return model.w[N] <= sum(model.y[k,N] for k in model.K_i_star)
    
    model.const7_SSP = pyEnv.Constraint(model.N,model.K_i_star,rule=rule_const7_SSP)
    
    def rule_const8_SSP(model,N,K_i_star):
        if K_i_star%3 != 0:
            return model.q[K_i_star,N] >= model.y[K_i_star,N] + model.y[K_i_star+1,N] - 1
        else:
            return (model.y[K_i_star,N]>=0)
    
    model.const8_SSP = pyEnv.Constraint(model.N,model.K_i_star,rule=rule_const8_SSP)
    
    def rule_const9_SSP(model,K_i_star):
        if K_i_star%3 != 0:
            return sum(model.q[K_i_star,j] for j in model.N) <= 1
        else:
            return sum(model.q[K_i_star,j] for j in model.N) >= 0
    
    model.const9_SSP = pyEnv.Constraint(model.K_i_star,rule=rule_const9_SSP)
    
    
    def rule_const10_SSP(model,k1,k2,N):
        if ((k1,k2,N) in model.R):
            model.y[k1,N] + model.y[k2,N] <= 1
    #Solves
    solver = pyEnv.SolverFactory('cplex_direct')
    solver.options['timelimit'] = 3600
    result = solver.solve(model,tee = False)
    
    
    #Prints the results
    #print(result)
    
    #l = list(model.y.keys())
    #for k in l:
       #if model.s[k]() != 0:
            #print(k,'--', model.s[k]())
            
    return model