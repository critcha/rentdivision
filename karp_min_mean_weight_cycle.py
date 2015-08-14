# Adapted from http://binetacm.wikidot.com/algo:minmeancycle
# by Christoph Dürr
 
import sys
from string import *
 
""" A graph is defined as a dictionnary G, mapping a vertex to its neighbors.
    For every arc (u,v) -- so with v in G[u] -- we have the labels
        b[u,v] the capacity of the arc
        f[u,v] the current flow along the arc
        c[u,v] the cost of the arc ( negative profit )
 
    here G_in[v] contains the vertices u such that there is an arc (u,v)
    and G_out[u] contains the vertices v such that there is an arc (u,v)
"""
 
def minMeanCycle(G_in, G_out, f, b, c):
   """ input: graph G, with arc flow, f, arc capacity b and arc cost c.
       output: a cycle in the residual graph of minimal mean cost
       assumes graph is connected and contains at least one vertex
       algorithm by Dick Karp from 1976
       complexity is O(n*m) where n is the number of nodes and m the number of arcs
   """
   V = G_out.keys()      # vertices
   n = len(V)            # number of vertices
   s = V[0]              # arbitrary root
   POSINFTY = float("inf")
   NEGINFTY = -float("inf")
   d = { (0,s): 0 }      # d maps (k,v) to the shortest path from s to v of length k
   p = { (0,s): s }      # p maps (k,v) to the predecessor on that path
 
   for k in range(1,n+1):       # from 1 to n
     for v in V: 
       for u in G_in[v]:        # what is the cost of going to v through pred. u ?
         if (k-1,u) in d:
           alt = d[k-1,u] + c[u,v]
           if (k,v) not in d or d[k,v] > alt:
              d[k,v] = alt
              p[k,v] = u
 
   # read from d the value min_v max_k (d[n,v] - d[k,v]) / (n-k)
   # best contains (value, argmin_v) 
   min_v    = POSINFTY
   argmin_v = s
   for v in V:
      max_k = NEGINFTY
      for k in range(n):     # from 0 to n-1
        if (n,v) in d and (k,v) in d:
           alt = (d[n,v] - d[k,v]) / float(n-k)     # floating point div
           if max_k < alt:
              max_k = alt
      if min_v > max_k and max_k > NEGINFTY:
         min_v = max_k
         argmin_v = v
 
   if min_v == POSINFTY:    # found no cycle at all, 
      return None           # which is impossible if graph is strongly connected
 
   print("argmin_v=" + str(argmin_v))
   print("d       =" + str(d))
   print("p       =" + str(p))
                            # unroll backwards the path from argmin_v to s
                            # and detect any cycle, which must exist by its length
   cycle = []
   j = {}
   v = argmin_v
   for i in range(n, 0, -1):
     u = p[i, v]
     j[v] = len(cycle)
     cycle.append((u,v))
     if u in j:             # detect a cycle through u, keep only suffix
       cycle = cycle[j[u]:]
       cycle.reverse()      # put in normal order
       return cycle
     v = u