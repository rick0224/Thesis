from Thesis_Repl_APSA import init, build_problem, solve, get_cut_stats
from Check2 import check
from Algorithm_1 import algorithm_1, diff
from Algorithm_2 import algorithm_2
import numpy as np
import timeit
import sys

# Make arrays to store the final MIP gap and CPU time in
fin = []
tim = []
descr = []

cuts = []

# Auxiliary array
dif = []

# Set the seed to 42 to allow for replication
np.random.seed(45)

# Initialise the eps array with the possible values epsilon can take
eps = [0.005, 0.010, 0.015]

# Initialise the tau range between 2 and 4 (inclusive)
t = range(2,5)

products_total = []
shelves_total = []
segments_total = []
lmbd_total = []
L_total = []
H1_total = []
H2_total = []
H3_total = []

# Counter to keep track of the number of instances of a data set
counter_instances=0

def relaxation(products, shelves, segments, rel, first, ineq2, ineq3,SSP,L, H1, H2, H3, L_dummy, H1_dummy, H2_dummy, H3_dummy ,products_total, c_k):
    # Create a relaxation and solve it
    model, L_tot, H1_tot, H2_tot, H3_tot = build_problem(products, shelves, segments, rel, first, ineq2, ineq3,SSP,L, H1, H2, H3, L_dummy, H1_dummy, H2_dummy, H3_dummy ,products_total, c_k)
    solve(model)
    return model, L_tot, H1_tot, H2_tot, H3_tot

# We want to create a new instance of a certain data set 10 times
while (counter_instances<10):

    N = 240
    B = 30
    c_k = 6
    C_i = 18
    
    # Call the init() function from Thesis_Repl_APSA.py to create the data set
    products, shelves, segments, lmbd, L, H1, H2, H3 = init(N, B, c_k, C_i)
    
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
    
    # Calculate APSA with the two inequalities
    model, L_tot, H1_tot, H2_tot, H3_tot = build_problem(products, shelves, segments, False, True,True,True,False,L_total[p], H1_total[p], H2_total[p], H3_total[p], L_dummy, H1_dummy, H2_dummy, H3_dummy ,products_total[p], c_k)
    
    # Solve APSA, and store all information we need into arrays
    solve(model)
    cuts.append(get_cut_stats(model))
    fin.append(model.solve_details.gap)
    tim.append(model.solve_details.time)
    descr.append("APSA")
    
    with open('Results.txt', 'a') as f:
        print("---- BEGIN OF DATA SET INSTANCE "+str(p+1)+" ----", file=f)
        print('APSA: ', file=f)
        print('Cuts: '+str(get_cut_stats(model)), file=f)
        print('Gap: '+str(model.solve_details.gap), file=f)
        print('Time: '+str(model.solve_details.time)+'\n', file=f)
    
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
                    
                    # Boolean to keep track of whether the affinity sets are (partly) included or not
                    no_aff = False
                    
                    # Booleans to keep track which affinity set(s) is/are included
                    L_dummy = False
                    H1_dummy = False
                    H2_dummy = False
                    H3_dummy = False
                    
                    #----- Model with affinity: L ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
                    # Initialize the time
                    t_start = timeit.default_timer()
                    t_end=0
                    
                    # Put affinity dummy L to True
                    L_dummy = True
                    
                    # Calculate associated relaxation
                    model_L, L, H1, H2, H3 = relaxation(products, shelves, segments, True, True, True, True, False, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy,products_total[p], c_k)
                    
                    # Store objective value of relaxation into "upperbound". This is our upper bound as described in Step 1 of Algorithm 2.
                    upperbound = model_L.objective_value
                    
                    # Call algorithm 1
                    allocation, r_star, x, y, s, q, z = algorithm_1(lmbd, products, shelves, segments, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k)
                    
                    # Call algorithm 2
                    gap, time = algorithm_2(allocation, r_star, t_start, upperbound, epsilon, model_L, tau, x, y, s, q, z, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k, no_aff)
                    
                    # Store results into arrays
                    fin.append(gap)
                    tim.append(time)
                    descr.append("tau = 4, epsilon = 0.005, L only")
                    
                    with open('Results.txt', 'a') as f:
                        print('', file=f)
                        print('tau = 4, epsilon = 0.005, L only: ', file=f)
                        print('Gap: '+str(gap), file=f)
                        print('Time: '+str(time)+'\n', file=f)
                    
                    #----- Model with affinity: H1 ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  
                    # Initialize the time
                    t_start = timeit.default_timer()
                    t_end=0
                    
                    # Put affinity dummy H1 to True, and put affinity dummy L back to False        
                    L_dummy = False
                    H1_dummy = True
                    
                    # Calculate associated relaxation
                    model_H1, L, H1, H2, H3 = relaxation(products, shelves, segments, True, True, True, True, False,L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy,products_total[p], c_k)                 
                    
                    # Store objective value of relaxation into "upperbound". This is our upper bound as described in Step 1 of Algorithm 2.
                    upperbound = model_H1.objective_value
                    
                    # Call algorithm 1
                    allocation, r_star, x, y, s, q, z = algorithm_1(lmbd, products, shelves, segments, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k)
                    
                    # Call algorithm 2
                    gap, time = algorithm_2(allocation, r_star, t_start, upperbound, epsilon, model_H1, tau, x, y, s, q, z, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k, no_aff)
                    
                    # Store results into arrays
                    fin.append(gap)
                    tim.append(time)
                    descr.append("tau = 4, epsilon = 0.005, H1 only")
                 
                    with open('Results.txt', 'a') as f:
                        print('', file=f)
                        print('tau = 4, epsilon = 0.005, H1 only: ', file=f)
                        print('Gap: '+str(gap), file=f)
                        print('Time: '+str(time)+'\n', file=f)

                    #----- Model with affinity: H2 ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  
                    # Initialize the time
                    t_start = timeit.default_timer()
                    t_end=0
                    
                    # Put affinity dummy H2 to True, and put affinity dummy H1 back to False
                    H1_dummy = False
                    H2_dummy = True
                    
                    # Calculate associated relaxation
                    model_H2, L, H1, H2, H3 = relaxation(products, shelves, segments, True, True, True, True, False,L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, products_total[p], c_k)                 
  
                    # Store objective value of relaxation into "upperbound". This is our upper bound as described in Step 1 of Algorithm 2.
                    upperbound = model_H2.objective_value
                    
                    # Call algorithm 1
                    allocation, r_star, x, y, s, q, z = algorithm_1(lmbd, products, shelves, segments, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k)
                    
                    # Call algorithm 2
                    gap, time = algorithm_2(allocation, r_star, t_start, upperbound, epsilon, model_H2, tau, x, y, s, q, z, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k, no_aff)
                    
                    # Store results into arrays
                    fin.append(gap)
                    tim.append(time)       
                    descr.append("tau = 4, epsilon = 0.005, H2 only")
                    
                    with open('Results.txt', 'a') as f:
                        print('', file=f)
                        print('tau = 4, epsilon = 0.005, H2 only: ', file=f)
                        print('Gap: '+str(gap), file=f)
                        print('Time: '+str(time)+'\n', file=f)
                    
                    #----- Model with affinity: H3 ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  
                    # Initialize the time
                    t_start = timeit.default_timer()
                    t_end=0
                    
                    # Put affinity dummy H3 to True, and put affinity dummy H2 back to False
                    H2_dummy = False
                    H3_dummy = True
                    
                    # Calculate associated relaxation
                    model_H3, L, H1, H2, H3= relaxation(products, shelves, segments, True, True, True, True, False,L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy ,products_total[p], c_k)                 

                    # Store objective value of relaxation into "upperbound". This is our upper bound as described in Step 1 of Algorithm 2.
                    upperbound = model_H3.objective_value
                    
                    # Call algorithm 1
                    allocation, r_star, x, y, s, q, z = algorithm_1(lmbd, products, shelves, segments, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k)
                    
                    # Call algorithm 2
                    gap, time = algorithm_2(allocation, r_star, t_start, upperbound, epsilon, model_H3, tau, x, y, s, q, z, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k, no_aff)
                    
                    # Store results into arrays
                    fin.append(gap)
                    tim.append(time)       
                    descr.append("tau = 4, epsilon = 0.005, H3 only")
                    
                    with open('Results.txt', 'a') as f:
                        print('', file=f)
                        print('tau = 4, epsilon = 0.005, H3 only: ', file=f)
                        print('Gap: '+str(gap), file=f)
                        print('Time: '+str(time)+'\n', file=f)
                    
                    #----- Model with affinity: L, H1, H2, H3 ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  
                    # Initialize the time
                    t_start = timeit.default_timer()
                    t_end=0
                    
                    # Put all affinity dummies to value True
                    L_dummy = True
                    H1_dummy = True
                    H2_dummy = True
                    H3_dummy = True
                    
                    # Calculate associated relaxation
                    model_H3, L, H1, H2, H3= relaxation(products, shelves, segments, True, True, True, True, False,L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy ,products_total[p], c_k)                 

                    # Store objective value of relaxation into "upperbound". This is our upper bound as described in Step 1 of Algorithm 2.
                    upperbound = model_H3.objective_value
                    
                    # Call algorithm 1
                    allocation, r_star, x, y, s, q, z = algorithm_1(lmbd, products, shelves, segments, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k)
                    
                    # Call algorithm 2
                    gap, time = algorithm_2(allocation, r_star, t_start, upperbound, epsilon, model_H3, tau, x, y, s, q, z, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k, no_aff)
                    
                    # Store results into arrays
                    fin.append(gap)
                    tim.append(time)       
                    descr.append("tau = 4, epsilon = 0.005, all")
                    
                    with open('Results.txt', 'a') as f:
                        print('', file=f)
                        print('tau = 4, epsilon = 0.005, all: ', file=f)
                        print('Gap: '+str(gap), file=f)
                        print('Time: '+str(time)+'\n', file=f)
                
                #----- Model without affinity ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  
                # Put the overall non-affinity dummy to value True
                no_aff = True
                
                # Initialize the time
                t_start = timeit.default_timer()
                t_end=0
                
                # Put all affinity dummies to value False
                L_dummy = False
                H1_dummy = False
                H2_dummy = False
                H3_dummy = False
                
                # Calculate associated relaxation
                model_all, L, H1, H2, H3 = relaxation(products, shelves, segments, True, True, True, True, False,L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy ,products_total[p], c_k)                 

                # Store objective value of relaxation into "upperbound". This is our upper bound as described in Step 1 of Algorithm 2.
                upperbound = model_all.objective_value
                
                # Call algorithm 1
                allocation, r_star, x, y, s, q, z = algorithm_1(lmbd, products, shelves, segments, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k)
                
                # Call algorithm 2
                gap, time = algorithm_2(allocation, r_star, t_start, upperbound, epsilon, model_all, tau, x, y, s, q, z, L_tot, H1_tot, H2_tot, H3_tot, L_dummy, H1_dummy, H2_dummy, H3_dummy, c_k, no_aff)
                
                # Store results into arrays
                fin.append(gap)
                tim.append(time)
                description = "tau = "+str(tau)+", epsilon = "+str(epsilon)+", none"
                descr.append(description)
                
                with open('Results.txt', 'a') as f:
                    print('tau = '+str(tau)+', epsilon = '+str(epsilon)+', none: ', file=f)
                    print('Gap: '+str(gap), file=f)
                    print('Time: '+str(time)+'\n', file=f)
                    
                if (tau==4 and epsilon==0.005):
                    with open('Results.txt', 'a') as f:
                        print("---- END OF DATA SET INSTANCE "+str(p+1)+" ----", file=f)
                    
                