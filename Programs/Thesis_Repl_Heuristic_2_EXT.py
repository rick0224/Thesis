from extension import init, build_problem, solve, get_cut_stats
from Check2 import check
from Algorithm_1 import algorithm_1, diff
from Algorithm_2 import algorithm_2
from heuristic import heuristic
from healthconstraints import healthconstraints
from solToExcel import solToExcel
import numpy as np
import timeit
import sys
import csv

# Make arrays to store the final MIP gap and CPU time in
fin = []
tim = []
descr = []

cuts = []

# Auxiliary array
dif = []

# Set the seed to 42 to allow for replication
np.random.seed(42)

# Initialise the eps array with the possible values epsilon can take
eps = [0.005, 0.010, 0.015]

# Initialise the tau range between 2 and 4 (inclusive)
t = range(2,5)

# Initialize arrays to store information in later
products_total = []
shelves_total = []
segments_total = []
lmbd_total = []
L_total = []
H1_total = []
H2_total = []
H3_total = []
P_total = []
Q_total = []
R_total = []
S_total = []

# Counter to keep track of the number of instances of a data set
counter_instances=0

# We want to create a new instance of a certain data set 10 times
while (counter_instances<10):

    N = 320
    B = 40
    c_k = 6
    C_i = 18
    
    # Call the init() function from Thesis_Repl_APSA.py to create the data set
    products, shelves, segments, lmbd, L, H1, H2, H3, P, Q, R, S = init(N, B, c_k, C_i)
    
    # Store the data set in arrays so they can be retrieved easily
    products_total.append(products)
    shelves_total.append(shelves)
    segments_total.append(segments)
    lmbd_total.append(lmbd)
    L_total.append(L)
    H1_total.append(H1)
    H2_total.append(H2)
    H3_total.append(H3)
    P_total.append(P)
    Q_total.append(Q)
    R_total.append(R)
    S_total.append(S)    
    
    # Counter increases by one because we created a full data set instance
    counter_instances = counter_instances + 1

for p in range(0,len(products_total)):
    
    # Take current data on products, shelves and segments and put them into variables
    products = products_total[p]
    shelves = shelves_total[p]
    segments = segments_total[p]
    
    # Creating dummies to check
    L_dummy = False
    H1_dummy = False
    H2_dummy = False
    H3_dummy = False
    
    relax = False
    ineq2 = True
    ineq3 = True
    SSP = False
    
    CS1 = False
    CS2 = False
    CS3 = False
    CS4 = False
    CS5 = False
    
    first = True
    APSA_TOTAL = True
    
    # Calculate APSA with the two inequalities
    model, L_tot, H1_tot, H2_tot, H3_tot, P_tot, Q_tot, R_tot, S_tot = build_problem(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k)
    
    # Solve APSA, and store all information we need into arrays
    solve(model)
    bb = model.solve_details.best_bound
    
    if (p==-1):
    
        descr_string = "APSA_TwoInequalities"
        
        solToExcel(model, descr_string)
    
        sum_healthy = 0
        count_healthy_segs = 0
        count_healthy =  0
        for j in P_tot:
            for k in model.segments:
                if model.s[k,j].solution_value>0:
                    count_healthy_segs = count_healthy_segs + 1
                    sum_healthy = sum_healthy + (k.attr * model.s[k,j].solution_value)/c_k
            if (sum(model.s[k,j].solution_value for k in model.segments)>0):
                count_healthy = count_healthy+1
        avg_healthy = sum_healthy / len(P_tot)
         
        sum_unhealthy = 0
        count_unhealthy_segs = 0
        count_unhealthy = 0
        for j in Q_tot:
            for k in model.segments:
                if model.s[k,j].solution_value>0:
                    count_unhealthy_segs = count_unhealthy_segs + 1
                    sum_unhealthy = sum_unhealthy + + (k.attr * model.s[k,j].solution_value)/c_k
            if (sum(model.s[k,j].solution_value for k in model.segments)>0):
                count_unhealthy = count_unhealthy+1
        avg_unhealthy = sum_unhealthy / len(Q_tot)
    
    
    descr_start = "Instance "+str(p+1)+" of N="+str(N)+",B="+str(B)
    descr_array = np.array(descr_start)
    with open('Results.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([descr_start])
                    
    with open('Results.txt', 'a') as f:
        print("---- BEGIN OF DATA SET INSTANCE "+str(p+1)+" ----", file=f)
        print('APSA with the two inequalities: ', file=f)
        print('B&B/C: '+str(model.solve_details.nb_nodes_processed), file=f)
        print("Objective: "+str(model.objective_value), file=f)
        print("Best bound: "+str(model.solve_details.best_bound), file=f)
        print('Gap: '+str(model.solve_details.gap), file=f)
        print('Time: '+str(model.solve_details.time), file=f)
        if (p==-1):
            print('Healthy: '+str(count_healthy) + ', Segments: '+str(count_healthy_segs)+', Average: '+str(avg_healthy), file=f)
            print('Unhealthy: '+str(count_unhealthy) + ', Segments: '+str(count_unhealthy_segs)+', Average: '+str(avg_unhealthy)+'\n', file=f)
            
    if (p==-1):       
        
        CS1 = True
        CS2 = False
        CS3 = False
        CS4 = False
        CS5 = False
        
        CSString = "CS1"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
        
        CS1 = False
        CS2 = True
        CS3 = False
        CS4 = False
        CS5 = False    
    
        CSString = "CS2"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = False
        CS2 = False
        CS3 = True
        CS4 = False
        CS5 = False    
    
        CSString = "CS3"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
     
        CS1 = False
        CS2 = False
        CS3 = False
        CS4 = True
        CS5 = False    
    
        CSString = "CS4"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = False
        CS2 = False
        CS3 = False
        CS4 = False
        CS5 = True   
    
        CSString = "CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = True
        CS3 = False
        CS4 = False
        CS5 = False   
    
        CSString = "CS1 + CS2"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
          
        CS1 = True
        CS2 = False
        CS3 = True
        CS4 = False
        CS5 = False   
    
        CSString = "CS1 + CS3"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
            
        CS1 = True
        CS2 = False
        CS3 = False
        CS4 = True
        CS5 = False   
    
        CSString = "CS1 + CS4"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = False
        CS3 = False
        CS4 = False
        CS5 = True  
    
        CSString = "CS1 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
           
        CS1 = False
        CS2 = True
        CS3 = True
        CS4 = False
        CS5 = False  
    
        CSString = "CS2 + CS3"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
           
        CS1 = False
        CS2 = True
        CS3 = False
        CS4 = True
        CS5 = False  
    
        CSString = "CS2 + CS4"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
            
        CS1 = False
        CS2 = True
        CS3 = False
        CS4 = False
        CS5 = True 
    
        CSString = "CS2 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
     
        
        CS1 = False
        CS2 = False
        CS3 = True
        CS4 = True
        CS5 = False
    
        CSString = "CS3 + CS4"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
        
        CS1 = False
        CS2 = False
        CS3 = True
        CS4 = False
        CS5 = True 
    
        CSString = "CS3 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = False
        CS2 = False
        CS3 = False
        CS4 = True
        CS5 = True 
    
        CSString = "CS4 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = True
        CS3 = True
        CS4 = False
        CS5 = False
    
        CSString = "CS1 + CS2 + CS3"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = True
        CS3 = False
        CS4 = True
        CS5 = False
    
        CSString = "CS1 + CS2 + CS4"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = True
        CS3 = False
        CS4 = False
        CS5 = True
    
        CSString = "CS1 + CS2 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = False
        CS3 = True
        CS4 = True
        CS5 = False
    
        CSString = "CS1 + CS3 + CS4"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = False
        CS3 = True
        CS4 = False
        CS5 = True
    
        CSString = "CS1 + CS3 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = False
        CS3 = False
        CS4 = True
        CS5 = True
    
        CSString = "CS1 + CS4 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = False
        CS2 = True
        CS3 = True
        CS4 = True
        CS5 = False
    
        CSString = "CS2 + CS3 + CS4"
        
        CS1 = False
        CS2 = True
        CS3 = True
        CS4 = False
        CS5 = True
    
        CSString = "CS2 + CS3 + CS5"
        
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = False
        CS2 = True
        CS3 = False
        CS4 = True
        CS5 = True
    
        CSString = "CS2 + CS4 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = False
        CS2 = False
        CS3 = True
        CS4 = True
        CS5 = True
    
        CSString = "CS3 + CS4 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = True
        CS3 = True
        CS4 = True
        CS5 = False
    
        CSString = "CS1 + CS2 + CS3 + CS4"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = True
        CS3 = True
        CS4 = False
        CS5 = True
    
        CSString = "CS1 + CS2 + CS3 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = True
        CS3 = False
        CS4 = True
        CS5 = True
    
        CSString = "CS1 + CS2 + CS4 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = False
        CS3 = True
        CS4 = True
        CS5 = True
    
        CSString = "CS1 + CS3 + CS4 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = False
        CS2 = True
        CS3 = True
        CS4 = True
        CS5 = True
    
        CSString = "CS2 + CS3 + CS4 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
    
        CS1 = True
        CS2 = True
        CS3 = True
        CS4 = True
        CS5 = True
    
        CSString = "CS1 + CS2 + CS3 + CS4 + CS5"
        healthconstraints(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, CSString)
                   
    # Calculate APSA with only the first inequality
    
   # ineq2 = True
   # ineq3 = False
    
   # model, L_tot, H1_tot, H2_tot, H3_tot, P_tot, Q_tot, R_tot, S_tot = build_problem(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k)
    
    # Solve APSA, and store all information we need into arrays
  #  solve(model)
   # cuts.append(get_cut_stats(model))
   # fin.append(model.solve_details.gap)
   # tim.append(model.solve_details.time)
   # descr.append("APSA with only inequality (2)")
    
   # with open('Results.txt', 'a') as f:
   #     print('APSA with only inequality (2): ', file=f)
   #     print('Cuts: '+str(get_cut_stats(model)), file=f)
   #     print('Gap: '+str(model.solve_details.gap), file=f)
   #     print('Time: '+str(model.solve_details.time)+'\n', file=f)
        
    # Calculate APSA with no inequalities
    
  #  ineq2 = False
  #  ineq3 = False
    
  #  model, L_tot, H1_tot, H2_tot, H3_tot, P_tot, Q_tot, R_tot, S_tot = build_problem(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k)
  
    # Solve APSA, and store all information we need into arrays
  #  solve(model)
  #  cuts.append(get_cut_stats(model))
  #  fin.append(model.solve_details.gap)
  #  tim.append(model.solve_details.time)
  #  descr.append("APSA with none of the inequalities")
    
  #  with open('Results.txt', 'a') as f:
  #      print('APSA with none of the inequalities: ', file=f)
  #      print('Cuts: '+str(get_cut_stats(model)), file=f)
  #      print('Gap: '+str(model.solve_details.gap), file=f)
  #      print('Time: '+str(model.solve_details.time)+'\n', file=f) 

    CS1 = False
    CS2 = False
    CS3 = False
    CS4 = False
    CS5 = False
    
    # Make each possible combination of the values for tau and epsilon
    for tau in t:
        for epsilon in eps:
            
            # We only want to test for various values of epsilon for tau = 4
            if (tau!=4 and epsilon>0.005):
                break
            
            else:
                
                # Define r (the current objective value) in such a way that the stopping condition is not yet satisfied.
                r = float('-inf')
                
                # If tau = 4 and epsilon = 0.005, we want to implement the affinity sets one by one, and all together
                if (tau==4 and epsilon==0.005):
                    
                    # Booleans to keep track which affinity set(s) is/are included
                    L_dummy = False
                    H1_dummy = False
                    H2_dummy = False
                    H3_dummy = False
                    
                    CS1 = False
                    CS2 = False
                    CS3 = False
                    CS4 = False
                    CS5 = False
                    
                    #----- Model with affinity: L ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
                    aff = True
                    
                    # Initialize the time
                    t_start = timeit.default_timer()
                    t_end=0
            
                    
                    # Put affinity dummy L to True
                    L_dummy = True
                    
                    CSString = "L"
                    
                    heuristic(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, lmbd, epsilon, tau, aff, CSString, t_start, bb)

                    
                    #----- Model with affinity: H1 ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  
                    # Initialize the time
                    t_start = timeit.default_timer()
                    t_end=0
                    
                    # Put affinity dummy H1 to True, and put affinity dummy L back to False        
                    L_dummy = False
                    H1_dummy = True
                    
                    CSString = "H1"
                    
                    heuristic(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, lmbd, epsilon, tau, aff, CSString, t_start, bb)

                    #----- Model with affinity: H2 ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  
                    # Initialize the time
                    t_start = timeit.default_timer()
                    t_end=0
                    
                    # Put affinity dummy H2 to True, and put affinity dummy H1 back to False
                    H1_dummy = False
                    H2_dummy = True
                    
                    CSString = "H2"
                    
                    heuristic(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, lmbd, epsilon, tau, aff, CSString, t_start, bb)
                    
                    #----- Model with affinity: H3 ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  
                    # Initialize the time
                    t_start = timeit.default_timer()
                    t_end=0
                    
                    # Put affinity dummy H3 to True, and put affinity dummy H2 back to False
                    H2_dummy = False
                    H3_dummy = True
                    
                    CSString = "H3"
                    
                    heuristic(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, lmbd, epsilon, tau, aff, CSString, t_start, bb)

                    
                    #----- Model with affinity: L, H1, H2, H3 ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  
                    # Initialize the time
                    t_start = timeit.default_timer()
                    t_end=0
                    
                    # Put all affinity dummies to value True
                    L_dummy = True
                    H1_dummy = True
                    H2_dummy = True
                    H3_dummy = True
                    
                    CSString = "L, H1, H2, H3"
                    
                    heuristic(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, lmbd, epsilon, tau, aff, CSString, t_start, bb)

                #----- Model without affinity ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                
                # Initialize the time
                t_start = timeit.default_timer()
                t_end=0
                
                # Put all affinity dummies to value False
                L_dummy = False
                H1_dummy = False
                H2_dummy = False
                H3_dummy = False
                
                relax= True
                
                aff = False
                
                CSString = "No affinity"
                
                heuristic(products, shelves, segments, relax, first, ineq2, ineq3, SSP, L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy, P_total[p], Q_total[p], R_total[p], S_total[p], CS1, CS2, CS3, CS4, CS5, products_total[p], c_k, lmbd, epsilon, tau, aff, CSString, t_start, bb)

                    
                if (tau==4 and epsilon==0.015):
                    with open('Results.txt', 'a') as f:
                        print("---- END OF DATA SET INSTANCE "+str(p+1)+" ----", file=f)
                        
                        