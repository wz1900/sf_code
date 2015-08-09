import networkx as nx ;
import pprint
import community ;
import 


from BasicFunction import build_sub_graph ;

class Zang:
    def __init__(self, G, infected_list):
        self.G = G ;
        self.infected_list = infected_list ;
        self.score = {} ;
        self.c = {} ;
        self.infected_dict = {} ;
 
        for node in infected_list:
            self.infected_dict[node] = 1 ;

        for node in G.nodes():
            if( self.infected_dict.has_key(node) ):
                self.score[node] = 1 ;
                self.c[node] = 1 ;
            else:
                self.score[node] = 0 ;
                self.c[node] = 0 ;

    def _update_by_neighbors(self, G, node):
        mysum = 0 ;
        for neighbor in G.neighbors(node):
            mysum = mysum + self.score[neighbor] ;
        self.score[node] = mysum ;
        return ;

    def recover_infected_nodes(self):
        mylist = list(self.infected_list) ;
        Nstep = 3 ;
        for i in range(Nstep):
            templist = [] ;
            for node in mylist:
                 for neighbor in self.G.neighbors(node):
                     if( self.c[neighbor] == 0 ):
                         self._update_by_neighbors(self.G, neighbor);
                         templist.append(neighbor) ;
                         self.c[neighbor] = 1 ;          
            mylist = list(set(mylist + templist))  ; 
        #pprint.pprint(self.score)
 
        basescore = 4 ;
        recover_list = [] ;      
        for node in mylist:
            if( self.score[node] > basescore and self.infected_dict.has_key(node)==False ):
                recover_list.append(node) ;
        return recover_list ;

    def get_center(self, myG):
        estimate = nx.betweenness_centrality(myG) ;
        mymax = -1 ;
        nodeId = -1 ;
        for node in estimate.keys():
            estimate[node] = estimate[node]/float(myG.degree(node)+0.000001) ;
            if( estimate[node] > mymax ):
                mymax = estimate[node] ;
                nodeId = node ;
        #pprint.pprint(estimate) ;
        print "center:", nodeId ;
        return nodeId ;

    def _get_sources(self, useful_node_list):
        myGraph = build_sub_graph(self.G, useful_node_list) ;
        partition = community.best_partition(myGraph) ;
        count = 0 ;
        sourcelist = [] ;
        for com in set(partition.values()) :
            count = count + 1 ;
            list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com] ;
            tempG = build_sub_graph(self.G.copy(), list_nodes) ;
            source = self.get_center(tempG) ;
            sourcelist.append(source) ;
        print "community num:", count ; 
        #print community.modularity(partition, myGraph) ;
        return sourcelist ;

    def get_community(self):
        tt = 0 ;
        

    def get_sources(self, model="SIR"):
        total_list = list(self.infected_list) ;
        if( model == "SIR" ):
            recover_list = self.recover_infected_nodes() ;
            print "recovered num: ", len(recover_list) ;
            total_list = list(set(total_list + recover_list))  ; 
        res = self._get_sources(total_list) ;
        print "detected sources:", res ;
        return res ;
          
if __name__ == "__main__":
    file_name = "../dataset/karate.txt" ;
    G = nx.read_edgelist(file_name) ;
    infected_list = ['0','2','3','4','1','19','10'] ;
    myZang = Zang(G, infected_list) ;
    myZang.get_sources(model="SIR") ;
    #myZang.get_center() ;
    '''
    res = myZang.recover_infected_nodes() ;
    print res ;
    print infected_list ;
    '''
