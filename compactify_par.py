from cPickle import load, dump
from scipy.io import savemat, mmwrite
from scipy.sparse import coo_matrix
import multiprocessing

class Worker(multiprocessing.Process):

    def __init__(self, queue, results):
         multiprocessing.Process.__init__(self):
         self.q = queue
         self.results = results
         self.sparse_to_dense =    

    def run(self):
        while True:
            try:
                lineno, linecontents = self.q.get()
            except Queue.Empty:
                break
            converted = [sparse_to_dense.get(int(ID)) for ID in line.split()]
             i = converted[0]
             j = converted[1]
            self.results.put((i, j))


def create_compact_dicts():
    print 'compactifying...'
    sparse_to_dense, dense_to_sparse = {}, []
    i = 0
    for line in open('graph.txt'):
        # FIX id generation!!!1111
        ID = int(line.split()[0])
        if ID not in sparse_to_dense.keys():
            i = i + 1
            sparse_to_dense[ID] = i
            dense_to_sparse.append(ID)
    dump(sparse_to_dense, open('sparse_to_dense.pickle', 'w'), 2)
    dump(dense_to_sparse, open('dense_to_sparse.pickle', 'w'), 2)

def create_matrix():
    q = multiprocessing.Queue()
    results = multiprocessing.JoinableQueue()

    for line in open('graph.txt').readlines():
        q.put((line))

    for _ in xrange(4):
        w = Worker(q, results)
        w.start()

    I, J = []
    while True:
        try:
            i, j = results.get()
        except Queue.Empty:
        break
    I.append(i)
    J.append(j)
    results.task_done()

    results.join()
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
