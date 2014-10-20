from cPickle import load, dump
from scipy.io import savemat, mmwrite
from scipy.sparse import coo_matrix

def create_compact_dicts():
    print 'compactifying...'
    sparse_to_dense, dense_to_sparse = {}, []
    i = 0
    for line in open('graph.txt'):
        # FIX id generation!!!1111
        IDs = line.split()
        for id in IDs:
            ID = int(id)
            if ID not in sparse_to_dense.keys():
                i = i + 1
                sparse_to_dense[ID] = i
                dense_to_sparse.append(ID)
    dump(sparse_to_dense, open('sparse_to_dense.pickle', 'w'), 2)
    dump(dense_to_sparse, open('dense_to_sparse.pickle', 'w'), 2)

def create_matrix():
    sparse_to_dense = load(open('sparse_to_dense.pickle'))
    print 'reading graph file and matrixifying...'
    I, J = [], []
    for line in open('graph.txt'):
        converted = [sparse_to_dense.get(int(ID)) for ID in line.split()]
        i = converted[0]
        j = converted[1]
        I.append(i)
        J.append(j)
    n = max([max(I), max(J)]) + 1
    data = [1]*len(I)
    return coo_matrix((data, (I,J)), shape=(n,n), dtype='i1')

def main():
    create_compact_dicts()
    W = create_matrix()
    savemat('W.mat', dict(W=W))

if __name__ == '__main__':
    main()
