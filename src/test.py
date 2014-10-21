import numpy as np
from scipy.io import loadmat
from alg.min_sum_distance import min_sum_distance
import clustering_error

def euc(x, y):
    return np.linalg.norm(x - y)

# A = loadmat('../data/W.mat')['W']
A = loadmat('../data/test/W.mat')['W']
names = loadmat('../data/test/clusterNumber.mat')['clusterNumber']

d = {'size' : 30, 'distance_func' : euc, 'index' : 0}

cluster_idx = min_sum_distance(A, d)
true_cluster = []
for i in xrange(len(names)):
    if (names[i] == 1):
        true_cluster.append(i)
num_error_vertex, error_found_vertex, error_true_vertex = clustering_error.number_error_clustered(true_cluster, cluster_idx)
print 'Num errors', num_error_vertex, '/', d['size']
print 'Vertices from found cluster and not from true', error_found_vertex
print 'Vertices from true cluster and not from found', error_true_vertex
