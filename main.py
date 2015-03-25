import numpy as np ;
import networkx as nx ;

from Propagation import Propagation ;
from Consistency import Consistency ;
from LabelPropagation import label_propagation ;
from SeeFinder import find_local_max, find_local_max_neighbors ;
from FScore import  FScore ;

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

def run_label_propagation(G, labels, run_num):
    return label_propagation(G, labels, run_num) ;

def run_propagation(G, seed_num):
    propagation = Propagation(G) ;
    seeds = propagation.choice_seeds(seed_num) ;
    infected_list = propagation.infect_by_rate(seeds) ;
    #infected_list = propagation.infect_by_step(seeds, 0) ;
    return [seeds, infected_list] ; 
   

def run_test():
    file_name = "../dataset/facebook_combined.txt" ;
    #file_name = "../dataset/test_edges.txt" ;
    G = nx.read_edgelist(file_name) ;
    print "------propagation-------"
    [gold_seeds, infected_list] = run_propagation(G, seed_num=10) ;
    print "gold_seeds:", gold_seeds ;
 
    print "------set label-------"
    labels = set_node_label(G, infected_list) ;
    #print labels ;

    #print "------consistency-------"
    #res = run_consistency(G, labels) ;
 
    print "------label pro---------"
    labels = run_label_propagation(G, labels, 100) ;
    
    #print labels;
    seeds = find_local_max(G, labels) ;
    print seeds ;
    max_neighbors = find_local_max_neighbors(G, labels, seeds) ;
    print max_neighbors ;

    fscore = FScore() ;
    fscore.increment(set(gold_seeds), set(seeds)) ;
    print "precision: ", fscore.precision();
    print "recall:", fscore.recall() ;
    print "fscore", fscore.fscore() ;
if __name__ == "__main__":
    for i in range(20):
        run_test() ;
