from sage.all import Graph, DiGraph
import itertools

def find_sym_struct(G,Gs,Gd,H):
	rev=G.reverse()
	vert=G.vertices()
	comb = list(itertools.combinations(vert,2))
    for e in comb:
		e=(e[0],e[1],None)
		for i in range(2):
			if e in G.edges():
				Gs.add_edge(e[0],e[1])
				if e in rev.edges():
					Gd.add_edge(e[0],e[1])
					H.add_edge(e[0],e[1],label=1)
				else:
					H.add_edge(e[0],e[1],label=2)
			elif (e[0],e[1],None) not in Gd.edges():
				H.add_edge(e[0],e[1],label=0)
			e=(e[1],e[0],None)
			print e
    """
	print "Gs"
	for e in Gs.edges():
		print e
	print "Gd"
	for e in Gd.edges():
		print e
	print "H"
	for e in H.edges():
		print e
    """
    
if __name__ == "__main__":	
	d={1:[2],2:[1],5:[1]}
	G=DiGraph(d)
	Gs=Graph()
	Gd=Graph()
	H=Graph()
	find_sym_struct(G,Gs,Gd,H)
	# modular decomposition of Gs, Gd
	
