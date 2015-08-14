#%%
location_of_this_script = "/Users/andrew/Dropbox/_Python/rentdivision"
import sys
sys.path.append(location_of_this_script)

#%%
# Load Joris van Rantwijk's Maximum Weight Matching package,
# taken from http://jorisvr.nl/maximummatching.html
from mwmatching import maxWeightMatching

#%%
# Load mysubroutine for computing the minimum density cycle 
# in a doubly weighted graph:
from mdcycle import min_density_cycle

#% LOAD STANDARD LIBRARIES
############################################
import itertools as it
import pandas as pd
import numpy as np
import numpy.linalg as la
import itertools # @@: try to eliminate this dependency


#%% DEFINE GENERALLY USEFUL FUNCTIONS
###########################################
def argmax (lst,fun) :
    vals = [fun(x) for x in lst]
    max_value = max(vals)
    max_index = vals.index(max_value)
    return lst[max_index]
def argmin (lst,fun) :
    vals = [fun(x) for x in lst]
    min_value = min(vals)
    min_index = vals.index(min_value)
    return lst[min_index]


#%% LOAD EXAMPLE INPUTS (for interactive use)
###########################################
total_rent = 5400
total_rent

#%%
values = pd.DataFrame({
    'Alice' : [30,20,0,200],
    'Bob' : [201,32,23,0],
    'Caitlin' : [31,204,29,0],
    'Dave' : [32,26,212,0]
    }).T
values

#%% RENTAL HARMONY CALCULATOR:
###########################################
def rental_harmony(total_rent,values) :

#%%  
    n = len(values)
    assert (values.shape == (n,n))
    housemate = list(values.index)
    
    #%% PART 1: ROOM ASSIGNMENTS
    ###########################################
    # Apply van Rantwijk's Maximum Weight Matching package:
    # create a weighted bipartite graph where 
    # vertices 0,...,n-1 represent housemates and
    # vertices n,2n-1 represent rooms,
    # and edge weights represent utility assignments.
    edge_weights = [(i,n+j,values[i][housemate[j]]) 
        for i in range(0,n) for j in range(0,n)]

    #s[i]=j will mean housemate[i] will get room j:
    s = maxWeightMatching(edge_weights,maxcardinality=True)[n:]

    #store s in a data frame with labelled rows for easier debugging    
    assignment = pd.DataFrame({housemate[i] : [s[i]] for i in range(0,n)}).T
    assignment.columns = ["Room"]
    
    #%% PART 2: RENT ASSIGNMENTS
    ############################################
    all_pairs = [(i,j) 
        for i in range(0,n) 
        for j in range(0,n)]
    distinct_pairs = [(i,j) 
        for i in range(0,n) 
        for j in range(0,n) 
        if i != j]
    
    #%%
    # In the end, d[i,j] will be the rent personi i pays 
    # minus the rent person j pays; that is, 
    # d[i,j] = price[s[i]] - price[s[j]]
    # But first the values of d[i,j] will be unknown.
    # M will be a matrix of linearly independent rows that
    # we build over time, which, when applied to the vector 
    # of optimal prices, will return another vector y.  
    # Once M has n rows, we can stop and solve for the 
    # optimal pricing.    
    global d 
    d = dict({})
    global M
    global y    
    def reset_mutables () :    
        global d 
        global M
        global y
        d = {ij : None for ij in distinct_pairs}
        for i in range(0,n):
            d[i,i] = 0
        M = np.matrix([[1]*n])
        y = np.matrix([[total_rent]])

    reset_mutables()
        
    #%%
    # For notational convenience, we let
    # v[i,j] = values.loc[housemate[i],s[j]]
    #        = the value housemate i will assign to person j's room.
    # let r_i = price[s[i]] = the rent paid by person i, so
    # v[i,i] - r_i > v[i,j] - r_j, thus
    # d[i,j] = r_i - r_j < v[i,i] - v[i,j]
    # Therefore
    # u[i,j] = v[i,i] - v[i,j]
    # will be an upper bound for d[i,j].
    v = {(i,j) : values.loc[housemate[i],s[j]] for (i,j) in all_pairs}
    u = {(i,j) : (v[i,i] - v[i,j]) for i in range(0,n) for j in range(0,n)}


    #%% 
    def get_min_density_cycle():
        vertices = range(0,n)
        length_dict = {(i,j) : 1 if d[i,j] == None else 0 for (i,j) in all_pairs}
        weight_dict = {(i,j) : u[i,j] if d[i,j] == None else d[i,j] for (i,j) in all_pairs}
        return min_density_cycle(vertices,weight_dict,length_dict,error_tolerance=1e-4)

    #%%
    def vec(i,j) : 
        entries = [1 if k == i else (-1 if k==j else 0) for k in range(0,n)]
        return np.array(entries)
        
    def in_rowspan (row,M) :
        return la.matrix_rank(np.vstack([M,row])) == M.shape[0]
    
    def maybe_add_to_M (i,j) :
        new_row = np.array(vec(i,j))
        global M
        global y
        if not in_rowspan(new_row,M) and not d[i,j] == None:
            M = np.vstack([M,new_row])
            y = np.vstack([y,[d[i,j]]])
    

    #%%
    def edges_of(path) :
        return [(path[i],path[i+1]) for i in range(0,len(path)-1)]
    #edges_of((1,3,4))

    def free_edges () : 
        return [(i,j) for (i,j) in distinct_pairs if d[(i,j)] == None]

    def free_edges_of(path) : 
        return [ij for ij in edges_of(path) if d[ij]==None]
    #free_edges_of((0,1,2))

    
    #%%
    def set_next_rent_differences () :
        global min_cycle; 
        global min_density; 
        (min_density,min_cycle) = get_min_density_cycle()
        global free_pairs; free_pairs = free_edges_of(min_cycle)    
        global d
        global M
        global y
        for (i,j) in free_pairs :
            #print (i,j)
            d[i,j] = u[i,j] - min_density
            maybe_add_to_M (i,j)
    
    #%%
    def set_implied_values () :
        global M
        global y
        for (i,j) in free_edges() :        
            r = vec(i,j)
            if in_rowspan(r,M) :
                row_coeffs = np.matrix(la.lstsq(M.T, r.T)[0])
                #print (row_coeffs)
                d[i,j] = (row_coeffs * y)[0,0]
    
    #%% COMPUTE OPTIMAL PRICES!
    reset_mutables()
    while len(free_edges())>0:
        set_next_rent_differences()
        set_implied_values()
        
    #%%
    #Compute rents (indexed by people)
    rent = la.solve(M,y).T.tolist()[0]
    rent_frame = pd.DataFrame(rent)
    rent_frame.index = housemate
    rent_frame.columns = ["Rent"]
    #rent_frame
    
    #%%
    solution = pd.concat([assignment,rent_frame], axis = 1)
     
    #%% CHECK:   
    #The utility of housemate j's room-and-rent to housemate i 
    def utility (i,j) :
        return (values.loc[housemate[i],j] - rent[s.index(j)])
    #utility(1,0)
    
#%%
    envies = pd.DataFrame({
    housemate[i] : [round(utility(i,j) - utility(i,s[i]),2) for j in range(0,n)] for i in range(0,n) 
    }).T
    
    #%%
#    print("\nEnvies:")
#    print(envies.to_string())
#    print("\nEnvies:")    
    envy_free = all([(e<=0) for e in list(envies.values.flatten())])
    if not envy_free:
        print("Warning: not all envies are negative!")

    #%%
    return (solution,envies,envy_free)

#%%
#rental_harmony(total_rent,values)

