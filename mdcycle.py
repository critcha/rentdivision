# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 11:42:17 2015

@author: andrew
"""

def argmin (lst,fun) :
    vals = [fun(x) for x in lst]
    min_value = min(vals)
    min_index = vals.index(min_value)
    return lst[min_index]

def min_density_cycle(vertices,weight_dict,length_dict,error_tolerance=0) :
    n = len(vertices)        
    W = weight_dict
    L = length_dict
    all_pairs = [(i,j) for i in vertices for j in vertices]
    distinct_pairs = [(i,j) for i in vertices for j in vertices if i != j]
    m = {(i,j,l) : float("inf") 
            for (i,j) in all_pairs 
            for l in range(0,n+1)}        
    for (i,j) in distinct_pairs:
        m[i,j,L[i,j]] = W[i,j]   
    def is_valid_path(lst) :
        if len(lst) == 0:
            return true
        elif lst[0] == lst[-1]:
            return len(set(lst)) == len(lst)-1
        else:
            return len(set(lst)) == len(lst)
    def edges_of(path) :
        return [(path[i],path[i+1]) for i in range(0,len(path)-1)]
    def length_of(path): 
        return sum([L[ij] for ij in edges_of(path)])
    def weight_of(path):
        return sum([W[ij] for ij in edges_of(path)])
    def density_of(path):
        if length_of(path) == 0:
            return float("inf")
        else:
            return weight_of(path)/float(length_of(path))
    #s will be a dictionary storing the shortest paths "seen so far"
    #example: if the shortest path from 1 to 5 discovered so far is
    #[(1,2),(2,6),(6,4),(4,5)], we'll store that as the list
    #s[(1,5)] = [1,2,6,4],
    #where the '5' is omitted from the end of the list
    #for convenient concatenations
    f = dict({})     
    for (i,j) in distinct_pairs:
            f[i,j,1] = [i]   
    for k in vertices:
        for i in vertices:
            for j in vertices:
                for l1 in range(1,n+1):
                    for l2 in range(1,n+1-l1):
                        if (i,k,l1) in f and (k,j,l2) in f and is_valid_path(f[i,k,l1]+f[k,j,l2]+[j]):
                            new_m = density_of(f[i,k,l1] + f[k,j,l2] + [j])                    
                            if new_m < m[i,j,l1+l2] :
                                f[i,j,l1+l2] = f[i,k,l1] + f[k,j,l2] #concatenating paths
                                m[i,j,l1+l2] = new_m        
    #print("Test point 2 - negative cycle checks")
    # Check for a negative-length cycle
    neg_wt_cycles = []            
    for i in vertices:
        for l in range(1,n):
            if m[i,i,l] < -error_tolerance:
                neg_wt_cycles.append((m[i,i,l],f[i,i,l]))                
    if len(neg_wt_cycles) > 0 :
        print("Wardning: Negative weight cycles found:")
        print(neg_wt_cycles)
    cycles_found = [f[i,j,l] + [i] for (i,j,l) in f if i == j]
    min_cycle = argmin(cycles_found,density_of)
    min_density = density_of(min_cycle)
    #print("Test point 3 - finding shortest shortest path")
    # Return shortest shortest path
    return (min_density,min_cycle) 

        #%%