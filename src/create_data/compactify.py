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
        # FIX id generation!!!1111
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
    print 'reading graph file and matrixifying...'
    I, J = [], []
    for line in open(in_dir + 'graph.txt'):
        converted = [sparse_to_dense.get(int(ID)) for ID in line.split()]
        i = converted[0]
        j = converted[1]
        I.append(i)
        J.append(j)
    n = max([max(I), max(J)]) + 1
    data = [1] * len(I)
    print 'reading graph file and matrixifying... Done.'
    return coo_matrix((data, (I, J)), shape=(n, n), dtype='i4')


def main(out_dir, in_dir='../../data/'):
    create_compact_dicts(out_dir, in_dir)
    W = create_matrix(in_dir)
    savemat(out_dir + 'W.mat', dict(W=W), oned_as='column')
    # rdkl:
    # Maybe here should be: savemat('W.mat', dict(W=W), oned_as='column')

if __name__ == '__main__':
    main()
