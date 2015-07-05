import networkx as nx ;

#filename = "/home/pear/seed_finder/dataset/facebook_combined.txt" ;
filename = "/home/pear/seed_finder/dataset/blog_edges.txt" ;
#filename = "/home/pear/seed_finder/dataset/hamster_full.txt" ;

G = nx.read_edgelist(filename, create_using=nx.Graph() ) ;
print nx.number_connected_components(G) ;

print G.number_of_nodes() ;

print G.number_of_edges() ;

mylist = [] ;
for node in G.nodes():
    mylist.append(int(node)) ;

print sorted(mylist) ;
