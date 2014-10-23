import collections
import math

import numpy as np


def min_sum_distance(A, args):
    '''
    Function extracts cluster based on the minimum sum of distances
    from current vertex to all vertices in cluster. If the sum of distances
    from the vertex is minimum and the cardinality of cluster is less than
    given value, then this vertex is added to the cluster.
    Input:
    A - adjacent matrix of wiki-graph
    Output:
    cluster - list of the row index of the vertices from the cluster
    '''
    S = args['matrix_pairwise_sim'].tocsr()
    start_index = args['index']
    cluster = collections.Counter()
    cluster[start_index] = 1 
    last_similarity = 0
    
    while (True):
        print 'Current size of cluster:', len(cluster)
        if (len(cluster) > args['size']):
            break
        
        similarities = np.zeros(A.shape[0])
        for vertex in xrange(A.shape[0]):
            if vertex not in cluster:
                for cluster_vertex in cluster:
                    if cluster_vertex != start_index:
                        similarities[vertex] += S[vertex, cluster_vertex]
                    else:
                        similarities[vertex] += S[vertex, cluster_vertex] * \
                                    min(math.log(len(cluster) + 1, 2), 6)
        
        max_similarity = np.max(similarities)
        max_sim_index = np.argmax(similarities)
        
        print 'Similarity:', max_similarity / (len(cluster) + 1), '\n'
        if len(cluster) > 0 and \
            (1 + 1.0 / math.log(len(cluster) + 1, 2)) * max_similarity < \
             (1 + 1.0 / len(cluster)) * last_similarity:
            print 'Cluster found. Algorithm was stopped.'
            break
        last_similarity = max_similarity                       
        cluster[max_sim_index] = 1
        #print cluster
    return cluster.keys()
