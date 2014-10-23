import cPickle
import scipy
from scipy.io import savemat, loadmat

import numpy as np


#-----------------------------------------------------------------------------
def choose_submatrix(size):
    A = loadmat('../../data/A.mat')['A']
    A = scipy.sparse.dok_matrix(A)
    A.keys()[:10]
    
    number_of_removed_rows = A.shape[0] - size
    removed_rows = {}
    
    i = 0
    while i < number_of_removed_rows:
        d = {i : 0 if not i in removed_rows else 10**6 
             for i in xrange(A.shape[0])}
        for a, b in A.keys():
            if not (a in removed_rows or b in removed_rows):
                d[a] += 1
                d[b] += 1
        
        values = np.array(d.values())
        zeros = np.sum(values == 0)
        if np.sum(values == 0) > 0:
            for index, item in enumerate(values == 0):
                if item:
                    removed_rows[index] = 0
            i += zeros
            print "Zero values removed. ",
        else:
            bad_index = np.argmin(values)
            removed_rows[bad_index] = 0
            i += 1
            print "Non-zero removed.    ",
        
        print "Removed indexes:", len(removed_rows), "(requested", \
            number_of_removed_rows, ")"
    
    val = [(i, j) for (i, j) in A.keys() if not i in removed_rows
                                        and not j in removed_rows]
    
    
    # Translate from new B index to old A index.
    tr_dict = dict(enumerate([i for i in xrange(A.shape[0]) 
                        if not i in removed_rows]))
    
    tr_dict_reversed = {v: k for k, v in tr_dict.items()}
    
    
    rows = [tr_dict_reversed[i] for (i, _) in val]
    cols = [tr_dict_reversed[j] for (_, j) in val]
    data = [1 for (_, _) in val]

    
    B = scipy.sparse.coo_matrix((data, (rows, cols)), shape = (len(tr_dict), 
                                                               len(tr_dict)))
    
    f = open('../../data/person_id2ind.pickle', 'rb')
    id_to_ind = cPickle.load(f)
    f.close()
    
    ind_to_id = {v: k for k, v in id_to_ind.items()}
    
    new_dict = {ind_to_id[tr_dict[i]] : i for i in tr_dict}
    
    f = open('../../data/person_id2ind_'+  str(A.shape[0] - 
                                               len(removed_rows))\
             +  '.pickle', 'wb')
    
    
    cPickle.dump(new_dict, f)    
    f.close()
    
    savemat("../../data/" + 'A_' + str(A.shape[0] - len(removed_rows)) + \
            '.mat', dict(A = B), oned_as='column')
    print B.shape
    
    
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    choose_submatrix(6800)
