from sage.all import Graph, DiGraph
from Trees import Tree
from modularDecomposition import *
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
			

"""
"Graph Decompositions and factorizing permutations",
C. Chapelle, M. Habib, F. de Montgolfier

Computation of the modular decomposition tree of a digraph given a factorizing permutation 
"""

# Step 1: find the parenthesized factorizing permutation given the factorizing permutation
def parenthesized_fact_perm(nodes,G):
	sigma=nodes[:]
	fc={}
	lc={}
	for i in range(len(nodes)-1):
		for j in range(0,i):
			if is_cutter(nodes[j],nodes[i],nodes[i+1],G):
				#print nodes[j],nodes[i]
				sigma.insert(sigma.index(nodes[j]),'(')
				sigma.insert(sigma.index(nodes[i])+1,')')
				fc[nodes[i]]=nodes[j]
				break
		for j in reversed(range(i+2,len(nodes))): 
			if is_cutter(nodes[j],nodes[i],nodes[i+1],G):
				#print nodes[i+1],nodes[j]
				sigma.insert(sigma.index(nodes[i+1]),'(')
				sigma.insert(sigma.index(nodes[j])+1,')')
				lc[nodes[i]]=nodes[j]
				break
	print fc
	print lc
	fracture_tree(sigma,fc,lc,G)

def is_cutter(x,a,b,G):
	"""
	Checks if the vertex x is a cutter of the set of vertices S={a,b}, of the given graph G
	
	A vertex x is cutter of a set S if S is not a module of the induced graph G(SU{x})
	i.e. x does not belong to S and a,b have different adjacency relation with x
	"""
	if G.has_edge(x,a) and (not G.has_edge(x,b)):
		return True
	if G.has_edge(a,x) and (not G.has_edge(b,x)):
		return True
	if (not G.has_edge(x,a)) and G.has_edge(x,b):
		return True
	if (not G.has_edge(a,x)) and (G.has_edge(b,x)):
		return True
	return False
	

# Step 2: Find the fracture tree
def fracture_tree(sigma,fc,lc,G):
	frac_tree=Tree('n')
	current=frac_tree
	for i in sigma:
		if i=='(':
			current.add_child(Tree('n'))
			current=current.children[-1]
		elif i==')':
			current=current.parent
		else:
			current.add_child(Tree(i))
	# Step 3,4
	postorder_marking(frac_tree,fc,lc)
	print " "
	# Step 5
	recovering(frac_tree,G)
	twin_detection(frac_tree,fc,lc,G)
	# Step 6
	delete_weak_modules(frac_tree)
	frac_tree.print_tree()

# Step 3: Module recognition
# Step 4: Dummy nodes deletion
def postorder_marking(tree,fc,lc):
	"""
	Find the 	
	"""
	for child in tree.children:
		postorder_marking(child,fc,lc)
	if tree.name!='n':
		tree.info=[nodes.index(tree.name),nodes.index(tree.name)]
		#print tree.info
	else:
		minimum=tree.children[0].info[0]
		maximum=tree.children[0].info[-1]
		for child in tree.children:
			if minimum>child.info[0]:
				minimum=child.info[0]
			if child!=tree.children[-1] and child.name in fc.keys() and minimum>nodes.index(fc[child.name]):
				minimum=nodes.index(fc[child.name])
			if maximum<child.info[-1]:
				maximum=child.info[-1]
			if child!=tree.children[-1] and child.name in lc.keys() and maximum<nodes.index(lc[child.name]) :
				maximum=nodes.index(lc[child.name])
			# Delete dummy node 1 (the ones that has only one child)
			if len(child.info)>1 and child.info[1]=='d1':
				tree.children[tree.children.index(child)]=child.children[0]
			# Delete dummy node 2 
			if len(child.info)>1 and child.info[1]=='d2':
				pos = tree.children.index(child)
				tree.children[pos]=child.children[-1]
				for i in reversed(child.children[:-1]):
					tree.children.insert(pos,i)
		tree.info=[minimum,maximum]

		# Mark dummy nodes 

		# Dummy node 1: has only one child
		if len(tree.children)==1:
			tree.info.insert(1,'d1')
			tree.children[0].parent=tree.parent

		# Dummy node 2: its cutter set does not belong to the set of leaves of the node "tree"
		#               and hence itis not a module 
		if tree.children[0].name=='n':
			if tree.info[0]<tree.children[0].info[0]:
				tree.info.insert(1,'d2')
		else:
			if tree.info[0]<nodes.index(tree.children[0].name):
				tree.info.insert(1,'d2')
		if tree.children[-1].name=='n':
			if tree.info[-1]>tree.children[-1].info[-1]:
				tree.info.insert(1,'d2')
		else:
			if tree.info[-1]>nodes.index(tree.children[-1].name):
				tree.info.insert(1,'d2')
		if tree.info[1]=='d2':
			for child in tree.children:
				child.parent=tree.parent

# Step 5: recoveringthe merged modules
def recovering(tree,G):
	for child in tree.children:
		recovering(child,G)
	if tree.name=='n':
		modules=range(len(tree.children))
		vertices=[nodes[tree.children[i].info[0]:tree.children[i].info[1]+1] for i in modules]
		a={key: 0 for key in modules}
		#module_adjacency(tree,a,vertices)
		for i in modules:
			for j in modules:
				if i!=j:
					for h in vertices[i]: 
						if len( set(G.neighbors_out(h)).intersection(vertices[j]))>0:
							a[i]+=1
							break
					
		#print ('vert',vertices)
		#print a.values()
		if a.values()==[0]*(len(vertices)):
			tree.name='parallel'
			#tree.print_tree()
		elif a.values()==[len(vertices)-1]*(len(vertices)):
			tree.name='series'
		elif set(a.values()).issuperset(range(len(vertices))) : # possibly something is missing
			tree.name='order'
		else:
			tree.name='prime'
			
	

def twin_detection(tree,fc,lc,G):
	for child in tree.children:
		twin_detection(child,fc,lc,G)
	if tree.name=='prime':#tree.name=='prime':
		twin=[]
		for i in range(tree.info[0],tree.info[1]):
			if tree.children[i-tree.info[0]].name!=tree.children[-1].name: 
				if not tree.children[i-tree.info[0]].name  in ['prime','series','parallel','order']:
					if (not (nodes[i] in fc.keys())) and (not (nodes[i]  in lc.keys())): #nodes.index(fc[i])>nodes.index(i):
						twin.append(i) ## nodes [i], [i+1] are twins
					elif twin!=[]:
						#print twin
						twin_node(tree,twin,G) # create the node
						twin=[] # reset the list
				else:
					
					if twin: 
						twin_node(tree,twin,G)
						#print twin
						twin=[] # reset the list
			else: break
		

def twin_node(tree,twin,G):
	# true twins,false twins, half twins
	true_twin=0
	half_twin=0
	false_twin=0
	for i in twin:
		if G.has_edge(nodes[i],nodes[i+1]) and G.has_edge(nodes[i+1],nodes[i]):
			true_twin+=1
		elif G.has_edge(nodes[i],nodes[i+1]) or G.has_edge(nodes[i+1],nodes[i]):
			half_twin+=1
		elif (not G.has_edge(nodes[i],nodes[i+1])) and (not G.has_edge(nodes[i+1],nodes[i])):
	 		false_twin+=1
	if   true_twin==len(twin):  label='series' # true twins
	elif half_twin==len(twin):  label='order' # half twins
	elif false_twin==len(twin): label='parallel' # false twins
	else: label=None
	if label: 
		i=0
		twin.append(twin[-1]+1)
		for j in range(len(tree.children)):
			if i<len(twin) and tree.children[j].name==nodes[twin[i]]:
				if i==0:
					temp_tree=Tree(label)
					tree.children[j].parent=temp_tree
					temp_tree.add_child(tree.children[j])
					tree.children[j]=temp_tree
				else:
					tree.children[j].parent=temp_tree
					temp_tree.add_child(tree.children[j])
					tree.children[j]=None
				i+=1
		while None in tree.children: tree.children.remove(None)
				
		


	

# Step 6: Delete weak modules
def delete_weak_modules(tree):
	"""
	The only weak modules are the order modules

	"""
	for child in tree.children:
		delete_weak_modules(child)
	for i in tree.children:
		if tree.name=='order'and tree.name==i.name:
			pos=tree.children.index(i)
			tree.children[pos]=i.children[-1]
			i.children[-1].parent=tree
			for j in reversed(i.children[:-1]):
				tree.children.insert(pos,j)
				j.parent=tree    	
  

    
if __name__ == "__main__":	
	d={1:[3,4,5], 2:[1], 3:[2,4,5], 4:[2], 5:[4,2], 6:[7,8,9,10], 7:[8,9,10], 8:[9,10], 10:[11,12,13,14], 11:[9,10,14], 12:[9,10,11,13], 13:[9,10,11,12], 14:[9,10,11]}
	G=DiGraph(d)
	Gs=Graph()
	Gd=Graph()
	H=Graph()
	find_sym_struct(G,Gs,Gd,H)
	TGs=modular_decomposition(Gs)
	TGd=modular_decomposition(Gd)
	Th=modular_decomposition(H)
	print TGs
	print TGd
	print Th
	# modular decomposition of Gs, Gd
	# factorizing permutation of the graph G is 1,...,14
	nodes=range(1,15)
	parenthesized_fact_perm(nodes,G)
	print (" ")
