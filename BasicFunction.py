import networkx as nx ;
import igraph;

def build_sub_graph(G, nodelist):
    resG = G.copy() ;
    mydict = {} ;
    for node in nodelist:
        mydict[node] = 1 ;
    for node in G.nodes() :
        if( mydict.has_key(node) == False ):
            resG.remove_node(node) ;
    return resG ;

def convert_networkx_igraph(myNxg):
    nx_ig_dict = {} ; # myNxg.node(int) ---> ig.node
    ig_nx_dict = {} ;

    nodelist = [] ;
    for node in myNxg.nodes():
        nodelist.append(int(node)) ;
    nodelist = sorted(nodelist) ;

    startId = 0 ;
    for node in nodelist:
        nx_ig_dict[node] = startId ;
        ig_nx_dict[startId] = node ;
        startId = startId + 1 ;

    edgelist = [] ;
    for edge in myNxg.edges():
        temp = (nx_ig_dict[int(edge[0])], nx_ig_dict[int(edge[1])]) ;
        edgelist.append(temp) ;

    return [edgelist, nx_ig_dict, ig_nx_dict] ;

def igraph_get_community(myNxg):
    [edges, nx_ig_dict, ig_nx_dict] = convert_networkx_igraph(myNxg) ;
    ig=igraph.Graph(edges) ;
    
    old_modual = -1 ;
    node_comm_list = [] ;
    for k in range(2, myNxg.number_of_nodes()):
        comm = ig.community_leading_eigenvector(clusters=k)
        temp = comm.modularity ;
        print "K is:", k, " modularity: ", temp ;
        if( abs(temp-old_modual) < 0.000001 ): break ;
        old_modual = temp ;
        node_comm_list = [] ;
        for entry in comm:
            #print entry ;
            templist = [] ;
            for node in entry:
                templist.append( unicode( ig_nx_dict[node] ) ) ;
            node_comm_list.append(templist) ;
    nx_list = [] ;
    for mylist in node_comm_list:        
        resNxg = build_sub_graph(myNxg.copy(), mylist) ;
        print "community size:", len(resNxg.nodes()) ;
        nx_list.append(resNxg) ;

    return nx_list ;

if __name__ == "__main__":
    file_name = "../dataset/karate.txt" ;
    G = nx.read_edgelist(file_name) ;
    #get_community(G) ;
    infected_list = ['0','2','3','4','1','19','10'] ;
    subgraph = build_sub_graph(G, infected_list) ;
    #res = convert_networkx_igraph(subgraph) ;
    res = igraph_get_community(subgraph) ;
    print res ;
