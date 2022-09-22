# CSCI 323 / 700
# Summer 2022
# Assignment 7 - Graph Algorithms
# Ilma Shaharin
import copy
import random
import time
from heapq import heappop, heappush

import pandas as pd
import matplotlib.pyplot as plt

asn_num = 7
INF = 99999


def random_graph(size, max_cost):
    graph = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(0)
            else:
                cost = random.randint(1, max_cost)
                row.append(cost)
        graph.append(row)
    return graph


def make_non_edges_inf(graph):
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == 0:
                graph[i][j] = INF


# Source: https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/
def floyd_apsp(graph):
    graph_copy = copy.deepcopy(graph)
    n = len(graph_copy)
    dist = [[INF] * n for i in range(n)]
    pred = [[-1] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            dist[i][j] = graph_copy[i][j]
            pred[i][j] = i
        dist[i][i] = 0
        pred[i][i] = -1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]


def convert_to_adj_table(graph):
    adj_table = []
    for i in range(len(graph)):
        row = graph[i]
        neighbors = []
        for j in range(len(row)):
            if graph[i][j] > 0:
                neighbors.append((j, graph[i][j]))
        adj_table.append(neighbors)
    return adj_table


def convert_to_edge_set(graph):
    edge_set = []
    for i in range(len(graph)):
        row = graph[i]
        for j in range(len(row)):
            if graph[i][j] > 0:
                edge_set.append((i, j, graph[i][j]))
    return edge_set


# Source: https://www.geeksforgeeks.org/bellman-ford-algorithm-dp-23/
def bellman_ford_sssp(es, n, src):
    dist = [INF] * n
    dist[src] = 0
    for i in range(n):
        for u, v, w in es:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in es:
        if dist[u] != INF and dist[u] + w < dist[v]:
            print("Graph contains negative weight cycle")


def bellman_ford_apsp(graph):
    es = convert_to_edge_set(graph)
    n = len(graph)
    for src in range(n):
        bellman_ford_sssp(es, n, src)


def min_distance(dist, done):
    n = len(dist)
    min_dist = INF
    min_index = -1
    for u in range(n):
        if dist[u] < min_dist and not done[u]:
            min_dist = dist[u]
            min_index = u
    return min_index


# Source: https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
def dijkstra_sssp_matrix(cm, src):
    n = len(cm)
    dist = [INF] * n
    dist[src] = 0
    done = [False] * n
    for i in range(n):
        x = min_distance(dist, done)
        done[x] = True
        for y in range(n):
            if cm[x][y] > 0 and not done[y] and dist[y] > dist[x] + cm[x][y]:
                dist[y] = dist[x] + cm[x][y]


def dijkstra_apsp_matrix(graph):
    n = len(graph)
    for src in range(n):
        dijkstra_sssp_matrix(graph, src)


# Source: http://nmamano.com/blog/dijkstra/dijkstra.html
def dijkstra_sssp_table(table, src):
    n = len(table)
    dist = [INF for u in range(n)]
    dist[src] = 0
    visited = [False for u in range(n)]
    priority_queue = [(0, src)]
    while len(priority_queue) > 0:
        _, u = heappop(priority_queue)  # We only need the nodes, not the distance
        if visited[u]:
            continue
        visited[u] = True
        for v, l in table[u]:
            if dist[u] + l < dist[v]:
                dist[v] = dist[u] + l
                heappush(priority_queue, (dist[u] + l, v))


def dijkstra_apsp_table(graph):
    table = convert_to_adj_table(graph)
    n = len(graph)
    for src in range(n):
        dijkstra_sssp_table(table, src)


def plot_time(dict_algorithms, sizes, graph_algorithms, trials):
    alg_counter = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for algs in graph_algorithms:
        alg_counter += 1
        d = dict_algorithms[algs.__name__]
        x_axis = [j + 0.05 * alg_counter for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=algs.__name__)
    plt.legend()
    plt.title("Run time of Graph Algorithms")
    plt.xlabel("Size for data")
    plt.ylabel("Time for " + str(trials) + "trial (ms)")
    plt.savefig("Assignment" + str(asn_num) + ".png")
    plt.show()


def main():
    sizes = [10 * i for i in range(1, 11)]
    trials = 1
    graph_algorithms = [floyd_apsp, bellman_ford_apsp, dijkstra_apsp_matrix, dijkstra_apsp_table]
    dict_algorithms = {}
    for alg in graph_algorithms:
        dict_algorithms[alg.__name__] = {}
    for size in sizes:
        for alg in graph_algorithms:
            dict_algorithms[alg.__name__][size] = 0  # initialize the dictionary
        for trial in range(1, trials + 1):
            m1 = random_graph(size, 100)
            for alg in graph_algorithms:
                start_time = time.time()
                m3 = alg(m1)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algorithms[alg.__name__][size] += 1000 * net_time
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_algorithms).T
    print(df)
    plot_time(dict_algorithms, sizes, graph_algorithms, trials)


if __name__ == "__main__":
    main()
