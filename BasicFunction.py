import networkx as nx ;

def build_sub_graph(G, nodelist):
    resG = G.copy() ;
    mydict = {} ;
    for node in nodelist:
        mydict[node] = 1 ;
    for node in G.nodes() :
        if( mydict.has_key(node) == False ):
            resG.remove_node(node) ;
    return resG ;
