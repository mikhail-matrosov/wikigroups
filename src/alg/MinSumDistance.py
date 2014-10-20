import numpy as np


def MinSumDistance (A, *args):
    '''
    
    '''
    cluster = [args['index']]
    while (len(cluster) < args['size']):
        current_distances = [np.inf for i in xrange(A.shape[0])]
        for idx in A.shape[0]:
            if idx not in cluster:
                d = [0 for i in xrange(len(cluster))]
                for idx_cluster in cluster:
                    d[idx_cluster] = args['distance_func'](A[idx], A[idx_cluster])
            current_distances[idx] = np.sum(d)
        cluster.append(np.argmin(current_distances))
    return cluster
