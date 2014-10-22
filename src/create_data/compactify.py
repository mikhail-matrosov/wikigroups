import cPickle
from scipy.io import savemat, mmwrite
from scipy.sparse import coo_matrix


def create_compact_dicts(out_dir, in_dir):
    print 'compactifying...'
    sparse_to_dense, dense_to_sparse = {}, {}
    f = open(in_dir + 'graph.txt')
    lines = f.readlines()
    f.close()
    
    mk_step = 20
    step = len(lines) / mk_step
    k = 0
    for line in lines:
        k = k + 1
        if k % step == 0:
            print "%d%% done" % (100 / mk_step * k / step)
        # FIX id generation!
        IDs = line.split()
        for id in IDs:
            ID = int(id)
            if ID not in sparse_to_dense:
                i = len(dense_to_sparse)
                sparse_to_dense[ID] = i
                dense_to_sparse[i] = ID
    cPickle.dump(sparse_to_dense, open(out_dir + 'sparse_to_dense.pickle',
                                       'wb'), 2)
    cPickle.dump(dense_to_sparse, open(out_dir + 'dense_to_sparse.pickle',
                                       'wb'), 2)
    
    print 'compactifying... Done.'


def create_matrix(in_dir):
    sparse_to_dense = cPickle.load(open(in_dir + 'sparse_to_dense.pickle', 
                                        'rb'))
    person_id = {}
    person_ind = 0
    with open(in_dir + 'ID-title_dict.pickle', 'rb') as f:
        id2title = cPickle.load(f)
    with open(in_dir + 'person_id.txt') as f:
        for line_id in f:
            try:
                t = id2title[int(line_id)]
                if int(line_id) in person_id:
                    continue
                person_id[int(line_id)] = person_ind
                person_ind += 1
            except KeyError:
                continue
    cPickle.dump(person_id, open(in_dir + 'person_id2ind.pickle', 'wb'), 2)
    print "Number of person's id", len(person_id)
    print 'reading graph file and matrixifying...'
    
    # *_p variables related to person's variables.
    I, J = [], []
    I_p, J_p = [], []
    for line in open(in_dir + 'graph.txt'):
        converted = [sparse_to_dense.get(int(ID)) for ID in line.split()]
        ids = [int(ID) for ID in line.split()]
        i = converted[0]
        j = converted[1]
        I.append(i)
        J.append(j)
        if ids[0] in person_id and ids[1] in person_id:
            I_p.append(person_id[ids[0]])
            J_p.append(person_id[ids[1]])
    n = max([max(I), max(J)]) + 1
    m = max([max(I_p), max(J_p)]) + 1
    data = [1] * len(I)
    data_p = [1] * len(I_p)
    W = coo_matrix((data, (I, J)), shape=(n, n), dtype='i4')
    A = coo_matrix((data_p, (I_p, J_p)), shape=(m, m), dtype='i4')
    print 'Number of cross-links from person to person', len(I_p)
    print 'reading graph file and matrixifying... Done.'
    return W, A


def main(out_dir, in_dir='../../data/'):
    create_compact_dicts(out_dir, in_dir)
    W, A = create_matrix(in_dir)
    savemat(out_dir + 'W.mat', dict(W=W), oned_as='column')
    savemat(out_dir + 'A.mat', dict(A=A), oned_as='column')
    # rdkl:
    # Maybe here should be: savemat('W.mat', dict(W=W), oned_as='column')

if __name__ == '__main__':
    main('../../data/')
