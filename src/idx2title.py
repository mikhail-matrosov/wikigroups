from cPickle import load


def Visualize(vertex_index_list, index2id_filename='dense_to_sparse.pickle',
              id2title_filename='ID-title_dict.pickle'):
    '''
    Convert obtained list of vertex indices belonging to the cluster into
    the list of the corresponding page titles
    Input:
    vertex_index_list - list of vertex indices from the cluster
    index2id_filename - pickle file with dict {index : id}
    id2title_filename - pickle file with dict {id : title}
    Output:
    title - list of titles
    '''
    title = []
    with open(index2id_filename, 'rb') as f:
        ind2id = load(f)
    with open(id2title_filename, 'rb') as f:
        id2title = load(f)
    for key in vertex_index_list:
        title.append(id2title[ind2id[key]])
    return title
