import numpy as np ;
import networkx as nx ;

from Propagation import Propagation ;
from Consistency import Consistency, laplace_normalize ;
from LabelPropagation import label_propagation ;
from SeedFinder import find_local_max, find_local_max_neighbors, neighbor_infect_rate, find_local_max_rules, seed_clean;
from FScore import  FScore, active_error ;

beta = 0 ;
max_infect_rate = 0.3 ;
seed_num = -1 ;
temp_result_files = ["orig_est_seeds.txt", "r1_est_seeds.txt", "r2_est_seeds.txt", "r1r2_est_seeds.txt"] ;
output_file = "result.txt" ;
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

def run_label_propagation(G, labels, run_num, nor_matrix):
    return label_propagation(G, labels, run_num, nor_matrix) ;

def run_propagation(G, seed_num):
    propagation = Propagation(G, beta, max_infect_rate) ;
    seeds = propagation.choice_seeds(seed_num) ;
    infected_list = propagation.infect_by_rate(seeds, 0) ;
    #infected_list = propagation.infect_by_step(seeds, 0) ;
    return [seeds, infected_list] ; 

def test_active_error(G, test_seeds, gold_infect_list):
    propagation = Propagation(G, beta, max_infect_rate) ;
    test_infect_list = propagation.infect_by_rate(test_seeds, 0) ; 
    res = active_error(G, gold_infect_list, test_infect_list) ;
    return res ;

def run_test(G, nor_matrix=None):
    print "------propagation-------"
    [gold_seeds, gold_infected_list] = run_propagation(G, seed_num) ;
    print "gold_seeds:", gold_seeds ;
    
    #print "------set label-------"
    original_labels = set_node_label(G, gold_infected_list) ;
    #print labels ;

    #print "------consistency-------"
    #labels = run_consistency(G, original_labels) ;
    #print "------label pro---------"
    labels = run_label_propagation(G, original_labels, 5, nor_matrix) ;
    
    #print labels;
    seeds = find_local_max(G, labels, original_labels) ;
    print "consistency seeds: ", seeds ;
    #seeds = seed_clean(G, seeds) ;
    #print "consistency seeds cleaned :", seeds, "\n" ;
    #if( )
    #new_seeds = find_local_max_with_infect(G, seeds, labels, original_labels) ;
    #print "with infect rate:", new_seeds, "\n" ;

    r1_seeds = find_local_max_rules(G, seeds, labels, original_labels, beta, checktype='r1') ;
    print "with r1:", r1_seeds, "\n" ;

    r2_seeds = find_local_max_rules(G, seeds, labels, original_labels, beta, checktype='r2') ;
    print "with r2:", r2_seeds, "\n" ;
    
    r1r2_seeds = find_local_max_rules(G, seeds, labels, original_labels, beta, checktype='r1r2') ;
    print "with r1r2:", r1r2_seeds, "\n" ;

    print "xxxxxx gold seeds xxxxx"
    for seed in gold_seeds:
        print seed, labels[int(seed)], neighbor_infect_rate(G, seed, original_labels);
    print "000000 r1r2_seeds 00000"
    for seed in r1r2_seeds:
        print seed, labels[int(seed)], neighbor_infect_rate(G, seed, original_labels);
        '''
        print "-----neigbhors------"
        for temp in G.neighbors(seed):
            infect_rate = neighbor_infect_rate(G, temp, original_labels) ;
            print temp, labels[int(temp)], infect_rate ;
        print ""
        '''

    fscore = FScore() ;
    fscore.increment(set(gold_seeds), set(seeds)) ;
    write_result(fscore, "orig_est_seeds.txt", len(set(seeds))) ;

    r1_fscore = FScore() ;
    r1_fscore.increment(set(gold_seeds), set(r1_seeds)) ;
    write_result(r1_fscore, "r1_est_seeds.txt", len(set(r1_seeds))) ;

    r2_fscore = FScore() ;
    r2_fscore.increment(set(gold_seeds), set(r2_seeds)) ;
    write_result(r2_fscore, "r2_est_seeds.txt", len(set(r2_seeds))) ;  

    r1r2_fscore = FScore() ;
    r1r2_fscore.increment(set(gold_seeds), set(r1r2_seeds)) ;
    write_result(r1r2_fscore, "r1r2_est_seeds.txt", len(set(r1r2_seeds))) ;  

def write_result(fscore, destfile, seed_len):
    f = open(destfile,'a')
    print >>f, "precision:", fscore.precision();
    print >>f, "recall:", fscore.recall() ;
    print >>f, "fscore:", fscore.fscore() ;
    print >>f, "length:", seed_len ;
    #active_error = test_active_error(G, set(seeds), gold_infected_list) ;
    #print "active_error", active_error ;
    f.close() ;
 
def my_run(G, set_beta, set_seed_num, run_num, nor_matrix=None):
    import os ;
    from Estimate import get_score ;
    global beta ;
    beta = set_beta ;
    global seed_num ;
    seed_num = set_seed_num ;

    for temp_file in temp_result_files:
        os.remove(temp_file) if os.path.exists(temp_file) else None

    for i in range(run_num):
        print "------------------", i , "-------------------"
        run_test(G, nor_matrix) ;

    f = open(output_file, 'a') ;
    for temp_file in temp_result_files:
        res = get_score(temp_file, seed_num) ;
        print >> f, temp_file, ":", res ; 
        os.remove(temp_file) ;
    f.close() ;

if __name__ == "__main__":
    import time ;
    start = time.clock()

    #file_name = "../dataset/facebook_combined.txt" ;
    #file_name = "../dataset/CA-GrQc_nor.txt" ;
    #file_name = "../dataset/karate.txt" ;
    #file_name = "../dataset/friendships-hamster_new.txt" ;
    #file_name = "../dataset/hamster_full_new.txt" ;
    file_name = "../dataset/blog_edges.txt" ;
    G = nx.read_edgelist(file_name) ;
    nor_matrix = laplace_normalize(G, beta=1) ;
    
    betaList = [0.1, 0.3, 0.5, 0.7, 0.9] ;
    #betaList = [0.1, 0.3, 0.5] ;
    seedList = [5] ;
    run_num = 5 ;
    f = open(output_file, 'w') ;  
    f.close() ;
    for beta in betaList:
        f = open(output_file, 'a') ;  
        print >> f, "----------------beta=", beta, "------------------" ;
        print  "----------------beta=", beta, "------------------" ;
        f.close() ;
        for seed in seedList:
            f = open(output_file, 'a') ;  
            print >> f, "***** seed_num=", seed, "*****" ;
            f.close() ;
            print "***** seed_num=", seed, "*****" ;
            my_run(G, beta, seed, run_num, nor_matrix) ;
        f = open(output_file, 'a') ;  
        print >> f, "\n" ;
        f.close() ;
    elapsed = (time.clock() - start)
    print("Time used:",elapsed)
