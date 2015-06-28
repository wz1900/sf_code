seed_num = 5 ;
num = 0 ;
filename = "orig_est_seeds.txt" ;
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

#print "\n".join(length_list) ;
ok_num1 = 0 ;
ok_num2 = 0 ;
for temp in length_list:
    if( int(temp)  == seed_num ): ok_num1 = ok_num1 + 1 ;
    if( int(temp)>=seed_num*0.8 and int(temp)<=seed_num*1.2 ): ok_num2 = ok_num2+1 ;

print ok_num1/(len(length_list)*1.0),
print ok_num2/(len(length_list)*1.0) ;
