import copy
import numpy as np
import scipy as sp
import scipy.sparse
from sklearn.preprocessing import normalize

#-----------------------------------------------------------------------------
def get_similarity_matrix(A, coefficients = [3, 2, 1]):
    print "Computing similarity matrix..."
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
    # To proceed multiply we have to convert A into csr_matrix.    
    B = normalize(sp.sparse.csr_matrix(A, dtype = float), norm = 'l1',
                  copy = False)

    
    result_matrix = coefficients[0, 0] * B
    C = copy.deepcopy(B)
    for coef in coefficients[0, 1:]:
        C = C.dot(B)
        result_matrix = result_matrix + coef * C
        
    print "Computing similarity matrix... Done."
    
    print result_matrix.todense()
    return result_matrix

#-----------------------------------------------------------------------------

if __name__ == '__main__':
    input_matrix = [[1, 1, 0], [0, 1, 0], [0, 0, 1]]
    get_similarity_matrix(np.matrix(input_matrix))
    get_similarity_matrix(sp.sparse.coo_matrix(input_matrix))