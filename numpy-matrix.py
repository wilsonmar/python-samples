import numpy as np

# Creating two 3x3 matrices
matrix_a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
matrix_b = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
# Performing matrix multiplication
result = np.matmul(matrix_a, matrix_b)
print(result)

# result:
# [[ 30  24  18]
# [ 84  69  54]
# [138 114  90]]