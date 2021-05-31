from Thesis_Repl_APSA import init, build_problem, solve, haha
from Check2 import check
import numpy as np
import timeit

# Make arrays to store the final MIP gap and CPU time in
fin = []
tim = []

# Auxiliary array
dif = []

# Set the seed to 42 to allow for replication
np.random.seed(42)

# Initialise the eps array with the possible values epsilon can take
eps = [0.005]

# Initialise the tau range between 2 and 4 (inclusive)
t = range(4,5)

products_total = []
shelves_total = []
segments_total = []
lmbd_total = []
L_total = []
H1_total = []
H2_total = []
H3_total = []

# Counter to keep track of the number of instances of a data set
counter_times=0

r_star = np.zeros(30)

# We want to create a new instance of a certain data set 10 times
while (counter_times<10):

    # Call the init() function from Thesis_Repl_APSA.py to create the data set
    products, shelves, segments, lmbd, L, H1, H2, H3 = init()
    
    # Store the data set in arrays so they can be retrieved easily
    products_total.append(products)
    shelves_total.append(shelves)
    segments_total.append(segments)
    lmbd_total.append(lmbd)
    L_total.append(L)
    H1_total.append(H1)
    H2_total.append(H2)
    H3_total.append(H3)
    
    # Counter increases by one because we created a full data set instance
    counter_times = counter_times + 1


for p in range(2,len(products_total)):
    
    # Create a relaxation and solve it
    model, L_fin, H1_fin, H2_fin, H3_fin = build_problem(products_total[p], shelves_total[p], segments_total[p], True, True,True,True,False,L_total[p], H1_total[p], H2_total[p], H3_total[p], True, True, True, True,products_total[p])
    solve(model)
    
    # Make each possible combination of the values for tau and epsilon
    for tau in t:
        for epsilon in eps:
            
            # We only want to test for various values of epsilon for tau = 4
            if (tau!=4 and epsilon>0.005):
                break
            else:
                
                # Initialize the time
                t_start = timeit.default_timer()
                t_end=0
                
                # Store objective value of relaxation into "obj". This is our upper bound as described in Step 1 of Algorithm 2.
                obj = model.objective_value
                r = -1
                    
                # Algorithm 1 starts here
                    
                # Calculate sigma, and initialize other variables
                sigma = np.flip(np.argsort(lmbd))
                products = products_total[p]
                selected_products = []
                
                no_shelves = len(shelves_total[p])
                no_products = len(products_total[p])
                no_segments = len(segments_total[p])
                
                r_star = np.zeros(no_shelves)
                
                shelves_temp = []
                
                x = np.zeros((no_shelves, no_products))
                y = np.zeros((no_segments, no_products))
                s = np.zeros((no_segments, no_products))
                q = np.zeros((no_segments, no_products))
                z = np.zeros((no_products, no_products))
                
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
                
                for i in sigma: # Step 2, with stopping condition (Step 13) automatically included.
                    if (len(products)==0): # Stopping condition (Step 13).
                        break
                    
                    # Step 3
                    shelf = [shelves_total[p][i]]
                    segments = [segments_total[p][i*3], segments_total[p][i*3+1], segments_total[p][i*3+2]]
                    model_SSP, L, H1, H2, H3 = build_problem(products, shelf, segments, False, True,True,True,True, L_total[p], H1_total[p], H2_total[p], H3_total[p], True, True, True, True, products_total[p])
                    solve(model_SSP)
                    
                    track.append(model_SSP)
                    
                    if(len(track)==18):
                        print("yay")
                    
                    for m in model_SSP.shelves:
                        for l in model_SSP.products:
                            if (round(model_SSP.x[m,l].solution_value)==1):
                                selected_products.append(l)
                                x[i,int(l.prod - 1)]=1
                    
                    for l in model_SSP.products:
                        for k in model_SSP.segments:
                            if (round(model_SSP.y[k,l].solution_value)==1):
                                y[int(k.seg - 1),int(l.prod- 1)]=1
                            s[int(k.seg-1),int(l.prod-1)]=round(model_SSP.s[k,l].solution_value,5)
                    
                    for l in model_SSP.products:
                        for k in model_SSP.segments:
                            if(int(k.seg)<no_segments):
                                if(y[int(k.seg - 1),int(l.prod- 1)]==1 and y[int(k.seg),int(l.prod- 1)]==1):
                                    q[int(k.seg - 1),int(l.prod- 1)]=1
                                else:
                                    q[int(k.seg - 1),int(l.prod- 1)]=0
                                    
                    for j1 in model_SSP.products:
                        for j2 in model_SSP.products:
                            if (round(model_SSP.z[j1,j2].solution_value)==1):
                                z[int(j1.prod- 1), int(j2.prod- 1)]=1
                    
                    # Step 5 until step 12
                    for (j1,j2) in H3:
                        if j1 in selected_products and j2 not in selected_products:
                            selected_products.append(j2)
                        elif j2 in selected_products and j1 not in selected_products:
                            selected_products.append(j1)
                            
                    x_track.append(x.copy())
                    y_track.append(y.copy())
                    s_track.append(s.copy())
                    q_track.append(q.copy())
                    z_track.append(z.copy())
                
                    # Step 4
                    allocation[i+1] = selected_products
                    products = diff(model_SSP.products, selected_products)
                    
                    for (j1,j2) in H2_fin:
                        if j2 in selected_products:
                            for k in products:
                                if k.prod==j1.prod:
                                    products.remove(k)
                                    
                    r_star[i] = sum(sum(j[3]* k[2] * s[int(k.seg)-1,int(j.prod)-1] / 6.0 for k in model_SSP.segments if k.shelf==i+1) for j in model_SSP.products)
                    selected_products = []
                
                # Step 2
                r = np.sum(r_star)
                
                i_ar = []
                
                count = 0
                
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
                
                # Stopping conditions (Step 6 and 20)
                while (t_end-t_start<1000 and count<20 and (obj-r)/obj>epsilon):
                    
                    # Step 7
                    tempset = model.shelves
                    
                    delta = np.flip(np.argsort(r_star))
                
                    # Step 8
                    while (len(tempset) > no_shelves % tau):
                        
                        shelves_fin = []
                        products_fin = []
                        segments_fin = []
                        i_ar_instance = []
                        
                        # Step 10
                        omega = np.floor(len(delta)/tau)
                        
                        # Step 11 and 12
                        for k in range(1, tau+1):
                            i = int(np.round(np.floor(np.random.uniform(((k-1)*omega+1),k*omega+1)),0))
                            print(i)
                            for l in model.shelves:
                                if (delta[i-1]+1 == l.shelf):
                                    i_ar.append(i-1)
                                    i_ar_instance.append(l)
                        
                        # Delete shelf value from delta
                        for i in i_ar_instance:
                            delta = np.delete(delta, np.where(delta==(i.shelf-1)))
                        
                        # Step 13
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
                        
                        products_fin_test = products_fin.copy()
                    
                    
                        temp_list = list(allocation.values())
                        
                        merged_list = []
                
                        for l in temp_list:
                            merged_list += l
                            
                        products_allocated = merged_list
                        
                        prod_H3 = []
                        
                        for k in diff(model.products, products_allocated):
                            products_fin.append(k)
                    
                        for (j1,j2) in H2_fin:
                            if j2 in products_allocated and j1 not in products_allocated:
                                for k in products_fin:
                                    if k.prod==j1.prod:
                                        products_fin.remove(k)
                                        
                        for (j1,j2) in H3_fin:
                            if ((j1 in products_fin and j2 not in products_fin)):
                                products_fin.remove(j1)

                        
                        for k in model.segments:
                            for l in shelves_fin:
                                if k.shelf == l:
                                    segments_fin.append(k)
                        
                        shelves_fin = [[i] for i in shelves_fin]
                        
                        # Step 15
                        model_fin, L, H1, H2, H3 = build_problem(products_fin, shelves_fin, segments_fin, False, False,True,True,False, L_total[p], H1_total[p], H2_total[p], H3_total[p],True, True, True, True,products_total[p],x,y,s,q, z)
                        
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
                        
#                        if check(s_prev, x_prev, y_prev, z_prev, q_prev, model_fin, L, H1, H2, H3)==False:
#                            exit
                        
                        x_track2.append(x_prev)
                        y_track2.append(y_prev)
                        s_track2.append(s_prev)
                        q_track2.append(q_prev)
                        z_track2.append(z_prev)
                        
                        # Step 17 and 18
                        for j in model_fin.products:
                            for i in model_fin.shelves:
                                x[int(i.shelf - 1),int(j.prod - 1)]=round(model_fin.x[i,j].solution_value,5)
                            for k in model_fin.segments:
                                y[int(k.seg-1),int(j.prod-1)]=round(model_fin.y[k,j].solution_value,5)
                                s[int(k.seg-1),int(j.prod-1)]=round(model_fin.s[k,j].solution_value,5)
                                
                        for l in model_fin.products:
                            for k in model_fin.segments:
                                if(int(k.seg)<no_segments):
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
                        
                        # Step 16
                        for i in model_fin.shelves:
                            prev = prev + prev_r_star[int(i.shelf-1)]
                            new = new + sum(sum(j[3]* k[2] * s[int(k.seg)-1,int(j.prod)-1] / 6.0 for k in model_fin.segments if k.shelf==i.shelf) for j in model_fin.products)
                            r_star[int(i.shelf-1)] = sum(sum(j[3]* k[2] * s[int(k.seg)-1,int(j.prod)-1] / 6.0 for k in model_fin.segments if k.shelf==i.shelf) for j in model_fin.products)
                        if (prev - sum(sum(j[3]* k[2] * s_prev[int(k.seg)-1,int(j.prod)-1] / 6.0 for k in model_fin.segments) for j in model_fin.products)) > 1e-7 or (prev - sum(sum(j[3]* k[2] * s_prev[int(k.seg)-1,int(j.prod)-1] / 6.0 for k in model_fin.segments) for j in model_fin.products) < -1e-7):
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
                    print(t_end-t_start)
                
                counter_times = counter_times+1
                
                
                comparison = y_track2[0] == y_track[len(y_track)-1]
                equal_arrays = comparison.all()
            
                print(equal_arrays)
            
            tim.append(t_end-t_start)
            fin.append((obj-r)/obj)
            