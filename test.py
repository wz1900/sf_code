num = 0 ;
filename = "nohup.out" ;
for line in open(filename).readlines():
    line = line.strip() ;
    if( len(line)==0 ): continue ;
    mylist = line.split(" ") ;
    if( mylist[0].strip() == 'precision:' ): print mylist[1], ;
    if( mylist[0].strip() == 'recall:' ): print mylist[1], ;
    if( mylist[0].strip() == 'fscore:' ): 
        print mylist[1], ;
    if( mylist[0].strip() == 'active_error' ): 
        print mylist[1] ;
        #print "\n" ;
        num = num +1 ;
    
    if line[0]=='[': print len(mylist), ;
print num ;

