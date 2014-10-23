import copy
import cPickle
import numpy as np
import scipy as sp
import scipy.io
import scipy.sparse
from sklearn.preprocessing import normalize

#-----------------------------------------------------------------------------
def get_similarity_matrix(A, coefficients = [3, 2, 1]):
    print "Computing similarity matrix..."
    print "input type = ", type(A)
    available_matrix_formats = [sp.sparse.coo_matrix,
                                sp.sparse.csc_matrix,
                                sp.sparse.csr_matrix,
                                np.matrixlib.defmatrix.matrix]
    
    if not type(A) in available_matrix_formats:
        print "Unknown matrix type:", str(type(A))
        return None
    
    # Result matrix is coef * (A^i) (elementwise).
    #coefficients = [3, 2, 1]
    coefficients = normalize(np.matrix(coefficients, dtype = float), 
                                   norm = 'l1')
    
    # To proceed multiply we have to convert A into csc_matrix.
    B = normalize(1.0 * sp.sparse.csc_matrix(A), norm = 'l1')
    
    result_matrix = coefficients[0, 0] * B
    C = copy.deepcopy(B)
    for coef in coefficients[0, 1:]:
        print coef
        C = C * B
        result_matrix = result_matrix + coef * C
        
    print "Computing similarity matrix... Done. \n"
    return result_matrix.tocoo()

#-----------------------------------------------------------------------------
def get_similarity_people_matrix_by_all_pagelinks(coefficients = [3, 2, 1]):
    print "Computing similarity matrix (full)..."
    W = scipy.io.loadmat('../data/W.mat')['W']
    # Check matrix type. 
    available_matrix_formats = [sp.sparse.coo_matrix,
                                sp.sparse.csc_matrix,
                                sp.sparse.csr_matrix,
                                np.matrixlib.defmatrix.matrix]
    
    if not type(W) in available_matrix_formats:
        print "Unknown matrix type from mat file:", str(type(W))
        return None
    
    full_sim = get_similarity_matrix(W, coefficients)
    
    path_to_people_dict = "../data/person_id2ind.pickle"
    
    f = open(path_to_people_dict, 'rb')
    person_to_id_dict = cPickle.load(f)
    f.close()

    f = open("../data/sparse_to_dense.pickle", 'rb')
    id_ind_dict = cPickle.load(f)
    f.close()

    for item in person_to_id_dict:
        print item, id_ind_dict[item]
    
    #Sub = full_sim.tocsr()[:, person_to_id_dict]
    #return result_matrix.tocoo()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    
    get_similarity_people_matrix_by_all_pagelinks()
    
    print "Testing...\n"
    input_matrix = scipy.io.loadmat('../data/A.mat')['A']#[:1000, :1000]
    get_similarity_matrix(np.matrix(input_matrix.todense()))
    get_similarity_matrix(input_matrix.tocsc())
    get_similarity_matrix(input_matrix.tocsr())
    print "Testing... Done."
