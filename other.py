
def _get_sources(self, useful_node_list):
    myGraph = build_sub_graph(self.G, useful_node_list) ;
    partition = community.best_partition(myGraph) ;
    count = 0 ;
    sourcelist = [] ;
    for com in set(partition.values()) :
        count = count + 1 ;
        list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com] ;
        tempG = build_sub_graph(self.G.copy(), list_nodes) ;
        source = self.get_center(tempG) ;
        sourcelist.append(source) ;
    print "community num:", count ; 
    #print community.modularity(partition, myGraph) ;
    return sourcelist ;


def get_community(myNxg):
    edges = myNxg.edges() ;
    int_edges = [] ;
    for edge in edges:
        temp = (int(edge[0]), int(edge[1])) ;
        int_edges.append(temp) ;

    ig=igraph.Graph(int_edges) ;
     
    #print ig.degree() ;
    old_modual = -1 ;
    for k in range(2, myNxg.number_of_nodes()):
        print "K is:", k ;
        comm = ig.community_leading_eigenvector(clusters=k)
        temp = comm.modularity ;
        print temp ;
        #if( abs(temp-old_modual) < 0.00000000000001 ): break ;
        old_modual = temp ; 
        for entry in comm:
            print entry


if __name__ == "__main__":
    file_name = "../dataset/karate.txt" ;
    G = nx.read_edgelist(file_name) ;
    #get_community(G) ;
    infected_list = ['0','2','3','4','1','19','10'] ;
    subgraph = build_sub_graph(G, infected_list) ;
    #res = convert_networkx_igraph(subgraph) ;
    res = get_comm(subgraph) ;
    print res ;
