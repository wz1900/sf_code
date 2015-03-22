import random ;
import networkx as nx ;

class Propagation:
    def __init__(self, graph):
        self.beta = 0.1 ;
        self.graph = graph ;
        self.max_step_num = 100 ;
        self.infect_dict = {} ;

    def choice_seeds(self, num):
        seeds = random.sample(G.nodes(), num) ;
        for seed in seeds:
            self.infect_dict[seed] = True ;
        print seeds ;
        return seeds ;   
 
    def count_rate(self, seeds):
        res = len(seeds)/(1.0*self.graph.number_of_nodes()) ;
        return res ;

    def infect_by_step(self, seeds, step):
        step = step + 1 ;
        print self.count_rate(seeds) ;
        if( step >= self.max_step_num ):
            return ;

        for seed in seeds:
            neighbors = self.graph.neighbors(seed) ;
            for neighbor in neighbors:
                if( self.infect_dict.has_key(neighbor) is False ):
                    if( random.random() <= self.beta ):
                        self.infect_dict[neighbor] = True ;
                        seeds.append(neighbor) ;

        self.infect_by_step(seeds, step) ;
        
if __name__ == "__main__":
    file_name = "../dataset/facebook_combined.txt" ;
    G = nx.read_edgelist(file_name) ;
    propagation = Propagation(G) ;
    seeds = propagation.choice_seeds(5) ;
    propagation.infect_by_step(seeds, 0) ;
