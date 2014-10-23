import numpy as np
import networkx as nx
import scipy
import matplotlib.pylab as plt 


def getTheMostImportantFromCluster(A, cluster):
    ratings = A[cluster,:].sum(axis=1)
    ratings = np.array(ratings).flatten()
    return cluster[ratings.argmax()]
    
def convertName(name):
    parts = name.split('_')
    return ''.join([p[0]+"." for p in parts[:-1]])+parts[-1]

def visualizeClusters(A, clusters, drawNames=1,
    i2t = '../data/ID-title_dict.pickle',
    pid2ind = '../data/person_id2ind.pickle'):
    '''
    Function that visualizes clusterization of the graph
    Input:
    clusters - list of the row index of the vertices from the cluster
    '''
    
    # size_treshold = max(0.05 * max([len(c) for c in clusters]), 1)
    size_treshold = 0
    clusters = [c for c in clusters if len(c)>size_treshold]
    
    K = len(clusters) #  number of clusters
    B = np.zeros((K,K)) #  clusters' network
    
    for i in range(K):
        for j in range(K):
            B[i,j] = A[clusters[i],:][:,clusters[j]].sum()
    
    B = np.sqrt(B)
    
    G = nx.DiGraph(B);
    #nx.draw_spectral(G);
    
    # make new undirected graph H without multi-edges
    H=nx.Graph(G)

    # edge width is proportional to similiarity of nodees
    edgewidth=[]
    for (u,v,d) in H.edges(data=True):
        edge = G.get_edge_data(u,v)
        if edge:
            edgewidth.append(edge['weight'])

    # node size is proportional to number of articles
    sizes = dict(zip(G.nodes(), map(lambda x: np.sqrt(len(x)), clusters)))
    
    if drawNames:
        pid2ind = scipy.load(pid2ind)
        i2t = scipy.load(i2t)
        ind2pid = dict(zip(pid2ind.values(), pid2ind.keys()))
        
        vips = map(lambda C: getTheMostImportantFromCluster(A, C), clusters) # id of centers
        pids = map(ind2pid.get, vips) # wiki-id
        names = map(i2t.get, pids) # names
        shorts = map(convertName, names) # short nice variants
        labels = dict(zip(G.nodes(), shorts))
    else:
        labels = dict(zip(G.nodes(), map(len, clusters)))
    
    #pos = nx.spectral_layout(H)
    pos = nx.spring_layout(H)
    #pos = nx.random_layout(H)
    
    plt.rcParams[u'text.usetex'] = False
    plt.figure(figsize=(20,20))
    nx.draw_networkx_edges(H,pos,alpha=0.4,width=edgewidth, edge_color='m')
    nodesize=[sizes[v]*50 for v in H]
    nx.draw_networkx_nodes(H,pos,node_size=nodesize,node_color='r',alpha=0.8)
    nx.draw_networkx_edges(H,pos,alpha=1,node_size=0,width=1,edge_color='b')
    nx.draw_networkx_labels(H,pos,labels,fontsize=12)

    plt.axis('off')
    plt.savefig('graph.png',dpi=200)
    plt.show() # display
