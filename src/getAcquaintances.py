import numpy as np
import scipy

def getAcquaintances(A, clusters, person = 'Barack_Obama',
    outputfile = '../data/people_in_the_cluster.txt',
    t2i = '../data/title-ID_dict.pickle',
    i2t = '../data/ID-title_dict.pickle',
    pid2ind = '../data/person_id2ind_6800.pickle', 
    printRating = 0):
        
    t2i = scipy.load(t2i)
    pid2ind = scipy.load(pid2ind)

    if person in t2i:
        ix = t2i[person]
        if ix:
            print 'Wiki ID is', ix
        else:
            print 'Wiki ID is None!'
            return
    else:
        print 'Person isn\'t found in t2i!'
        return
    
    # get person's dense-dense id (in 15k array)
    ix = pid2ind[ix]
    
    if ix:
        print 'In dense matrix he/she is', ix
    else:
        print 'Peron\'s id not found in t2i!'
        return
    
    # find the cluster that contains the person
    cluster = np.where(map(lambda x: ix in x, clusters))[0]
    ids = np.array(clusters[cluster[0]])
    
    if len(cluster):
        print person, 'is acquaintant with', len(ids), 'people'
    else:
        print 'Person isn\'t found in any cluster!'
        return
    
    # create inverse index-to-person dictionary
    ind2pid = dict(zip(pid2ind.values(), pid2ind.keys()))
    
    # get ratings
    ratings = A[ids,:][:,ids].sum(axis=1) # only inside cluster
    ratings = np.array(ratings).flatten()
    
    # sort people by rating
    ix = ratings.argsort()[::-1]
    ids = ids[ix]
    ratings = ratings[ix]
    
    i2t = scipy.load(i2t)
    ids = map(ind2pid.get, ids)
    
    # print all the people in this cluster
    if printRating:
        string = '\n'.join([i2t[i]+", "+str(r) for i, r in zip(ids, ratings)])
    else:
        string = '\n'.join(map(i2t.get, ids))
    
    # write to file
    f = open(outputfile, 'w')
    f.write(string)
    f.close()
    
