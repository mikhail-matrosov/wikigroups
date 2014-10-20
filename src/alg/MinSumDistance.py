import numpy as np


def MinSumDistance(A, *args):
    '''
    Function extracts cluster based on the minimum sum of distances
    from current vertex to all vertices in cluster. If the sum of distances
    from the vertex is minimum and the cardinality of cluster is less than
    given value, then this vertex is added to the custer.
    Input:
    A - adjacent matrix of wiki-graph
    Output:
    cluster - list of the row index of the vertices fron the cluster
    '''
    dist_func = args['distance_func']
    cluster = [args['index']]
    while (len(cluster) < args['size']):
        current_distances = [np.inf for i in xrange(A.shape[0])]
        for idx_vertex in A.shape[0]:
            if idx_vertex not in cluster:
                d = [0 for i in xrange(len(cluster))]
                for idx_vertex_in_cluster in cluster:
                    d[idx_vertex_in_cluster] =
                    dist_func(A[idx_vertex], A[idx_vertex_in_cluster])
            current_distances[idx_vertex] = np.sum(d)
        cluster.append(np.argmin(current_distances))
    return cluster
