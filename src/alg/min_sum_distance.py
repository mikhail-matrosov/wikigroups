import numpy as np


def min_sum_distance(A, args):
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
    S = args['matrix_pairwise_sim'].tocsr()
    cluster = [args['index']]
    while (len(cluster) < args['size']):
        print 'Current size of cluster', len(cluster)
        current_distances = [0 for i in xrange(A.shape[0])]
        for idx_vertex in xrange(A.shape[0]):
            if idx_vertex not in cluster:
                s = [0 for i in xrange(A.shape[0])]
                for idx_vertex_in_cluster in cluster:
                    s[idx_vertex_in_cluster] = S[idx_vertex, idx_vertex_in_cluster]
                current_distances[idx_vertex] = np.sum(s)
        cluster.append(np.argmax(current_distances))
    return cluster
