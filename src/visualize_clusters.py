import numpy as np
import networkx as nx


def visualizeClusters(A, clusters):
    '''
    Function that visualizes clusterization of the graph
    Input:
    clusters - list of the row index of the vertices from the cluster
    '''
    
    K = len(clusters) # number of clusters
    B = np.zeros((K,K)) # clusters' network
    
    for i in range(K):
        for j in range(K):
            B[i,j] = A[clusters[i], :][:,clusters[j]].sum()
    
    G = nx.DiGraph(B);
    #nx.draw_spectral(G);
    
    # make new undirected graph H without multi-edges
    H=nx.Graph(G)

    # edge width is proportional number of games played
    edgewidth=[]
    for (u,v,d) in H.edges(data=True):
        edgewidth.append(G.get_edge_data(u,v)['weight'])

    # node size is proportional to number of games won
    sizes = dict(zip(G.nodes(), map(len, clusters)))
    
    labels = dict(zip(G.nodes(), map(len, clusters)))
    
    pos=nx.spectral_layout(H)
        
    plt.rcParams['text.usetex'] = False
    plt.figure(figsize=(8,8))
    nx.draw_networkx_edges(H,pos,alpha=0.5,width=edgewidth, edge_color='k')
    nodesize=[sizes[v]*50 for v in H]
    nx.draw_networkx_nodes(H,pos,node_size=nodesize,node_color='r',alpha=0.8)
    nx.draw_networkx_edges(H,pos,alpha=1,node_size=0,width=1,edge_color='k')
    nx.draw_networkx_labels(H,pos,labels,fontsize=14)

    plt.axis('off')
    #plt.savefig("chess_masters.png",dpi=75)
    plt.show() # display