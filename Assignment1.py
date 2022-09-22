# CSCI 323 / 700
# Summer 2022
# Assignment 1 - Searching Algorithms
# Ilma Shaharin
import math
import random
import time
import pandas as pd
import matplotlib.pyplot as plt


def random_list(min_num, max_num, size, do_sort, unique):
    numbers = []
    # empty list for random numbers
    i = 0
    while i < size:
        rnd = random.randint(min_num, max_num)
        if unique and rnd in numbers:
            continue
        else:
            i += 1
            numbers.append(rnd)
    if do_sort:
        numbers.sort()
    return numbers


def python_search(arr, key):
    return arr.index(key)
# built-in index search


def linear_search(arr, key):
    n = len(arr)           # number of items in the array
    for i in range(0, n):
        if arr[i] == key:
            return i
    return -1
# if a random number in the array matches the comparable key, return that element,
# otherwise, return false
# Time Complexity: O(n)


def binary_search_recursive(arr, left, right, key):
    if right >= left:
        mid_point = left + int((right - left) / 2)
        if arr[mid_point] == key:
            return mid_point  # returns the middle element if it matches the key
        elif arr[mid_point] > key:
            return binary_search_recursive(arr, left, mid_point-1, key)
            # recursive call to search from the first half of the array
        else:
            return binary_search_recursive(arr, mid_point+1, right, key)
            # recursive call to search from the second half of the array
    else:
        return -1       # empty array
# Time Complexity: O(lg n)


def binary_search(arr, key):
    return binary_search_recursive(arr, 0, len(arr)-1, key)


def randomized_binary_search_recursive(arr, left, right, key):
    if right >= left:
        mid_point = random.randint(left, right)
        if arr[mid_point] == key:
            return mid_point
        if arr[mid_point] > key:
            return randomized_binary_search_recursive(arr, left, mid_point-1, key)
        return randomized_binary_search_recursive(arr, mid_point+1, right, key)
# This algorithm always generates the correct answer as the mid-point element is randomly
# selected from the left and right sided elements. It is a Las Vegas randomized algorithm.
# Time Complexity: O(lg n)


def randomized_binary_search(arr, key):
    return randomized_binary_search_recursive(arr, 0, len(arr)-1, key)


def interpolation_search_recursive(arr, left, right, key):
    if left == right:
        if arr[left] == key:
            return left
        else:
            return -1
    if left < right and arr[left] <= key <= arr[right]:
        position = left + int(((right-left) / (arr[right] - arr[left])) * (key - arr[left]))
        # assigns the higher index value if it's closer to arr[right] and lower index value
        # if it's closer to arr[left] to position
        if arr[position] == key:
            return position
        if arr[position] < key:
            return interpolation_search_recursive(arr, position+1, right, key)
            # recursively search for the element = key on the right side of the position index
            # if the current element is smaller than key
        if arr[position] > key:
            return interpolation_search_recursive(arr, left, position-1, key)
            # recursively search for the element = key on the left side of the position index
            # if the current element is larger than key
    return -1
# Time Complexity: O(lg(lg n))


def interpolation_search(arr, key):
    return interpolation_search_recursive(arr, 0, len(arr)-1, key)


def jump_search(arr, key):
    n = len(arr)
    step = math.sqrt(n)
    prev = 0
    while arr[int(min(step, n) - 1)] < key:
        prev = step
        step += math.sqrt(n)
        if prev >= n:
            return -1
    while arr[int(prev)] < key:
        prev += 1
        if prev == min(step, n):
            return -1
    if arr[int(prev)] == key:
        return int(prev)
    return -1
# Time Complexity: O(√n)


def fibonacci_search(arr, key):
    n = len(arr)
    fib2 = 0
    fib1 = 1
    fib = fib2 + fib1
    while fib < n:
        fib2 = fib1
        fib1 = fib
        fib = fib2 + fib1
    offset = -1
    while fib > 1:
        i = min(offset+fib2, n-1)
        if arr[i] < key:
            fib = fib1
            fib1 = fib2
            fib2 = fib - fib1
            offset = i
        elif arr[i] > key:
            fib = fib2
            fib1 = fib1 - fib2
            fib2 = fib - fib1
        else:
            return i
    if fib1 and arr[n-1] == key:
        return n-1
    return -1
# Divide and Conquer Approach
# Time Complexity: O(lg n)


def plot_time(dict_searches, sizes, searches):
    search_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for search in searches:
        search_num += 1
        d = dict_searches[search.__name__]
        x_axis = [j + 0.05 * search_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=search.__name__)
    plt.legend()
    plt.title("Run time of Search Algorithms")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time for hundred trials (ms)")
    plt.savefig("Assignment1.png")
    plt.show()


def main():
    # my_list = random_list(min_num=1, max_num=1, size=20, do_sort=True, unique=True)
    # print(my_list)
    # key = my_list[10]
    # print(python_search(my_list, key))
    # print(linear_search(my_list, key))
    # print(binary_search(my_list, key))
    # print(randomized_binary_search(my_list, key))
    # print(interpolation_search(my_list, key))
    # print(jump_search(my_list, key))
    # print(fibonacci_search(my_list, key))
    sizes = [1000 * i for i in range(1, 11)]  # for element size
    trials = 100
    searches = [python_search, linear_search, binary_search, randomized_binary_search, interpolation_search,
                jump_search, fibonacci_search]
    dict_searches = {}
    for search in searches:
        dict_searches[search.__name__] = {}
    for size in sizes:
        for search in searches:
            dict_searches[search.__name__][size] = 0   # to initialize the dictionary
        for trial in range(1, trials+1):
            arr = random_list(1, 1000000, size, True, True)
            idx = random.randint(1, size) - 1
            key = arr[idx]
            for search in searches:
                start_time = time.time()
                idx_2 = search(arr, key)
                end_time = time.time()
                if idx_2 != idx:
                    print("We have found an error in", search.__name__, "found at", idx_2, "expected at", idx)
                net_time = end_time - start_time
                dict_searches[search.__name__][size] += 1000 * net_time
        # print(dict_searches)
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_searches).T
    print(df)
    plot_time(dict_searches, sizes, searches)


if __name__ == "__main__":
    main()
