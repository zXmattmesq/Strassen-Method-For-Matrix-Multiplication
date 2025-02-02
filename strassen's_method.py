class MatrixOperations:
    def get_row_col(A, B):
        Arows, Acols = len(A), len(A[0])
        Brows, Bcols = len(B), len(B[0])
        return Arows, Acols, Brows, Bcols

    def get_empty_matrix(Arows, Bcols):
        return [[0 for i in range(Bcols)] for j in range(Arows)]

    def left_down_multiply(A, B):
        Arows, Acols, Brows, Bcols = MatrixOperations.get_row_col(A, B)
        C = MatrixOperations.get_empty_matrix(Arows, Bcols)
        for i in range(0, Arows):
            for j in range(0, Bcols):
                temp = 0
                for k in range(0, Acols):
                    temp += (A[i][k] * B[k][j])
                C[i][j] = temp
        return C

    def quadrant_matrix(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rowMid, colMid = rows // 2, cols // 2
        T21 = [[matrix[row][col] for col in range(colMid)] for row in range(rowMid)]
        T22 = [[matrix[row][col] for col in range(colMid, cols)] for row in range(rowMid)]
        B11 = [[matrix[row][col] for col in range(colMid)] for row in range(rowMid, rows)]
        B12 = [[matrix[row][col] for col in range(colMid, cols)] for row in range(rowMid, rows)]
        return T21, T22, B11, B12

    def matrix_add(A, B):
        Arows, Acols, Brows, Bcols = MatrixOperations.get_row_col(A, B)
        if Arows != Brows or Acols != Bcols:
            return "Dimension Missmatch Error..."
        else:
            C = MatrixOperations.get_empty_matrix(Arows, Acols)
            for row in range(Arows):
                for col in range(Bcols):
                    C[row][col] = A[row][col] + B[row][col]
            return C

    def matrix_sub(A, B):
        Arows, Acols, Brows, Bcols = MatrixOperations.get_row_col(A, B)
        if Arows != Brows or Acols != Bcols:
            return "Dimension Missmatch Error..."
        else:
            C = MatrixOperations.get_empty_matrix(Arows, Acols)
            for row in range(Arows):
                for col in range(Bcols):
                    C[row][col] = A[row][col] - B[row][col]
            return C

    def matrix_combine(B11, B12, T21, T22):
        rows, cols = len(B11), len(B11[0])
        rowFinal, colFinal = rows * 2, cols * 2
        matrix = MatrixOperations.get_empty_matrix(rowFinal, colFinal)
        for i in range(rows):
            for j in range(cols):
                matrix[i][j] = B11[i][j]
        for i in range(rows):
            for j in range(cols):
                matrix[i][j + cols] = B12[i][j]
        for i in range(rows):
            for j in range(cols):
                matrix[i + rows][j] = T21[i][j]
        for i in range(rows):
            for j in range(cols):
                matrix[i + rows][j + cols] = T22[i][j]
        return matrix

    def strassen(A, B):
        Arows, Acols, Brows, Bcols = MatrixOperations.get_row_col(A, B)
        if Acols != Brows or Arows == 0 or Acols == 0 or Brows == 0 or Bcols == 0:
            return "Error... Proper conditions for matrix multiplication not met"
        if Arows < 2 or Acols < 2 or Brows < 2 or Bcols < 2:
            return MatrixOperations.left_down_multiply(A, B)
        else:
            A11, A12, A21, A22 = MatrixOperations.quadrant_matrix(A)
            B11, B12, B21, B22 = MatrixOperations.quadrant_matrix(B)
            M1 = MatrixOperations.strassen(MatrixOperations.matrix_add(A11, A22), MatrixOperations.matrix_add(B11, B22))
            M2 = MatrixOperations.strassen(MatrixOperations.matrix_add(A21, A22), B11)
            M3 = MatrixOperations.strassen(A11, MatrixOperations.matrix_sub(B12, B22))
            M4 = MatrixOperations.strassen(A22, MatrixOperations.matrix_sub(B21, B11))
            M5 = MatrixOperations.strassen(MatrixOperations.matrix_add(A11, A12), B22)
            M6 = MatrixOperations.strassen(MatrixOperations.matrix_sub(A21, A11), MatrixOperations.matrix_add(B11, B12))
            M7 = MatrixOperations.strassen(MatrixOperations.matrix_sub(A12, A22), MatrixOperations.matrix_add(B21, B22))
            C11 = MatrixOperations.matrix_add(MatrixOperations.matrix_sub(MatrixOperations.matrix_add(M1, M4), M5), M7)
            C12 = MatrixOperations.matrix_add(M3, M5)
            C21 = MatrixOperations.matrix_add(M2, M4)
            C22 = MatrixOperations.matrix_add(MatrixOperations.matrix_sub(MatrixOperations.matrix_add(M1, M2), M3), M6)
            return MatrixOperations.matrix_combine(C11, C12, C21, C22)
