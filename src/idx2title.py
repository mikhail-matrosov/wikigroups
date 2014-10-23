from cPickle import load


def visualize(vertex_index_list, id2index_filename='person_id2ind.pickle',
              id2title_filename='ID-title_dict.pickle', path='../data/'):
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
    with open(path + id2index_filename, 'rb') as f:
        id2ind = load(f)
    with open(path + id2title_filename, 'rb') as f:
        id2title = load(f) 
    key = 0
    for ind in vertex_index_list:
        for k in id2ind:
            if id2ind[k] == ind:
                key = k
                break
        title.append(id2title[key])
    return title
