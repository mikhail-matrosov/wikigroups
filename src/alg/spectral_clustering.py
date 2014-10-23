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
        print 'Building graph...'
        G = nx.from_numpy_matrix(A)
        laplacian = nx.laplacian_matrix(G)
    elif type(A) == scsp.csc.csc_matrix:
        print 'Building graph...'
        G = nx.from_scipy_sparse_matrix(A)
        laplacian = nx.laplacian_matrix(G)
    print 'Start finding reduction...'
    max_eigvals = scspl.eigs(laplacian * 1.0, return_eigenvectors=False, 
                             k=args['dim'] + 10)
    alpha = np.amax(max_eigvals)
    modif_laplacian = alpha * scsp.eye(laplacian.shape[0], 
                                       laplacian.shape[1]) - laplacian
    lap_eigval, lap_eigvec = scspl.eigs(modif_laplacian * 1.0, 
                                        k=20)
    if args['show_eigenvalues']:
        print 'Show eigenvalues...'
        plt.scatter(np.array(range(len(lap_eigval))) + 1, np.sort(-lap_eigval.real + alpha), marker='x', s=90)
        plt.show()
    U = lap_eigvec[:, 0:args['dim']].real
    print 'Start clustering...'
    if U.shape[0] < 1000:
        clustering = skcl.KMeans(n_clusters=args['number_of_clusters'])
        clustering.fit(U)
    else:
        clustering = skcl.MiniBatchKMeans(n_clusters=args['number_of_clusters'])
        clustering.fit(U)
    center_person_cluster_id = clustering.labels_[args['index']]
    center_person_cluster = [i for i in xrange(len(clustering.labels_)) 
                             if clustering.labels_[i] == center_person_cluster_id]
    
    cluster = [[i for i in xrange(len(clustering.labels_)) if clustering.labels_[i] == j] 
                for j in xrange(args['number_of_clusters'])]
    return center_person_cluster, cluster


if __name__ == '__main__':
    print "Testing..."
    test_matrix = scipy.io.loadmat('../data/test/W.mat')['W']
    # input_matrix = scipy.io.loadmat('../data/A.mat')['A']
    args = {'dim': 3, 'number_of_clusters': 3, 'show_eigenvalues': False}
    cl_cent_person, cl_test = spectral_clustering(test_matrix, args)
    # cl_cent_person, cl_real = spectral_clustering(input_matrix, args)
    with open('../../data/cluster_id.txt' , 'w') as f:
        for i in cl_test:
            f.write(str(i) + '\n')
            
    print 'Testing... Done.'
