import networkx as nx ;

filename = "/home/pear/research/dataset/Wiki-Vote.txt" ;

G = nx.read_edgelist(filename, create_using=nx.DiGraph() ) ;
print G.number_of_nodes() ;

print G.number_of_edges() ;

mylist = [] ;
for node in G.nodes():
    mylist.append(int(node)) ;

print sorted(mylist) ;
