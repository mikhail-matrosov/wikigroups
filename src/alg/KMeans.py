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
    K = args['number_of_clusters']  # it is K-means, isn't it?
    N_ITERATIONS = args['max_number_of_iterations']
    VERBOSE = args['verbose_level']
    
    # cluster_ids[0,:] = 0, its a workaround for argmax
    clusters_membership = np.zeros((K+1, N), np.int8)
    
    fill_empty_clusters_FLAG = True
    
    # make an initial guess - K different random indexes
    initial_centers = np.random.choice(N, K, replace=False)
    for i,k in enumerate(initial_centers):
        clusters_membership[i+1,k] = 1

    # iterate until converge
    ix_previous = []
    for iteration in xrange(N_ITERATIONS):
        if VERBOSE>0:
            if VERBOSE>1 or iteration%10==9:
                print 'Iteration #%d' % (iteration+1,)
            
        dists = A.dot(clusters_membership.T)
        ix = dists.argmax(1) # ids where to assign each vertex
        
        # stop cluase
        if len(ix_previous) and (ix==ix_previous).all():
            if VERBOSE>1:
                print 'Converged on iteration #%d.' % (iteration+1,)
            break
        else:
            ix_previous = ix
        
        nz = np.where(ix)[0] # non-zero indexes
        
        clusters_membership[:,nz] = 0
        for i in nz:
            clusters_membership[ix[i], i] = 1
            
        # find empty clusters and try to fill them with random vertices
        if fill_empty_clusters_FLAG:
            not_assigned_verts = np.where(ix==0)[0]
            
            if len(not_assigned_verts):
                isClusterEmpty = [not clusters_membership[k+1, :].any() for k in xrange(K)]
                centers = np.random.choice(not_assigned_verts,
                    min(sum(isClusterEmpty), len(not_assigned_verts)), replace=False)
                
                if len(centers):
                    for k,c in zip(np.where(isClusterEmpty)[0], centers):
                        clusters_membership[:,c] = 0
                        clusters_membership[k+1,c] = 1
                        
                    if VERBOSE>2:
                        print "Clusters", np.where(isClusterEmpty)[0], "initiated with", centers
            else:
                fill_empty_clusters_FLAG = False
                if VERBOSE>2:
                    print "fill_empty_clusters_FLAG = False"
                
    # organize return
    clusters = [np.where(clusters_membership[k+1,:])[0] for k in range(K)]
    return clusters
