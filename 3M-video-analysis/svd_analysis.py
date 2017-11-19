from scipy.sparse import load_npz
from scipy.sparse.linalg import svds
import numpy

def dimensional_reduction():
    """
    :return:
    """
    # load data from file
    sp_matrix = load_npz("temp/sparse_matrix.npz")
    sp_matrix.dtype = numpy.float
    print('SVD is running...')
    u, s, v = svds(sp_matrix, 128)
    numpy.savez_compressed("temp/svd_result.npz", u=u, s=s, v=v)
    print("SVD done.")