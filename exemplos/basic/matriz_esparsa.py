import numpy as np
import scipy.sparse as sp

# 1. Create a 100x100 matrix with mostly zeros
# (Using sparse array syntax - standard in SciPy)
dense_matrix = np.zeros((100, 100))
dense_matrix[10, 20] = 5.5
dense_matrix[50, 75] = 9.1

# 2. Convert to a sparse representation (CSR format)
sparse_matrix = sp.csr_array(dense_matrix)

# 3. Save to a compressed .npz file
sp.save_npz('sparse_matrix.npz', sparse_matrix)

# 4. Load it back instantly
loaded_sparse = sp.load_npz('sparse_matrix.npz')