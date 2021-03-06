import networkx as nx ;
from Consistency import laplace_normalize ;
from Consistency import read_label ;

def get_trans_matrix(G, beta):
    n = G.number_of_nodes() ;
    myMatrix = np.zeros((n, n)) ;
    for edge in G.edges():
        myMatrix[int(edge[0]), int(edge[1])] = beta ;
        myMatrix[int(edge[1]), int(edge[0])] = beta ;


def si_label_propagation(G, Y, run_num=10):
    print "-----getting laplace------"
    S = laplace_normalize(G) ;
    print "-----laplace has been calculated------"
    labels = Y[:] ;
    for i in range(run_num):
        #print "------label pro once--------"
        labels = run_once(G, S, labels, Y) ;
        #print [2*x for x in labels];
    return labels ;

def run_once(G, S, labels, Y):
    alpha = 0.5 ;
    labels_next = labels[:] ;

    for node in G.nodes():
        temp = 0 ;
        for neighbor in G.neighbors(node):
            temp = temp + S[int(node), int(neighbor)]*labels[int(neighbor)] ;
        labels_next[int(node)] = alpha*temp + (1-alpha)*Y[int(node)] ;

    return labels_next ; 

if __name__ == "__main__":
    file_name = "../dataset/test_edges.txt" ;
    G = nx.read_edgelist(file_name) ;

    label_file = "../dataset/test_edges_labels.txt" ;
    labels = read_label(label_file) ;
    #labels = np.array(labels) ;

    F = label_propagation(G, labels) ;
    print F ;
