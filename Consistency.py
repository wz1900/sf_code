import networkx as nx ;
import numpy as np ;
from math import sqrt ;
import time ;

def si_normalize(G):
    #print "-----get laplace normalize matrix-------"
    n = G.number_of_nodes() ;
    myMatrix = np.zeros((n, n)) ;
    beta = 0.5 ;
    
    tMatrix = np.zeros((n, n)) ;
    for edge in G.edges():
        myMatrix[int(edge[0]), int(edge[1])] = beta ;
        myMatrix[int(edge[1]), int(edge[0])] = beta ;

        tMatrix[int(edge[0]), int(edge[0])] += beta ;
        tMatrix[int(edge[1]), int(edge[1])] += beta ;
    #print myMatrix ;
    S = np.zeros((n,n)) ;
    for edge in G.edges():
        i = int(edge[0]) ;
        j = int(edge[1]) ;
        S[i,j] = myMatrix[i,j]/((tMatrix[i,i])*(tMatrix[j,j]))  ;
        S[j,i] = S[i,j] ;
    #print S ;
    return S ;


def laplace_normalize(G, beta):
    #print "-----get laplace normalize matrix-------"
    n = G.number_of_nodes() ;
    myMatrix = np.zeros((n, n)) ;
    
    tMatrix = np.zeros((n, n)) ;
    for edge in G.edges():
        myMatrix[int(edge[0]), int(edge[1])] = beta ;
        myMatrix[int(edge[1]), int(edge[0])] = beta ;

        tMatrix[int(edge[0]), int(edge[0])] += beta ;
        tMatrix[int(edge[1]), int(edge[1])] += beta ;
    #print myMatrix ;
    # a faster one
    S = np.zeros((n,n)) ;
    for edge in G.edges():
        i = int(edge[0]) ;
        j = int(edge[1]) ;
        S[i,j] = myMatrix[i,j]/(sqrt(tMatrix[i,i])*sqrt(tMatrix[j,j]))  ;
        S[j,i] = S[i,j] ;
    #print S ;
    return S ;

# not used
def direct_laplace_normalize(G, beta):
    #print "-----get laplace normalize matrix-------"
    n = G.number_of_nodes() ;
    myMatrix = np.zeros((n, n)) ;
    
    tMatrix = np.zeros((n, n)) ;
    for edge in G.edges():
        start = int(edge[0]) ;
        end = int(edge[1]) ;
        myMatrix[end, start] = beta ;
        #tMatrix[int(end, end] += beta ;
    # print myMatrix ;
    # a faster one

    S = np.zeros((n,n)) ;
    for edge in G.edges():
        i = int(edge[0]) ;
        j = int(edge[1]) ;
        S[i,j] = myMatrix[i,j]/(sqrt(tMatrix[i,i])*sqrt(tMatrix[j,j]))  ;
    #print S ;
    return S ;
'''
def Consistency(G, labels, beta):
    alpha = 0.5 ;
    n = G.number_of_nodes() ;
    S = laplace_normalize(G, beta) ;
    #print "------laplace is calculated-------" ;
    F = np.dot(np.linalg.inv(np.eye(n) - alpha*S), labels) ;
    #print F ;
'''

def Consistency(G, labels, beta):
    alpha = 0.5 ;
    n = G.number_of_nodes() ;
    S = laplace_normalize(G, beta) ;
    #print S ;
    #print "------laplace is calculated-------" ;
    F = np.dot(np.linalg.inv(np.eye(n) - alpha*S), labels) ;
    #print F ;
    print "##geting F##"
    return F ;

def read_label(filename):
    labels = [] ;
    for line in open(filename).readlines():
        line = line.strip() ;
        mylist = line.split(" ") ;
        labels.append(float(mylist[1])) ;

    return labels ;

if __name__ == "__main__":
    file_name = "../dataset/test_edges.txt" ;
    G = nx.read_edgelist(file_name) ;

    label_file = "../dataset/test_edges_labels.txt" ;
    labels = read_label(label_file) ;
    labels = np.array(labels) ;

    start = time.time()
    for i in range(1):
        Consistency(G, labels, 0.5) ;
    end = time.time()
    print "run time: ", end-start
