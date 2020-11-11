from solver import SimplexSolver

# Simplex algorithm utilizing the big-M method.
def simplex(c, A, b):
    # Start the basis
    basis = []
    for i in range(len(A)):
        basis.append(None)

    n = len(c)
    n_artificial = len(basis)
    # Introducing the artificial variables
    zeros = [0] * n_artificial
    A = [a_j + zeros for a_j in A]

    nxt_art_var = n
    M_basis = basis[:]
    for j, bi in enumerate(basis):
        if bi is None:
            A[j][nxt_art_var] = 1
            M_basis[j] = nxt_art_var
            nxt_art_var += 1

    # The C vector for the Big M method
    cM = [0]*n + [1]*n_artificial

    # Solving the Big M problem until all the artificial variables are not in the basis
    M_solver = SimplexSolver(A, b, cM, M_basis, clean_c_row=True)
    real_vertex_reached = False

    while M_solver.is_solved == False:
        M_solver.step()

        # Verifies if the Big M problem was reached
        if all(bi < n for bi in M_solver.basis):
            real_vertex_reached = True
            break

    # Reducing the problem back
    A = [a_row[:n] for a_row in M_solver.a]
    solver = SimplexSolver(A, M_solver.b, c, M_solver.basis, clean_c_row = True)
    while solver.is_solved == False:
        solver.step()

    return solver.vertex()
