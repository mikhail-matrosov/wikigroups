import copy
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
    coefficients = [3, 2, 1]
    coefficients = normalize(np.matrix(coefficients, dtype = float), 
                                   norm = 'l1')
    
    # To proceed multiply we have to convert A into csc_matrix.
    B = normalize(1.0 * sp.sparse.csc_matrix(A), norm = 'l1')
    
    result_matrix = coefficients[0, 0] * B
    C = copy.deepcopy(B)
    for coef in coefficients[0, 1:]:
        C = C.dot(B)
        result_matrix = result_matrix + coef * C
        
    print "Computing similarity matrix... Done. \n"
    return result_matrix.tocoo()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    print "Testing...\n"
    input_matrix = scipy.io.loadmat('../data/A.mat')['A']
    get_similarity_matrix(np.matrix(input_matrix.todense()))
    get_similarity_matrix(input_matrix.tocsc())
    get_similarity_matrix(input_matrix.tocsr())
    print "Testing... Done."
