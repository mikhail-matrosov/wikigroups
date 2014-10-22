import numpy as np
import scipy.linalg as scl
import scipy.sparse as scsp
import scipy.sparse.linalg as scspl
import scipy.io
import matplotlib.pylab as plt
import sklearn.cluster as skcl
import networkx as nx


def spectral_clustering(A, args):
    '''
    Function uses dimension reduction by spectral clustering 
    to cluster with some cluster algorithm 
    '''
    if type(A) == np.ndarray:
        G = nx.from_numpy_matrix(A)
    elif type(A) == scsp.csc.csc_matrix:
        G = nx.from_scipy_sparse_matrix(A)
    if args['show_eigenvalues']:
        laplacian_eigval = nx.laplacian_spectrum(G)
        plt.scatter(np.array(range(len(laplacian_eigval))) + 1, 
                             laplacian_eigval, marker='x', s=90)
        plt.show()
    laplacian = nx.laplacian_matrix(G)
    max_eigvals = scspl.eigs(laplacian * 1.0, return_eigenvectors=False, 
                             k=laplacian.shape[0] - 2)
    alpha = np.amax(max_eigvals)
    modif_laplacian = alpha * scsp.eye(laplacian.shape[0], 
                                       laplacian.shape[1]) - laplacian
    lap_eigval, lap_eigvec = scspl.eigs(modif_laplacian * 1.0, 
                                        k=args['dim'])
    U = lap_eigvec.real
    if args['dim'] < 1000:
        clustering = skcl.KMeans(n_clusters=args['number_of_clusters'])
        clustering.fit(U)
    else:
        clustering = skcl.MiniBatchKMeans(n_clusters=args['number_of_clusters'])
        clustering.fit(U)
    return clustering.labels_


if __name__ == '__main__':
    print "Testing..."
    test_matrix = scipy.io.loadmat('../data/test/W.mat')['W']
    input_matrix = scipy.io.loadmat('../data/A.mat')['A']
    args = {'dim': 2, 'number_of_clusters': 2, 'show_eigenvalues': True}
    cl_test = spectral_clustering(test_matrix, args)
#    cl_real = spectral_clustering(input_matrix, args)
