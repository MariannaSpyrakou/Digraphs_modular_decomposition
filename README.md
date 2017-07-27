# Digraphs_modular_decomposition

#Given a directed graph computes its modular decomposition.

Step 1: ()
                     
       Given graph G, compute the undirected graphs: 
       Gs: edge (u,v) is in Gs iff edge (u,v) or (v,u) is in G
       Gd: edge (u,v) is in Gd iff edge (u,v) and (v,u) is in G
       H: edge (u,v)=0 if edge (u,v) is a non-edge
          edge (u,v)=1 if edge (u,v) is an edge in both Gs,Gd
          edge (u,v)=2 if edge (u,v) is an edge in Gs but not in Gd
