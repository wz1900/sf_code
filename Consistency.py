import networkx as nx ;
import numpy as np ;

def Consistency(G, labels):
    beta = 0.5 ;
    n = G.number_of_nodes() ;
    myMatrix = np.zeros((n, n)) ;
    
    for edge in G.edges():
        myMatrix[int(edge[0]), int(edge[1])] = beta ;
        myMatrix[int(edge[1]), int(edge[0])] = beta ;

    tMatrix = np.zeros((n, n)) ;
    mysum = myMatrix.sum(axis=1) ;
    for i in range(n):
        tMatrix[i, i] = mysum[i] ; 

    #temp = np.exp(tMatrix, 1.0/2) ;
    temp = tMatrix**(1.0/2) ;

    temp = np.linalg.inv(temp) ;

    S = np.dot(np.dot(temp, myMatrix), temp) ;
    F = np.dot(np.linalg.inv(np.eye(n)-0.5*S), labels) ;
    print F ;
    return F ;

def read_label(filename):
    labels = [] ;
    for line in open(filename).readlines():
        line = line.strip() ;
        mylist = line.split(" ") ;
        labels.append(float(mylist[1])) ;

    return labels ;

'''
file_name = "../dataset/test_edges.txt" ;
G = nx.read_edgelist(file_name) ;

label_file = "../dataset/test_edges_labels.txt" ;
labels = read_label(label_file) ;
labels = np.array(labels) ;

Consistency(G, labels) ;
'''
