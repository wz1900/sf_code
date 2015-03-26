
def active_error(G, gold_infect, test_infect):
    #print gold_infect ;
    #print test_infect ;
    gold_infect_dict = {} ;
    test_infect_dict = {} ;
    for temp in gold_infect: gold_infect_dict[temp] = True ;
    for temp in test_infect: test_infect_dict[temp] = True ;
    res = 0 ;
    for node in G.nodes():
        if( gold_infect_dict.has_key(node) and test_infect_dict.has_key(node) ): continue ;
        if( gold_infect_dict.has_key(node) is False and test_infect_dict.has_key(node) is False ): continue ;
        res = res + 1 ;
    return res ;

class FScore:
  "Compute F1-Score based on gold set and test set."

  def __init__(self):
    self.gold = 0.0
    self.test = 0.0
    self.correct = 0.0

  def increment(self, gold_set, test_set):
    "Add examples from sets."
    self.gold += len(gold_set)
    self.test += len(test_set)
    self.correct += len(gold_set & test_set)

  def fscore(self): 
    pr = self.precision() + self.recall()
    if pr == 0: return 0.0
    return (2 * self.precision() * self.recall()) / pr

  def precision(self): 
    if self.test == 0: return 0.0
    return self.correct / self.test

  def recall(self): 
    if self.gold == 0: return 0.0
    return self.correct / self.gold 

if __name__ == "__main__":
    gold = [1,2,3,4,9];
    test = [0,2,3, 5] ;
    fscore = FScore() ;
    fscore.increment(set(gold), set(test)) ;
    print fscore.precision(), fscore.recall() ;
    print fscore.fscore() ;
