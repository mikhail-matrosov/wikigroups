import numpy as np
from scipy.io import loadmat
from time import clock
from cPickle import load
from alg.min_sum_distance import min_sum_distance
from alg.KMeans import KMeans
import visualize_clusters
from getAcquaintances import getAcquaintances
import clustering_error
from idx2title import visualize
from get_similarity_matrix import get_similarity_matrix


# Define all neccessary constants and parameters
path_to_data = '../data/'
center_person = 'Vladimir_Putin'
center_person = 'Barack_Obama'
center_person = 'Ashley_Cole'
center_person = 'David_Cameron'
id2index_filename = 'person_id2ind.pickle'
title2id_filename = 'title-ID_dict.pickle'
args = {
'max_number_of_iterations': 100,
'number_of_clusters': 500,
'verbose_level': 1,
'size': 10
}
with open(path_to_data + id2index_filename, 'rb') as f:
    id2ind = load(f)
with open(path_to_data + title2id_filename, 'rb') as f:
    title2id = load(f)
try:
    id_center_person = title2id[center_person]
except KeyError:
    print 'Center person id not found!'
    sys.exit(0)
try:
    index_center_person = id2ind[id_center_person]
    args['index'] = index_center_person
except KeyError:
    print 'Center person index not found!'
    sys.exit(0)


# Load adjacent matrix of the wiki-graph
# A = loadmat(path_to_data + 'W.mat')['W']
# A = loadmat(path_to_data + '/test/W.mat')['W']
A = loadmat(path_to_data + 'A.mat')['A']
args['matrix_pairwise_sim'] = get_similarity_matrix(A)

# Use some clustering algorithm

# t = clock()
# clusters = KMeans(A+A.T,args)
# print clock() - t

cl = min_sum_distance(A, args)
print visualize(cl)

# np.save('../data/clusters', clusters)

# Compare their results

# Visualize their results
# clusters = np.load('../data/person_clusters_ensw500c5000i.npy')
# visualize_clusters.visualizeClusters(A+A.T, clusters);
# getAcquaintances(A+A.T, clusters, 'Vladimir_Putin',
#                  '../data/people_in_the_cluster.txt', printRating = 1)
