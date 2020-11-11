import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from simplex import simplex

def plot_discretization(A, dx, title, xlabel, ylabel):
    # Create figure and axes
    fig, ax = plt.subplots(1)
    if title == "Position Graph":
        plt.ylim([-2, 2])
    else:
        plt.ylim([-dx, dx])
    plt.xlim([0,10])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    x = []
    x.append(0)
    for i in range(1, len(A)):
        x.append(x[i-1] + dx)

    plt.plot(x, A, 'ro')
    plt.show()

    return

def print_constraint(c, b, n):
    for i in range(0, 2*n, 2):
        print("+" + str(int(c[i])) + "*a" + str(int(i/2 + 1)) + "^+ "
              + str(int(c[i+1])) + "*a" + str(int(i/2 + 1)) + "^⁻ ", end = '')
    print(" = " + str(b))

    return

def print_problem(A_eq, b_eq, c, t, n):
    print("minimizar")

    for i in range(0, 2*n, 2):
        print(str(t) + "*a" + str(int(i/2 + 1)) + "^+ "
              + str(t) + "*a" + str(int(i/2 + 1)) + "^⁻ ", end = '')
    print("")

    print("Sujeito a:")
    # Prints position constraint
    print_constraint(A_eq[0], b_eq[0], n)
    # Prints velocity constraint
    print_constraint(A_eq[1], b_eq[1], n)
    print("Todo ai >= 0")

    return

def find_accelerations(x, n):
    A = []
    for i in range(0,n, 2):
        A.append(x[i] - x[i+1]) # xi = xi^+ - xi^-
    return A

def get_cost(c, sol):
    cost = 0
    for i in range(len(c)):
        cost += c[i]*sol[i]

    return cost

def problem(time_increment, is_single):
    t = 10
    n = int(t/time_increment)

    # Constructing the coefficients vector of the objective function
    c = []
    for i in range(2*n):
        c.append(time_increment)
    c_copy = c.copy()

    # Constructing the equality constraints matrix
    A_eq = [[], []]
    b_eq = [1, 0]

    # Constructing the position constraint
    for i in range(0, 2*n, 2):
        ai = (10/time_increment + 1) - (i+1)/2
        A_eq[0].append(ai)
        A_eq[0].append(-ai)

    # Constructing the velocity constraint
    for i in range(0, 2*n, 2):
        A_eq[1].append(1)
        A_eq[1].append(-1)

    # Printing the problem
    if is_single:
        print_problem(A_eq, b_eq, c, time_increment, n)

    # Printing results
    print("Simplex result")
    sol = simplex(c, A_eq, b_eq)
    print(sol)

    # Adding the values of a0^+ and a0^-
    x = [0, 0]
    for i in range(2*n):
        x.append(sol[i])

    if is_single:
        A = find_accelerations(x, 2*n + 2)
        print("Accelerations:")
        print(A)

        plot_discretization(A, time_increment, "Acceleration Graph", "Time", "Acceleration")

        A_sum = []; A_sum.append(0)
        V = []; V.append(0)
        for i in range(1, len(A)):
            A_sum.append(A[i] + A_sum[i-1])
            V.append(A_sum[i])

        plot_discretization(V, time_increment, "Velocity Graph", "Time", "Velocity")

        V_sum = []; V_sum.append(0)
        POS = []; POS.append(0)
        for i in range(1, len(V)):
            V_sum.append(V[i] + V_sum[i-1])
            POS.append(V_sum[i])
        plot_discretization(POS, time_increment, "Position Graph", "Time", "Position")

    return get_cost(c_copy, sol)

def main():
    opt = int(input("Enter 1 to choose to run a single problem. Enter 2 to run a test with several discretization intervals or type 3 to exit: "))

    while (opt == 1 or opt == 2):
        if (opt == 1):
            time_increment = float(input('Enter the discretization interval: '))
            problem(time_increment, True)
        else:
            x = []
            y = []
            x.append(2)
            for i in range(1, 10):
                x.append(x[i-1]/2)
            for i in range(len(x)):
                y.append(problem(x[i], False))
            fig, ax = plt.subplots(1)
            plt.ylim([0,1.1])
            plt.xlabel("Discretization interval")
            plt.ylabel("Final cost")
            plt.title("(Fuel) Cost x Discretization interval")
            plt.plot(x, y, 'ro')
            plt.show()
        opt = int(input("Enter 1 to choose to run a single problem. Enter 2 to run a test with several discretization intervals or type 3 to exit: "))

main()
