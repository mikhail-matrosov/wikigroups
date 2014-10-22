import numpy as np
import scipy

f = open('../../data/person_id.txt')
persons_sparse_ids = np.array(map(int, f.readlines()), np.int32)

W = scipy.io.loadmat('../../data/W.mat')['W']
s2d = scipy.load('../../data/sparse_to_dense.pickle')

# persons dense ids
ix = map(s2d.get, persons_sparse_ids)
persons_sparse_ids_existent = [sid for i,sid in zip(ix, persons_sparse_ids) if i!=None]
ix = [i for i in ix if i!=None] # throw away Nones
ix = np.array(ix, np.int32)

A = W[ix, :][:, ix]
scipy.io.savemat('../../data/A.mat', {'A':A})

persons_sparse_id_to_15329 = dict(zip(persons_sparse_ids_existent, ix))
scipy.save('../../data/persons_sparse_id_to_15329', persons_sparse_id_to_15329)