import networkx as nx
import scipy.linalg as scl
import scipy.sparse as scsp
import scipy.sparse.linalg as scspl
import numpy as np
import matplotlib.pylab as plt
from sklearn.cluster import KMeans

def spectral_clustering(A, dim, cluster_alg, args):
    '''
    '''
    # A = scsp.csr_matrix(A)
    # G = nx.from_scipy_sparse_matrix(A)
    G = nx.from_numpy_matrix(A)
    laplacian_eigval = nx.laplacian_spectrum(G)
    plt.scatter(np.array(range(len(laplacian_eigval))) + 1, laplacian_eigval, marker = 'x', s = 90)
    plt.show()
    laplacian = nx.laplacian_matrix(G)
    max_eigvals = scspl.eigs(laplacian * 1.0, return_eigenvectors=False, k = laplacian.shape[0] - 2)
    alpha = np.amax(max_eigvals)
    modif_laplacian = alpha*scsp.eye(laplacian.shape[0], laplacian.shape[1]) - laplacian
    lap_eigval, lap_eigvec = scspl.eigs(modif_laplacian*1.0, k = dim)
    U = lap_eigvec.real
    print U
    
#    np_lapl_eigval, np_lapl_eigv = scl.eig(laplacian.todense())
#    id_min_eigval = np.argsort(np_lapl_eigval)
#    idx_min_eigval = np.argsort(np_lapl_eigval)[0:2]
#    U = np_lapl_eigv[idx_min_eigval].transpose()
#    print U
#     eigval, laplacian_eigvec = scspl.eigsh(1.0 * laplacian, k = 32)
    clustering = KMeans(n_clusters=args['num_clusters'])
    clustering.fit(U)
    print clustering.labels_
    return clustering.labels_
