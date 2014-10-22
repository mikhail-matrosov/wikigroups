import numpy as np
from scipy.io import loadmat
from time import clock

from alg.min_sum_distance import min_sum_distance
from alg.KMeans import KMeans
from getAcquaintances import getAcquaintances
import clustering_error

# Load adjacent matrix of the wiki-graph
# A = loadmat('../data/W.mat')['W']
#A = loadmat('../data/test/W.mat')['W']
A = loadmat('../data/test/A.mat')['A']

# Define all neccessary constants and parameters
args = {
'max_number_of_iterations': 5000,
'number_of_clusters': 500,
'verbose_level': 1}

# Use some clustering algorithm
t = clock()
clusters = KMeans(A,args)
print time.clock()-t

np.save('../data/clusters', clusters)

# Compare their results

# Visualize their results 
#clusters = np.load('person_clusters_ensw100c1000i.npy')
visualizeClusters(A, clusters);
getAcquaintances(clusters, 'Barack_Obama', '../data/people_in_the_cluster.txt')
