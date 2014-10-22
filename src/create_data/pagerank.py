import cPickle
from scipy.io import loadmat
from numpy.linalg import norm
from numpy import ones, divide, argsort, array
from itertools import islice, count

def pagerank(A, d=.85, tol=1e-3):
    n = A.shape[0]
    D = A.astype('i4').sum(1)
    D[D == 0] = n
    At = A.transpose()
    v = ones((n, 1)) / n
    for i in count(1):
        prev = v
        v = d * (At * divide(v, D)) + (1 - d) / n
        err = norm(v - prev)
        print 'i =', i, 'err =', err
        if err < tol:
            break
    return v


def load_data(in_dir):
    print 'loading data...'
    A = loadmat(in_dir + 'W.mat')['W']
    d2s = cPickle.load(open(in_dir + 'dense_to_sparse.pickle', 'rb'))
    i2t = cPickle.load(open(in_dir + 'ID-title_dict.pickle', 'rb'))
    return A, d2s, i2t


def top_k(in_dir, k=10, v=None):
    '''
    Does all titles if k < 0
    '''
    A, d2s, i2t = load_data(in_dir)
    if v is None:
        print 'doing pagerank'
        v = pagerank(A)
    print 'sorting'
    t = reversed(argsort(array(v)[:, 0]))  # pageranked list of dense IDs

    def get_title(x):
        ''' convert dense ID to sparse ID, then sparse ID to title '''
        i = d2s[x]
        try:
            return i2t[i]
        except KeyError:
            return 'TITLE_ERROR'
    return (get_title(x) for x in islice(t, k)) if k >= 0 else (get_title(x)
                                                                for x in t)


def main(in_dir='../../data/'):
    for i, title in enumerate(top_k(in_dir), 1):
        print('%2d %s' % (i, title))

if __name__ == '__main__':
    main('../../data/')
