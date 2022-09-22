# CSCI 323 / 700
# Summer 2022
# Assignment 4 - Empirical Performance of Search Structures
# Ilma Shaharin
# Sources: Classmate Shi Cheng, GeeksForGeeks
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from math import floor, sqrt


asn_num = 4


def pseudo_random_list(n):
    data = [0]
    for i in range(1, n):
        data.append(data[i - 1] + random.randint(1, 10))
    random.shuffle(data)
    return data


def get_random_sublist(data, size):
    return [data[random.randint(0, len(data) - 1)] for i in range(size)]
# get random subset of size items from data list


def get_prime_number(n):
    if n & 1:
        n -= 2
    else:
        n -= 1
    i, j = 0, 3
    for i in range(n, 2, -2):
        if i % 2 == 0:
            continue
        while j <= floor(sqrt(i)) * 1:
            if i % j == 0:
                break
            j += 2
        if j > floor(sqrt(i)):
            return i
    return 2


def build_chaining_hash(data):
    hash_table = [[] for i in range(10)]
    for number in data:
        hash_table[number % 10].append(number)
    return hash_table


def build_quadratic_hash(data):
    hashing_size = len(data) * 2
    hash_table = [-1 for i in range(hashing_size)]
    for i in range(len(data)):
        hash_one = data[i] % hashing_size
        if hash_table[hash_one] == -1:
            hash_table[hash_one] = data[i]
        else:
            for j in range(hashing_size):
                new_hash_value = (hash_one + j * j) % hashing_size
                if hash_table[new_hash_value] == -1:
                    hash_table[new_hash_value] = data[i]
                    break
    return hash_table


def build_double_hash(data):
    hashing_size = len(data) * 5
    hash_table = [None for i in range(hashing_size)]
    for number in data:
        hash_one = number % hashing_size
        if not hash_table[hash_one]:
            hash_table[hash_one] = number
        else:
            hash_two = get_prime_number(number) - number % get_prime_number(number)
            inserted = False
            k = 1
            while not inserted:
                if k > hashing_size:
                    print("No place to insert value")
                    break
                combined_hash = (hash_one + hash_two * k) % hashing_size
                if not hash_table[combined_hash]:
                    hash_table[combined_hash] = number
                    inserted = True
                else:
                    k += 1
    return hash_table


def cuckoo_insert(key, table_num, cnt, table_size, pos, hash_table):
    if cnt == table_size:
        print("non-positioned:", key)
        print("Cycle present. REHASH.")
        return

    ver = len(hash_table)
    for i in range(ver):
        pos[i] = hash(i + 1, key, table_size)
        if hash_table[i][pos[i]] == key:
            return

    if hash_table[table_num][pos[table_num]] != -1:  # if something is already there
        dis = hash_table[table_num][pos[table_num]]
        hash_table[table_num][pos[table_num]] = key
        cuckoo_insert(dis, (table_num+1) % ver, cnt+1, table_size, pos, hash_table)
    else:
        hash_table[table_num][pos[table_num]] = key


def build_cuckoo_hash(data):
    size = len(data)
    table_size = size*10
    num_tables = 2

    # init table
    hash_table = [None] * num_tables
    for i in range(table_size):
        hash_table[0] = [-1] * i
        hash_table[1] = [-1] * i
    pos = [None] * num_tables

    for i in range(size):
        cuckoo_insert(data[i], 0, 0, table_size, pos, hash_table)

    return hash_table


def search_chaining_hash(hash_table, data):
    if hash_table[data % 10].index(data) >= 0:
        return True
    else:
        return False


def search_quadratic_hash(hash_table, data):
    hashing_size = len(hash_table)
    for i in range(hashing_size):
        if hash_table[data % hashing_size] == data:
            return True
        else:
            for j in range(hashing_size):
                new_hash = (data % hashing_size + j * j) % hashing_size
                if hash_table[new_hash] == data:
                    return True
        return False


def search_double_hash(hash_table, data):
    hashing_size = len(hash_table)
    hash_one = data % hashing_size
    if hash_table[hash_one] == data:
        return True
    else:
        hash_two = get_prime_number(data) - data % get_prime_number(data)
        k = 1
        while k <= hashing_size:
            combined_hash = (hash_one + hash_two * k) % hashing_size
            if hash_table[combined_hash] == data:
                return True
            else:
                k += 1
    return False


# def hash(func_num, key, size):
#     if func_num == 1:
#         return key % size
#     else:
#         return int(key/size) % size


# def search_cuckoo_hash(hash_table, key, table_size):
#     ver = len(hash_table)
#     for i in range(ver):
#         pos = hash(i + 1, key, table_size)
#         if hash_table[i][pos] == key:
#             return i, pos


def plot_time(hash_algorithms, sizes, algos, trials, hash_activity):
    alg_counter = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for alg in algos:
        alg_counter += 1
        d = hash_algorithms[alg.__name__]
        x_axis = [j + 0.05 * alg_counter for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=alg.__name__)
    plt.legend()
    plt.title("Run time of Hashing Algorithms")
    plt.xlabel("Size for data")
    plt.ylabel("Time for " + str(trials) + "trials (ms)")
    plt.savefig("Assignment" + str(asn_num) + hash_activity + ".png")
    plt.show()


def main():
    sizes = [100 * i for i in range(1, 11)]
    trials = 10
    build_functions = [build_chaining_hash, build_quadratic_hash, build_double_hash, build_cuckoo_hash]
    search_functions = [search_chaining_hash, search_quadratic_hash, search_double_hash]
    dict_build = {}
    dict_search = {}
    for build in build_functions:
        dict_build[build.__name__] = {}
    for search in search_functions:
        dict_search[search.__name__] = {}
    for size in sizes:
        for build in build_functions:
            dict_build[build.__name__][size] = 0
        for search in search_functions:
            dict_search[search.__name__][size] = 0
        for trial in range(1, trials + 1):
            data = pseudo_random_list(size)
            sublist = get_random_sublist(data, 1000)
            hash_tables = []
            for build in build_functions:
                # print("Building", size, build.__name__)
                start_time = time.time()
                hash_tables.append(build(data))
                end_time = time.time()
                net_time = end_time - start_time
                dict_build[build.__name__][size] += 1000 * net_time
            for i in range(len(search_functions)):
                search = search_functions[i]
                table = hash_tables[i]
                start_time = time.time()
                for item in sublist:
                    if search(table, item) is False:
                        print("Searching", size, search.__name__)
                        print("Not found")
                        break
                end_time = time.time()
                net_time = end_time - start_time
                dict_search[search.__name__][size] += 1000 * net_time
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df_build = pd.DataFrame.from_dict(dict_build).T
    df_search = pd.DataFrame.from_dict(dict_search).T
    print(df_build)
    print(df_search)
    plot_time(dict_build, sizes, build_functions, trials, "Build")
    plot_time(dict_search, sizes, search_functions, trials, "Search")


if __name__ == "__main__":
    main()
