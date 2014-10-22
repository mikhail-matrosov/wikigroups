import numpy as np
import scipy

t2i = scipy.load('../data/title-ID_dict.pickle')
pid2ind = scipy.load('../data/person_id2ind.pickle')


def getAcquaintances(clusters, person = 'Barack_Obama', outputfile = '../data/people_in_the_cluster.txt'):
    print person
    if person in t2i:
        ix = t2i[person]
        
        if ix:
            print 'Wiki ID is', ix
        else:
            print 'Peron\'s id not found!'
        
        ix = pid2ind[ix]
        
        if ix:
            print 'In dense matrix he/she is', ix
        else:
            print 'Peron\'s id not found in t2i!'
        
        cluster = np.where(map(lambda x: ix in x, clusters))[0]
        
        if len(cluster):
            print person, 'is acquaintant with ', len(clusters[cluster[0]]), 'people'
        else:
            print 'Person isn\'t found in any cluster!'
        
    else:
        print 'Person isn\'t found in t2i!'
    
    ind2pid = dict(zip(pid2ind.values(), pid2ind.keys()))
    
    # print all the people in this cluster
    i2t = scipy.load('../data/ID-title_dict.pickle')
    ids = map(ind2pid.get, clusters[cluster[0]])
    string = '\n'.join(map(i2t.get, ids))
    
    f = open(outputfile, 'w')
    f.write(string)
    f.close()