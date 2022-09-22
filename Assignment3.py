# CSCI 323 / 700
# Summer 2022
# Assignment 3 - Matrix Manipulation Algorithms
# Ilma Shaharin
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

asn_num = 3


def random_matrix(mn, mx, rows, cols):
    my_random_matrix = [[random.randint(mn, mx) for col in range(0, cols)] for row in range(0, rows)]
    return np.array(my_random_matrix)


def all_ones_matrix(mn, mx, rows, cols):
    my_ones_matrix = [[1 for col in range(0, cols)] for row in range(0, rows)]
    return np.array(my_ones_matrix)


def print_matrix(my_matrix):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in my_matrix]))


def native_mult(m1, m2):
    return np.dot(m1, m2)


def simple_mult(m1, m2):
    rows = len(m1)
    cols = len(m2[0])
    m3 = [[0 for x in range(cols)] for y in range(rows)]
    for i in range(rows):
        for j in range(cols):
            m3[i][j] = 0
            for x in range(cols):
                m3[i][j] += m1[i][x] * m2[x][j]
    return m3


def strassen_mult(m1, m2):
    x = len(m1)
    y = len(m2)
    if x == 1 or y == 1:
        return m1 * m2
    j = m1.shape[0]
    if j % 2 == 1:
        m1 = np.pad(m1, (0, 1), mode='constant')
        m2 = np.pad(m2, (0, 1), mode='constant')
    k = int(np.ceil(j / 2))
    a = m1[: k, : k]
    b = m1[: k, k:]
    c = m1[k:, : k]
    d = m1[k:, k:]
    e = m2[: k, : k]
    f = m2[: k, k:]
    g = m2[k:, : k]
    h = m2[k:, k:]
    p1 = strassen_mult(a, f - h)
    p2 = strassen_mult(a + b, h)
    p3 = strassen_mult(c + d, e)
    p4 = strassen_mult(d, g - e)
    p5 = strassen_mult(a + d, e + h)
    p6 = strassen_mult(b - d, g + h)
    p7 = strassen_mult(a - c, e + f)
    result = np.zeros((2 * k, 2 * k), dtype=np.int32)
    result[: k, : k] = p5 + p4 - p2 + p6
    result[: k, k:] = p1 + p2
    result[k:, : k] = p3 + p4
    result[k:, k:] = p1 + p5 - p3 + p7
    return result[: j, : j]
# Source: https://www.interviewbit.com
# Divide matrix m1 and m2 into 7 sub-matrices and then recursively compute the sub-matrices of result
# Worst-Case: O(n^3) or polynomial runtime / Using the Master Theorem, it's O(n^2.8074)


def plot_time(dict_algorithms, sizes, matrix_algorithms, trials):
    alg_counter = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for algs in matrix_algorithms:
        alg_counter += 1
        d = dict_algorithms[algs.__name__]
        x_axis = [j + 0.05 * alg_counter for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=algs.__name__)
    plt.legend()
    plt.title("Run time of Matrix Multiplication Algorithms")
    plt.xlabel("Size for data")
    plt.ylabel("Time for " + str(trials) + "trial (ms)")
    plt.savefig("Assignment" + str(asn_num) + ".png")
    plt.show()


def main():
    sizes = [10 * i for i in range(1, 11)]
    trials = 1
    matrix_algorithms = [native_mult, simple_mult, strassen_mult]
    dict_algorithms = {}
    for alg in matrix_algorithms:
        dict_algorithms[alg.__name__] = {}
    for size in sizes:
        for alg in matrix_algorithms:
            dict_algorithms[alg.__name__][size] = 0   # initialize the dictionary
        for trial in range(1, trials + 1):
            m1 = random_matrix(-1, 1, size, size)
            m2 = random_matrix(-1, 1, size, size)
            for alg in matrix_algorithms:
                start_time = time.time()
                m3 = alg(m1, m2)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algorithms[alg.__name__][size] += 1000 * net_time
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_algorithms).T
    print(df)
    plot_time(dict_algorithms, sizes, matrix_algorithms, trials)


if __name__ == "__main__":
    main()
