
# -*- coding: utf-8 -*-
from Thesis_Repl_APSA import init, build_problem, solve, haha
from Check2 import check
import numpy as np
import timeit

fin = []
tim = []
dif = []
counter_times=0
while (counter_times<20):
    
    t_start = timeit.default_timer()
    
    # Algorithm 2
    
    # Step 1: Solve the continuous relaxation
    x=0
    y=0
    s=0
    q=0
    z=0
    
    PRODUCTS, SHELVES, SEGMENTS, lmbd, L_tot, H1_tot, H2_tot, H3_tot = init()
    model, L, H1, H2, H3 = build_problem(PRODUCTS, SHELVES, SEGMENTS, True, True,True,True,False,x,y,s,q, z,L_tot, H1_tot, H2_tot, H3_tot)
    solve(model)
    
    obj = model.objective_value
    
    sigma = np.flip(np.argsort(lmbd))
    products = PRODUCTS
    selected_products = []
    
    r_star = np.zeros(len(SHELVES))
    
    shelves_temp = []
    
    x = np.zeros((len(SHELVES), len(PRODUCTS)))
    y = np.zeros((len(SEGMENTS), len(PRODUCTS)))
    s = np.zeros((len(SEGMENTS), len(PRODUCTS)))
    q = np.zeros((len(SEGMENTS), len(PRODUCTS)))
    z = np.zeros((len(PRODUCTS), len(PRODUCTS)))
    
    allocation = {}
    
    track = []
    
    x_track=[]
    y_track=[]
    s_track=[]
    q_track=[]
    z_track=[]
    
    def diff(first, second):
            second = set(second)
            return [item for item in first if item not in second]
    
    for i in sigma:
        if (len(products)==0):
            break
        shelf = [SHELVES[i]]
        segments = [SEGMENTS[i*3], SEGMENTS[i*3+1], SEGMENTS[i*3+2]]
        model_two, L, H1, H2, H3 = build_problem(products, shelf, segments, False, True,True,True,True,x,y,s,q, z, L_tot, H1_tot, H2_tot, H3_tot)
        solve(model_two)
        track.append(model_two)
        
        for m in model_two.shelves:
            for l in model_two.products:
                if (round(model_two.x[m,l].solution_value)==1):
                    selected_products.append(l)
                    x[i,int(l.prod - 1)]=1
        
        for l in model_two.products:
            for k in model_two.segments:
                if (round(model_two.y[k,l].solution_value)==1):
                    y[int(k.seg - 1),int(l.prod- 1)]=1
                s[int(k.seg-1),int(l.prod-1)]=round(model_two.s[k,l].solution_value,5)
        
        for l in model_two.products:
            for k in model_two.segments:
                if(int(k.seg)<len(SEGMENTS)):
                    if(y[int(k.seg - 1),int(l.prod- 1)]==1 and y[int(k.seg),int(l.prod- 1)]==1):
                        q[int(k.seg - 1),int(l.prod- 1)]=1
                    else:
                        q[int(k.seg - 1),int(l.prod- 1)]=0
                        
        for j1 in model_two.products:
            for j2 in model_two.products:
                if (round(model_two.z[j1,j2].solution_value)==1):
                    z[int(j1.prod- 1), int(j2.prod- 1)]=1
                        
        x_track.append(x.copy())
        y_track.append(y.copy())
        s_track.append(s.copy())
        q_track.append(q.copy())
        z_track.append(z.copy())
    
        allocation[i+1] = selected_products
        print(len(selected_products))
        products = diff(model_two.products, selected_products)
        print(len(products))
        r_star[i] = model_two.objective_value
        selected_products = []
        
    
    r = np.sum(r_star)
    
    i_ar = []
    
    tau = 4
    
    count = 0
    
    epsilon = 0.005
    
    res = []
    
    differ = []
    
    flag = True
    
    flag2=False
    
    file_sol=0
    
    track2 = []
    
    x_track2=[]
    y_track2=[]
    s_track2=[]
    q_track2=[]
    z_track2=[]
    
    prev_r_star_matrix = []
    
    while (flag == True):
        
        tempset = model.shelves
        
        delta = np.flip(np.argsort(r_star))
    
        while (len(tempset) > len(SHELVES) % tau):
            
            shelves_fin = []
            products_fin = []
            segments_fin = []
            i_ar_instance=[]
            
            omega = np.floor(len(delta)/tau)
            
            for k in range(1, tau+1):
                i = int(np.round(np.floor(np.random.uniform(((k-1)*omega+1),k*omega+1)),0))
                print(i)
                for l in model.shelves:
                    if (delta[i-1]+1 == l.shelf):
                        i_ar.append(i-1)
                        i_ar_instance.append(l)
                            
            for i in i_ar_instance:
                delta = np.delete(delta, np.where(delta==(i.shelf-1)))
            
            tempset = diff(tempset, i_ar_instance)
            
            for k in range(0,len(i_ar_instance)):
                shelves_fin.append(i_ar_instance[k].shelf)
                
                
            for k in range(0,len(shelves_fin)):
                if (shelves_fin[k] in allocation):
                    products_fin.append(allocation[shelves_fin[k]])
            
            merged_list = []
    
            for l in products_fin:
                merged_list += l
                
            products_fin = merged_list
            
                
            temp_list = list(allocation.values())
            
            merged_list = []
    
            for l in temp_list:
                merged_list += l
                
            products_allocated = merged_list
            
            for k in diff(model.products, products_allocated):
                products_fin.append(k)
            
            for k in model.segments:
                for l in shelves_fin:
                    if k.shelf == l:
                        segments_fin.append(k)
            
            shelves_fin = [[i] for i in shelves_fin]
            model_fin, L, H1, H2, H3 = build_problem(products_fin, shelves_fin, segments_fin, False, False,True,True,False,x,y,s,q,z, L_tot, H1_tot, H2_tot, H3_tot)
            
            if flag2==True:
                model_fin.add_mip_start(file_sol)
            else:
                flag2==True
                
            sol = solve(model_fin)
            track2.append(model_fin)
            file_sol = sol.export_as_mst()
            
            x_prev = x.copy()
            y_prev = y.copy()
            s_prev = s.copy()
            q_prev = q.copy()
            z_prev = z.copy()
            
            if check(s_prev, x_prev, y_prev, z_prev, q_prev, model_fin, L, H1, H2, H3)==False:
                exit
            
            x_track2.append(x_prev)
            y_track2.append(y_prev)
            s_track2.append(s_prev)
            q_track2.append(q_prev)
            z_track2.append(z_prev)
        
            for j in model_fin.products:
                for i in model_fin.shelves:
                    x[int(i.shelf - 1),int(j.prod - 1)]=round(model_fin.x[i,j].solution_value,5)
                for k in model_fin.segments:
                    y[int(k.seg-1),int(j.prod-1)]=round(model_fin.y[k,j].solution_value,5)
                    s[int(k.seg-1),int(j.prod-1)]=round(model_fin.s[k,j].solution_value,5)
                    
            for l in model_fin.products:
                for k in model_fin.segments:
                    if(int(k.seg)<len(SEGMENTS)):
                        if(y[int(k.seg - 1),int(l.prod- 1)]==1 and y[int(k.seg),int(l.prod- 1)]==1):
                            q[int(k.seg - 1),int(l.prod- 1)]=1
                        else:
                            q[int(k.seg - 1),int(l.prod- 1)]=0
            
            for j1 in model_fin.products:
                for j2 in model_fin.products:
                    z[int(j1.prod-1),int(j2.prod-1)]=round(model_fin.z[j1,j2].solution_value,5)

            prev = 0
            new = 0
            prev_r_star = r_star.copy()
            
            prev_r_star_matrix.append(prev_r_star)
            
            print(r_star)
            for i in model_fin.shelves:
                prev = prev + prev_r_star[int(i.shelf-1)]
                obj3, obj2  = haha(model_fin)
                new = new + obj2[int(i.shelf-1)]
                print(obj2[int(i.shelf-1)])
                r_star[int(i.shelf-1)] = (obj2[int(i.shelf-1)])
            if (prev - sum(sum(j[3]* k[2] * s_prev[int(k.seg)-1,int(j.prod)-1] / 6.0 for k in model_fin.segments) for j in model_fin.products)) > 1e-7 and (prev - sum(sum(j[3]* k[2] * s_prev[int(k.seg)-1,int(j.prod)-1] / 6.0 for k in model_fin.segments) for j in model_fin.products) < -1e-7):
                exit
            differ.append(new-prev)
            if (new-prev<-1e-7):
                exit
                
            allocation = {}
            
            for i in model.shelves:
                prod_shelf = []
                for j in model.products:
                    if x[int(i.shelf - 1),int(j.prod - 1)]==1:
                        print(str(int(i.shelf - 1))+","+str(int(j.prod - 1)))
                        prod_shelf.append(j)
                allocation[int(i.shelf)] = prod_shelf 
                        
            r = np.sum(r_star)
            
            if ((obj-r)/obj < epsilon):
                flag = False
                break
            
        print((obj-r)/obj)
        res.append(((obj-r)/obj))
        count = count + 1
            
    t_end = timeit.default_timer()
    
    tim.append(t_end-t_start)
    fin.append((obj-r)/obj)
    counter_times = counter_times+1
    
    
    comparison = y_track2[0] == y_track[len(y_track)-1]
    equal_arrays = comparison.all()

    print(equal_arrays)
    
            
            
                