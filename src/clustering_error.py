def number_error_clustered(true_cluster, found_cluster):
    '''
    Function computes number of error in found cluster 
    if the true cluster is known
    Input:
    true_cluster - list of vertex indices from true cluster
    found_cluster - list of vertex indices from found cluster
    Output:
    num_error_vertex - number of errors in found cluster
    error_found_vertex - list of vertex indices from found cluster, 
    which are not in true cluster
    error_true_vertex - list of vertex indices from true cluster,
    which are not in found cluster
    '''
    error_found_vertex = set(found_cluster) - set(true_cluster)
    error_true_vertex = set(true_cluster) - set(found_cluster)
    true_cluster_dict = {true_cluster[i] : 0 for i in xrange(len(true_cluster))}
    num_error_vertex = 0;
    for i in xrange(len(found_cluster)):
        if found_cluster[i] not in true_cluster_dict:
              num_error_vertex += 1
    return num_error_vertex, error_found_vertex, error_true_vertex
