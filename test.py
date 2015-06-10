num = 0 ;
#filename = "nohup.out" ;
filename = "new_est_seeds.txt" ;
precision_list = [] ;
recall_list = [] ;
fscore_list = [] ;
length_list = [] ;
for line in open(filename).readlines():
    line = line.strip() ;
    if( len(line)==0 ): continue ;
    mylist = line.split(" ") ;
    if( mylist[0].strip() == 'precision:' ): 
        print mylist[1], ;
        precision_list.append( float(mylist[1]) ) ;

    if( mylist[0].strip() == 'recall:' ): 
        print mylist[1], ;
        recall_list.append( float(mylist[1]) ) ;

    if( mylist[0].strip() == 'fscore:' ): 
        print mylist[1] ;
        fscore_list.append( float(mylist[1]) ) ;

    if( mylist[0].strip() == 'active_error' ): 
        print mylist[1] ;
        #print "\n" ;
        num = num +1 ;
    
    if line[0]=='[': print len(mylist), ;
    if( mylist[0].strip() == 'length:' ): 
        print mylist[1] ;
        length_list.append(mylist[1]) ;
#print num ;
print "-----------average-----------"
print sum(precision_list)/float(len(precision_list)) , sum(recall_list)/float(len(recall_list)), sum(fscore_list)/float(len(fscore_list)) ;

print "\n".join(length_list) ;
