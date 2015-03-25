import networkx as nx ;
import numpy as np ;
from Consistency import Consistency, read_label ;

def find_local_max(G, labels):
    seeds = [] ;
    for node in G.nodes():
        temp = 0 ;
        for neighbor in G.neighbors(node):
            if( labels[int(node)] > labels[int(neighbor)] ): temp = temp + 1 ;
        if(temp == len(G.neighbors(node)) and labels[int(node)]>0): seeds.append(node) ;
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
 

