'''
Implementation of a Simplex Solver object. It detects when the optimal resolution
was found and has a step() method where one full iteration will be the doneself.
The vertex method returns the optimal solution.
'''

class SimplexSolver:
    def __init__(self, a, b, c, basis, clean_c_row = False):
        self.a = a
        self.b = b
        self.c = c
        self.basis = basis
        self.is_solved = False
        if clean_c_row:
            self._diagonalize_c_row()

    def vertex(self):
        v = [0]*len(self.c)
        for i, val in zip(self.basis, self.b):
            v[i] = val
        return v

    '''
    An iteration of the simplex algorithm
    '''
    def step(self):
        # Gets minimal value index
        i_lead = self._find_leading_column()

        if i_lead is None:
            # No value is negative hence the algorithm ends
            self.is_solved = True
            return False

        # Finds the leading row
        best_ratio = None; best_row = None

        for j, b_j in enumerate(self.b):
            a_ji = self.a[j][i_lead]

            if a_ji == 0: # When A contains zeros
                continue

            # Coinciding vertices. If a_ji is positive, the ratios are positive
            if b_j == 0:
                if a_ji <= 0:
                    continue
            ratio = b_j/a_ji
            if ratio < 0:
                continue

            if best_ratio is None or ratio < best_ratio:
                best_ratio = ratio
                best_row = j

        # Found best_row and best_column.
        self._diagonalize_by_row_col(best_row, i_lead)
        self.basis[best_row] = i_lead # Update the basis

        return True

    '''
    Do the diagonalization relatively to rows and columns
    j -> row1
    i -> column
    '''
    def _diagonalize_by_row_col(self, j, i):
        a_ji = self.a[j][i]

        # Normalization of the j'th row
        self.b[j] /= a_ji
        aj = self.a[j]
        for i1 in range(len(self.c)):
            if i1 != i:
                aj[i1] /= a_ji
            else:
                aj[i1] = 1

        # Clear the other rows
        _subtract_scaled_row(self.c, aj, self.c[i])
        self.c[i] = 0

        for j1, a_j1 in enumerate(self.a):
            if j1 == j: continue
            k = a_j1[i]
            _subtract_scaled_row( a_j1, aj, k)
            a_j1[i] = 0
            self.b[j1] -= self.b[j] * k

    def _diagonalize_c_row(self):
        c = self.c
        for j, i in enumerate(self.basis):
            if c[i] != 0:
                _subtract_scaled_row(c, self.a[j], c[i])
                c[i] = 0

    def _find_leading_column(self):
        imin = min(range(len(self.c)), key=lambda i: self.c[i])
        if self.c[imin] >= 0:
            return None
        else:
            return imin

# OPERATION: row1 -= k*row2
def _subtract_scaled_row(row1, row2, k):
    if k == 0:
        return
    for i, row2_i in enumerate(row2):
        row1[i] -= k*row2_i
