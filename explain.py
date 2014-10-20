from scipy.io import loadmat
from cPickle import load
import h5py
import numpy as np

d2s = load(open('dense_to_sparse.pickle'))
i2t = load(open('ID-title_dict.pickle'))
t2i = load(open('title-ID_dict.pickle'))
s2d = load(open('sparse_to_dense.pickle'))

print len(d2s.keys())
print len(s2d.keys())
print len(i2t.keys())
print len(t2i.keys())

def load_data():
    print 'loading data...'
    U = h5py.File('../U.mat')['U'][:]
    D = h5py.File('../D.mat')['D'][:]
    print U.shape, D.shape
    return U.T, D

def concept_to_dense_id(concept):
    id_s = t2i[concept]
    return s2d[id_s]

def dense_id_to_concept(d_id):
    s_id = d2s[d_id]
    return i2t[s_id]


def similarity(p_ids, n_ids):
    U, D  = load_data()
    
    n = max(U.shape)
    x = np.zeros( (n,1) )
    nrm = len(p_ids) + len(n_ids)
    nrm = 1.0 * nrm
    for id in p_ids:
        x[id,0] = 1.0/nrm
    for id in n_ids:
        x[id,0] = -1.0/nrm
    s = U.dot(D.dot(U.T.dot(x)))
    idx = sorted(range(max(s.shape)), key=lambda k: -s[k])
    for k in range(10):
	d_id = idx[k]    
        try:
        	print s[d_id], dense_id_to_concept(d_id)
	except:
		pass	

def test(lst):
    for item in lst:
	did = concept_to_dense_id(item)
        print item, dense_id_to_concept(did)
       

def main():
    p_c = ["Russia"]
    p_n = []
    test(p_c)
    test(p_n)
    p_ids = map(concept_to_dense_id, p_c)
    n_ids = map(concept_to_dense_id, p_n)
    print len(i2t.keys())
    similarity(p_ids, n_ids)

main()

