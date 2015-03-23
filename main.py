from Propagation import Propagation ;
from Consistency import Consistency ;

import numpy as np ;
import networkx as nx ;
def set_node_label(G, infect_list):
    infect_dict = {} ;
    for node in infect_list:
        infect_dict[int(node)] = True ;

    labels = [] ;
    for i in  range(G.number_of_nodes()):
        if( infect_dict.has_key(i) ): labels.append(+1) ;
        else: labels.append(-1) ;

    return labels ;

def run_consistency(G, labels):
    labels = np.array(labels) ;
    res = Consistency(G, labels) ;
    return res ;

def run_propagation(G):
    propagation = Propagation(G) ;
    seeds = propagation.choice_seeds(5) ;
    infected_list = propagation.infect_by_step(seeds, 0) ;
    return [seeds, infected_list] ; 
   

if __name__ == "__main__":
    file_name = "../dataset/facebook_combined.txt" ;
    G = nx.read_edgelist(file_name) ;
    print "------propagation-------"
    [seeds, infected_list] = run_propagation(G) ;
    print "------set label-------"
    labels = set_node_label(G, infected_list) ;
    print labels ;
    print "------consistency-------"
    res = run_consistency(G, labels) ; 
    print res ;
