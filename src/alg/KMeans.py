import numpy as np


def KMeans(A, args):
    '''
    Function extracts clusters in k-means manner. First it selects k random
    centers, the rest of the vertices are assigned to the closest group.
    Input:
    A - adjacent matrix of wiki-graph
    number_of_clusters
    Output:
    cluster - list of the row index of the vertices from the cluster
    '''
    
    N = A.shape[0]
    K = args['number_of_clusters'] # it is K-means, isn't it?
    N_ITERATIONS = args['max_number_of_iterations']
    
    # cluster_ids[0,:] = 0, its a workaround for argmax
    clusters_membership = np.zeros((K+1, N), np.int32)
    
    # make an initial guess - K different random indexes
    initial_centers = np.random.choice(N, K, replace=False)
    for i,k in enumerate(initial_centers):
        clusters_membership[i,k+1] = 1
    
    # iterate until converge
    for iteration in xrange(N_ITERATIONS):
        print 'iteration #%d' % (iteration+1,)
        dists = A.dot(clusters_membership.T)
        ix = dists.argmax(1) # ids where to assign each vertex
        nz = np.where(ix)[0] # non-zero indexes
        
        clusters_membership[:,nz] = 0
        for i in nz:
            clusters_membership[ix[i], i] = 1
        
    # organize return
    clusters = [np.where(clusters_membership[k+1,:])[0] for k in range(K)]
    return clusters