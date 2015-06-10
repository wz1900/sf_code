import networkx as nx ;
import numpy as np ;
from Consistency import Consistency, read_label ;

def neighbor_infect_rate(G, my_node, original_labels):
    infect_num = 0 ;
    for neighbor in G.neighbors(my_node):
        if( original_labels[int(neighbor)] > 0 ):
            infect_num = infect_num + 1 ;
    infect_rate = infect_num/( len(G.neighbors(my_node))*1.0 ) ;
    return infect_rate ;

def find_local_max_with_infect(G, seeds, labels, original_labels):
    res = [] ;
    beta = 0.5 ;
    for seed in seeds:
        seed_infect_rate = neighbor_infect_rate(G, seed, original_labels) ;
        if( seed_infect_rate !=0 and seed_infect_rate<=1.0*beta ): continue ;
        seed_val = labels[int(seed)]*seed_infect_rate ;
        seed_id = seed ;
        

        for neighbor in G.neighbors(seed):
            if( original_labels[int(neighbor)] < 0 ): continue ;
            temp_rate = neighbor_infect_rate(G, neighbor, original_labels) ;
            neighbor_val = labels[int(neighbor)]*temp_rate ;
            if( neighbor_val > seed_val ):
                seed_val = neighbor_val ;
                seed_id = neighbor ;

        res.append(seed_id) ;
    return res ;

def find_local_max_r1(G, seeds, labels, original_labels):
    return [] ;


# original method
def find_local_max(G, labels, original_labels):
    tole = 0.001 ;
    seeds = [] ;
    for node in G.nodes():
        if( original_labels[int(node)] < 0 ): continue ;
        temp = 0 ;
        for neighbor in G.neighbors(node):
            if( labels[int(node)] > labels[int(neighbor)]+tole ): temp = temp + 1 ;
        if(temp == len(G.neighbors(node)) ): seeds.append(node) ;
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
 

