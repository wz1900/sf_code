import networkx as nx ;
import random ;
import numpy as np ;
from Consistency import Consistency, read_label ;

def seed_select_unconnected(G, num):
    edgeSet = G.edges()
    total_num = 0 ;
    while 1:
        total_num = total_num + 1 ;
        seeds = random.sample(G.nodes(), num) ;
        flag = True ;
        for seed1 in seeds:
            if( flag == False ): break ;
            for seed2 in seeds:
                if( seed1!=seed2 and (seed1, seed2) in edgeSet ): 
                    flag = False ;
                    break ;
        if( flag == True ): break ;
        if( total_num > 50 ): break ;
    print "total num is: ", total_num ;
    return seeds ;


def is_connected(G, seeds, node):
    edgeSet = G.edges()
    for seed in seeds:
        if( node!=seed and (seed, node) in edgeSet ): return True ;
    return False ;
            
def seed_clean(G, seeds):
    print "------cleaning-----"
    seeds = set(seeds) ;
    edgeSet = G.edges()
    tempSet = set(seeds) ;
    res = [] ;
    while len(tempSet) >= 1 :
        temp = tempSet.pop() ;
        if( is_connected(G, seeds, temp) is False ):
            res.append(temp) ;
        seeds = set(tempSet) ;
    print res ;        
    return res ;

# get teh min neighbor rate of a seed should be
def get_min_neighbor_rate(G, seeds, original_labels):
    res = [] ;
    for seed in seeds:
        seed_infect_rate = neighbor_infect_rate(G, seed, original_labels) ;
        #print "Seed: %s, infect_rate: %f", seed, seed_infect_rate ;
        res.append( seed_infect_rate ) ;
    temp = 0.8 * np.mean(res) ;
    return temp ;


def neighbor_infect_rate(G, my_node, original_labels):
    infect_num = 0 ;
    for neighbor in G.neighbors(my_node):
        if( original_labels[int(neighbor)] > 0 ):
            infect_num = infect_num + 1 ;
    infect_rate = infect_num/( len(G.neighbors(my_node))*1.0 ) ;
    return infect_rate ;

def find_local_max_with_infect(G, seed, labels, original_labels, checktype, min_neigh_rate):
    seed_infect_rate = neighbor_infect_rate(G, seed, original_labels) ;
    seed_val = labels[int(seed)]*seed_infect_rate ;
    seed_id = seed ;
    #print "checktype is ", checktype ;

    if( checktype=='r1' or checktype=='r1r2' ):
        #print "-------rule 1-----------" 
        for neighbor in G.neighbors(seed):
            if( original_labels[int(neighbor)] < 0 ): continue ;
            temp_rate = neighbor_infect_rate(G, neighbor, original_labels) ;
            neighbor_val = labels[int(neighbor)]*temp_rate ;
            if( neighbor_val > seed_val ):
                seed_val = neighbor_val ;
                seed_id = neighbor ;

    if( checktype=='r2' or checktype=='r1r2' ):
        #print "-------rule 2-----------"
        ''' 
        if( seed_infect_rate !=0 and seed_infect_rate<=min_neigh_rate ): 
            return None ;
        else:
            return seed_id ;
        '''
        neighbor_dict = {} ;
        neighbor_dict[seed_id] = 1 ;
        for neighbor in G.neighbors(seed_id):
            neighbor_dict[neighbor] = 1 ;

        myset = set() ;
        for neighbor in G.neighbors(seed_id):
            for temp in G.neighbors(neighbor):
                if( neighbor_dict.has_key(temp) is False  and original_labels[int(temp)] >0 ): myset.add(temp) ;

        num = 0 ;
        for temp in myset:
            if( checktype=='r2' and labels[int(seed_id)] > labels[int(temp)] ): num = num + 1 ;
            if( checktype=='r1r2' and labels[int(seed_id)]*neighbor_infect_rate(G, seed_id, original_labels) > labels[int(temp)]*neighbor_infect_rate(G, temp, original_labels) ): num = num + 1 ;

        if( num >= 0.95*len(myset) ): return seed_id ; 
        else: return None ; 

    return seed_id ;


def find_local_max_rules(G, seeds, labels, original_labels, average_rate, checktype=None):
    if( checktype is None ): return find_local_max(G, labels, original_labels) ;
    min_neigh_rate = get_min_neighbor_rate(G, seeds, original_labels) ;
    print "min_neigh_rate is:", min_neigh_rate ; 
    reslist = [] ;
    for seed in seeds:
        res = find_local_max_with_infect(G, seed, labels, original_labels, checktype, min_neigh_rate) ;
        if( res is not None ): reslist.append(res) ;   

    return reslist ;

# original method
def find_local_max(G, labels, original_labels):
    tole = 0.0000001 ;
    seeds = [] ;
    for node in G.nodes():
        if( original_labels[int(node)] < 0 ): continue ;
        #print "xxxxx a node xxxx" ;
        #print node, original_labels[int(node)] ;
        #print "----neighbors-----"
        temp = 0 ;
        for neighbor in G.neighbors(node):
            #print labels[int(node)],  labels[int(neighbor)], original_labels[int(neighbor)] ;
            if( labels[int(node)] > labels[int(neighbor)] or original_labels[int(neighbor)]<0 ): 
                temp = temp + 1 ;
        if(temp == len(G.neighbors(node)) ): seeds.append(node) ;
        #print temp, len(G.neighbors(node)) ;
        #if(temp == len(G.neighbors(node)) ): seeds.append(node) ;
    return seeds ;

def find_local_max_neighbors(G, labels, seeds):
    res = [] ;
    for seed in seeds:
        max_neighbor = -1000000 ;
        max_id = -1 ;
        for neighbor in G.neighbors(seed):
            if( labels[int(neighbor)] > max_neighbor ):
                max_neighbor = labels[int(neighbor)] ;
                max_id = neighbor ;
        num = 0 ;
        for neighbor in G.neighbors(seed):
            if( neighbor == max_id ): continue ;
            if( max_neighbor > 1.3*labels[int(neighbor)] ): num = num + 1 ;
        if( num == len(G.neighbors(seed))-1): res.append(max_id) ;

    return res ;
        
if __name__ == "__main__":

    file_name = "../dataset/test_edges.txt" ;
    G = nx.read_edgelist(file_name) ;

    label_file = "../dataset/test_edges_labels.txt" ;
    labels = read_label(label_file) ;
    labels = Consistency(G, np.array(labels)) ;

    seeds = find_local_max(G, labels) ;
    print seeds ;
 

