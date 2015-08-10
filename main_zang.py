from networkx import nx ;
from Zang import Zang ;
from Propagation import Propagation ;
from FScore import  FScore, active_error ;
import numpy as np ;

beta = 0.5 ;
max_infect_rate = 0.3 ;
seed_num = -1 ;

output_file = "result_zang.txt" ;

si_res_list = [] ;
sir_res_list = [] ;

def run_propagation(G, seed_num):
    propagation = Propagation(G, beta, max_infect_rate) ;
    seeds = propagation.choice_seeds(seed_num) ;
    infected_list = propagation.infect_by_rate(seeds, 0) ;
    #infected_list = propagation.infect_by_step(seeds, 0) ;
    return [seeds, infected_list] ; 

def get_score(gold_seeds, source_si, source_sir):
    fscore = FScore() ;
    fscore.increment(set(gold_seeds), set(source_si)) ;
    si_res_list.append(fscore) ;

    fscore = FScore() ;
    fscore.increment(set(gold_seeds), set(source_sir)) ;
    sir_res_list.append(fscore) ;

def write_score_file(model_name, reslit):
    precision_list = [] ;
    recall_list = [] ;
    fscore_list = [] ;
    r0 = 0 ;
    r0_2 = 0 ; 
    for temp in reslit:
        precision_list.append(temp.precision()) ;
        recall_list.append(temp.recall()) ;
        fscore_list.append(temp.fscore()) ;
        if( temp.test == seed_num ): r0 = r0 + 1 ;
        if( temp.test >= seed_num*0.8 and temp.test<=seed_num*1.2 ): r0_2=r0_2+1 ;

    precision = np.mean(precision_list) ;
    recall = np.mean(recall_list) ;
    fscore = np.mean(fscore_list) ;

    f = open(output_file, 'a') ;
    mylen = float(len(precision_list)) ;
    print >> f, model_name, ":", precision, recall, fscore, r0/mylen, r0_2/mylen; 
    f.close() ;


def run_test(G):
    print "------propagation-------"
    [gold_seeds, gold_infected_list] = run_propagation(G, seed_num) ;
    print "gold_seeds:", gold_seeds ;
     
    myZang = Zang(G.copy(), gold_infected_list) ;
    print "------zang si model ------"
    source_si = myZang.get_sources(model="SI") ;     

    print "------zang sir model ------"
    source_sir = myZang.get_sources(model="SIR") ; 
    get_score(gold_seeds, source_si, source_sir) ;

def my_run(G, set_seed_num, run_num):
    global seed_num ;
    seed_num = set_seed_num ;

    global si_res_list ;
    si_res_list = [] ;
    global sir_res_list ;
    sir_res_list = [] ;
    for i in range(run_num):
        print "------------------", i , "-------------------"
        run_test(G) ;

    write_score_file('SI', si_res_list) ;
    write_score_file('SIR', sir_res_list) ;

if __name__ == "__main__":
    import time ;
    start = time.clock()

    file_name = "../dataset/facebook_combined.txt" ;
    #file_name = "../dataset/CA-GrQc_nor.txt" ;
    #file_name = "../dataset/karate.txt" ;
    #file_name = "../dataset/friendships-hamster_new.txt" ;
    #file_name = "../dataset/hamster_full_new.txt" ;
    #file_name = "../dataset/blog_edges.txt" ;

    G = nx.read_edgelist(file_name) ;

    seedList = [3] ;
    run_num = 200 ;
    f = open(output_file, 'w') ;  
    f.close() ;
    
    for seed in seedList:
        f = open(output_file, 'a') ;  
        print >> f, "***** seed_num=", seed, "*****" ;
        f.close() ;
        print "***** seed_num=", seed, "*****" ;
        my_run(G, seed, run_num) ;
    f = open(output_file, 'a') ;  
    print >> f, "\n" ;
    f.close() ;

    elapsed = (time.clock() - start)
    print("Time used:",elapsed)

