import numpy as np ;
import networkx as nx ;

from Propagation import Propagation ;
from Consistency import Consistency ;
from LabelPropagation import label_propagation ;
from SeeFinder import find_local_max, find_local_max_neighbors, neighbor_infect_rate, find_local_max_with_infect ;
from FScore import  FScore, active_error ;

beta = 0.5 ;
max_infect_rate = 0.3 ;

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
    res = Consistency(G, labels, beta) ;
    return res ;

def run_label_propagation(G, labels, run_num):
    return label_propagation(G, labels, run_num) ;

def run_propagation(G, seed_num):
    propagation = Propagation(G, beta, max_infect_rate) ;
    seeds = propagation.choice_seeds(seed_num) ;
    infected_list = propagation.infect_by_rate(seeds) ;
    #infected_list = propagation.infect_by_step(seeds, 0) ;
    return [seeds, infected_list] ; 

def test_active_error(G, test_seeds, gold_infect_list):
    propagation = Propagation(G, beta, max_infect_rate) ;
    test_infect_list = propagation.infect_by_rate(test_seeds) ; 
    res = active_error(G, gold_infect_list, test_infect_list) ;
    return res ;

def run_test():
    file_name = "../dataset/facebook_combined.txt" ;
    #file_name = "../dataset/CA-GrQc_nor.txt" ;
    #file_name = "../dataset/karate.txt" ;
    #file_name = "../dataset/test_edges.txt" ;
    G = nx.read_edgelist(file_name) ;
    print "------propagation-------"
    [gold_seeds, gold_infected_list] = run_propagation(G, seed_num=10) ;
    print "gold_seeds:", gold_seeds ;
    
    print "------set label-------"
    original_labels = set_node_label(G, gold_infected_list) ;
    #print labels ;

    print "------consistency-------"
    labels = run_consistency(G, original_labels) ;
    #print "------label pro---------"
    #labels = run_label_propagation(G, original_labels, 100) ;
    
    #print labels;
    seeds = find_local_max(G, labels, original_labels) ;
    print "consistency seeds: ", seeds ;
    new_seeds = find_local_max_with_infect(G, seeds, labels, original_labels) ;
    print "with infect rate:", new_seeds, "\n" ;
    print "xxxxxx gold seeds xxxxx"
    for seed in gold_seeds:
        print seed, labels[int(seed)], neighbor_infect_rate(G, seed, original_labels);
    print "000000 new seeds 00000"
    for seed in new_seeds:
        print seed, labels[int(seed)], neighbor_infect_rate(G, seed, original_labels);
        '''
        print "-----neigbhors------"
        for temp in G.neighbors(seed):
            infect_rate = neighbor_infect_rate(G, temp, original_labels) ;
            print temp, labels[int(temp)], infect_rate ;
        print ""
        '''
    #print " " ;

    '''print seeds ;
    for temp in seeds:
        print labels[int(temp)], ;
    print " " ;
    '''
    #max_neighbors = find_local_max_neighbors(G, labels, seeds) ;
    #print max_neighbors ;
    fscore = FScore() ;
    fscore.increment(set(gold_seeds), set(seeds)) ;
    write_result(fscore, "orig_est_seeds.txt", len(set(seeds))) ;

    new_fscore = FScore() ;
    new_fscore.increment(set(gold_seeds), set(new_seeds)) ;
    write_result(new_fscore, "new_est_seeds.txt", len(set(new_seeds))) ;

def write_result(fscore, destfile, seed_len):
    f = open(destfile,'a')
    print >>f, "precision:", fscore.precision();
    print >>f, "recall:", fscore.recall() ;
    print >>f, "fscore:", fscore.fscore() ;
    print >>f, "length:", seed_len ;
    #active_error = test_active_error(G, set(seeds), gold_infected_list) ;
    #print "active_error", active_error ;
    f.close() ; 

if __name__ == "__main__":
    import time ;
    start = time.clock()
    for i in range(100):
        print "------------------", i , "-------------------"
        run_test() ;
    elapsed = (time.clock() - start)
    print("Time used:",elapsed)
