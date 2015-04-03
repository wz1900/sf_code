import random ;
import networkx as nx ;

class Propagation:
    def __init__(self, graph, beta):
        self.beta = beta ;
        self.graph = graph ;
        self.max_step_num = 3 ;
        self.max_infect_rate = 0.3 ;
        self.infect_dict = {} ;

    def choice_seeds(self, num):
        seeds = random.sample(self.graph.nodes(), num) ;
        for seed in seeds:
            self.infect_dict[seed] = True ;
        #print seeds ;
        return seeds ;   
 
    def count_rate(self):
        res = len(self.infect_dict)/(1.0*self.graph.number_of_nodes()) ;
        return res ;

    def get_all_seeds(self):
        seeds = [] ;
        for temp in self.infect_dict:
            seeds.append(temp) ;
        return seeds ;

    def infect_by_rate(self, seeds):
        print "----infect once-----"
        print self.count_rate() ;
        for seed in seeds:
            neighbors = self.graph.neighbors(seed) ;
            for neighbor in neighbors:
                if( self.count_rate() > self.max_infect_rate ): 
                    print "active nodes number:", len(self.infect_dict) ;
                    print self.count_rate() ;
                    return self.get_all_seeds() ;

                if( self.infect_dict.has_key(neighbor) is False ):
                    if( random.random() <= self.beta ):
                        self.infect_dict[neighbor] = True ;
        
        seeds = self.get_all_seeds() ;
        return self.infect_by_rate(seeds) ;


    def infect_by_step(self, seeds, step):
        print "seeds number:", len(seeds)
        step = step + 1 ;
        print self.count_rate() ;
        if( step >= self.max_step_num ): return seeds;

        for seed in seeds:
            neighbors = self.graph.neighbors(seed) ;
            for neighbor in neighbors:
                if( self.infect_dict.has_key(neighbor) is False ):
                    if( random.random() <= self.beta ):
                        self.infect_dict[neighbor] = True ;
        seeds = self.get_all_seeds() ;
        return self.infect_by_step(seeds, step) ;
        
if __name__ == "__main__":
    file_name = "../dataset/facebook_combined.txt" ;
    G = nx.read_edgelist(file_name) ;
    print "nodes number: ", len(G.nodes()) ;
    propagation = Propagation(G) ;
    seeds = propagation.choice_seeds(5) ;
    #seeds = propagation.infect_by_step(seeds, 0) ;
    seeds = propagation.infect_by_rate(seeds) ;
    print len(seeds) ;
