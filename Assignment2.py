# CSCI 323 / 700
# Summer 2022
# Assignment 2 - Sorting Algorithms
# Ilma Shaharin
import copy
import math
import random
import time
import pandas as pd
import matplotlib.pyplot as plt


def random_list(range_max, size):
    numbers = []
    i = 0
    while i < size:
        rnd = random.randint(1, range_max)
        i += 1
        numbers.append(rnd)
    return numbers


def native_sort(arr):
    arr.sort()
    return arr
# mix of Insertion and Merge Sort = Tim Sort


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # swap the numbers
    return arr
# Source: https://www.geeksforgeeks.org/bubble-sort/
# Sorts by comparing two adjacent values
# Implementation is stable
# Not ideal for large dataset sorting strategy as its worst-case is quadratic


def selection_sort(arr):
    # n = len(arr)
    for i in range(len(arr)):
        min_index = i
        for j in range(i + 1, len(arr)):
            if arr[min_index] > arr[j]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr
# Source: https://www.geeksforgeeks.org/selection-sort/
# Repeatedly selects the minimum value from the unsorted part and puts it at the beginning
# Thus, it maintains two sub-arrays (remaining unsorted, already sorted)
# Implementation is NOT stable
# Quadratic Runtime


def insertion_sort(arr):
    for i in range(len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
# Source: https://www.geeksforgeeks.org/insertion-sort/
# in-place sorting algorithm
# Compares the key with its previous value. If the key is smaller than other values before, move the positions of those
# elements one position up to make space for the swapped element
# Implementation is stable
# Ideal for smaller datasets and partially sorted dataset
# Quadratic Runtime: worst-case; improved runtime with binary search


def cocktail_sort(arr):
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end = end - 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start = start + 1
    return arr
# Source: https://www.geeksforgeeks.org/cocktail-sort/
# A variation of Bubble Sort
# Loops through the array both forward and backward, which makes this algorithm more efficient than bubble sort
# Another name is Bi-Directional sorting algorithm
# Implementation is stable
# Quadratic Runtime: worst-case, average-case


def shell_sort(arr):
    n = len(arr)
    gap = int(n / 2)
    while gap > 0:
        j = gap
        while j < n:
            i = j - gap
            while i >= 0:
                if arr[i + gap] > arr[i]:
                    break
                else:
                    arr[i + gap], arr[i] = arr[i], arr[i + gap]
                i = i - gap
            j += 1
        gap = int(gap / 2)
    return arr
# Source: https://www.geeksforgeeks.org/shell-sort/
# A variation of Insertion Sort
# Ideal for medium to large-sized datasets.
# Quadratic Runtime


def merge_sort(arr):
    n = len(arr)
    if n > 1:
        mid = int(n/2)
        left_side = arr[:mid]
        right_side = arr[mid:]
        merge_sort(left_side)
        merge_sort(right_side)
        i = j = k = 0
        while i < len(left_side) and j < len(right_side):
            if left_side[i] < right_side[j]:
                arr[k] = left_side[i]
                i += 1
            else:
                arr[k] = right_side[j]
                j += 1
            k += 1
        while i < len(left_side):
            arr[k] = left_side[i]
            i += 1
            k += 1
        while j < len(right_side):
            arr[k] = right_side[j]
            j += 1
            k += 1
    return arr
# Source: https://www.geeksforgeeks.org/merge-sort/
# Divide-and-Conquer Approach
# In this algorithm, the array is initially divided into two equal halves, and then they are combined in a sorted manner
# Implementation is stable
# Linearithmic Runtime


def quick_sort_recursive(arr, low, high):
    if low >= high:
        return arr
    pivot = low
    i = low
    j = high
    while i < j:
        while i < j and arr[j] > arr[pivot]:
            j -= 1
        while i < j and arr[i] <= arr[pivot]:
            i += 1
        arr[i], arr[j] = arr[j], arr[i]
    arr[pivot], arr[j] = arr[j], arr[pivot]
    quick_sort_recursive(arr, low, j - 1)
    quick_sort_recursive(arr, j + 1, high)
    return arr


def quick_sort(arr):
    n = len(arr)
    return quick_sort_recursive(arr, 0, n - 1)
# Source: https://www.geeksforgeeks.org/quick-sort/
# In this algorithm, an element is picked as a pivot, and it partitions the given array around the picked pivot
# In-Place Algorithm
# Implementation is NOT stable


def heapify(arr, n, i):
    largest = i
    left_side = 2 * i + 1
    right_side = 2 * i + 2
    if left_side < n and arr[largest] < arr[left_side]:
        largest = left_side
    if right_side < n and arr[largest] < arr[right_side]:
        largest = right_side
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
# The process of reshaping a binary tree into a Heap data structure is known as ‘heapify’


def heap_sort(arr):
    n = len(arr)
    # Build the Max-Heap
    for i in range(int(n/2) - 1, -1, -1):
        heapify(arr, n, i)
    # Extract the elements one-by-one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr
# Source: https://www.geeksforgeeks.org/heap-sort/
# In-Place Algorithm
# Implementation is NOT stable


def counting_sort(arr):
    n = len(arr)
    maximum_val = 0
    for i in range(n):
        if arr[i] > maximum_val:
            maximum_val = arr[i]
    tables = [0] * (maximum_val + 1)
    for i in arr:
        tables[i] += 1
    i = 0
    for j in range(maximum_val + 1):
        for b in range(tables[j]):
            arr[i] = j
            i += 1
    return arr
# Source: https://www.geeksforgeeks.org/counting-sort/
# A sorting technique based on keys between a specific range
# Implementation is stable
# Linear Runtime


def insertion_sort_for_bucket(x):
    n = len(x)
    for i in range(1, n):
        up = x[i]
        j = i - 1
        while j >= 0 and up < x[j]:
            x[j + 1] = x[j]
            j -= 1
        x[j + 1] = up
    return x


def bucket_sort(arr):
    bucket_num = round(math.sqrt(len(arr)))
    maximum = max(arr)
    arr1 = []
    for i in range(bucket_num):
        arr1.append([])
    for j in arr:
        idx = math.ceil(j * bucket_num / maximum)
        arr1[idx - 1].append(j)
    for i in range(bucket_num):
        arr1[i] = insertion_sort_for_bucket(arr1[i])
    k = 0
    for i in range(bucket_num):
        for j in range(len(arr1[i])):
            arr[k] = arr1[i][j]
            k += 1
    return arr
# Source: https://www.geeksforgeeks.org/bucket-sort/


def counting_sort_for_radix(arr, val):
    count_array = [0] * 10
    n = len(arr)
    for i in range(n):
        element = int((arr[i] / val)) % 10
        count_array[element] += 1
    for i in range(1, 10):
        count_array[i] += count_array[i - 1]
    output_array = [0] * n
    i = n - 1
    while i >= 0:
        current_element = arr[i]
        element = int((arr[i] / val)) % 10
        count_array[element] -= 1
        new_position = count_array[element]
        output_array[new_position] = current_element
        i -= 1
    return output_array


def radix_sort(arr):
    max_element = max(arr)
    d = 1
    while max_element > 0:
        max_element /= 10
        d += 1
    place_val = 1
    output_array = arr
    while d > 0:
        output_array = counting_sort_for_radix(output_array, place_val)
        place_val *= 10
        d -= 1
    return output_array
# Source: https://stackabuse.com/radix-sort-in-python/


def pigeonhole_sort(arr):
    my_min = min(arr)
    my_max = max(arr)
    size = my_max - my_min + 1
    holes = [0] * size
    for x in arr:
        assert type(x) is int, "integers only please"
        holes[x - my_min] += 1
    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            arr[i] = count + my_min
            i += 1
    return arr
# Source: https://www.geeksforgeeks.org/pigeonhole-sort/
# A sorting algorithm that is suitable for sorting lists of elements
# where the number of elements and the number of possible key values are approximately the same
# Moves items twice: once to the bucket array [holes] and again to the final destination


def stooge_sort_recursive(arr, low, high):
    if low >= high:
        return
    if arr[low] > arr[high]:
        t = arr[low]
        arr[low] = arr[high]
        arr[high] = t
    if high - low + 1 > 2:
        t = int((high - low + 1) / 3)
        stooge_sort_recursive(arr, low, high - t)
        stooge_sort_recursive(arr, low + t, high)
        stooge_sort_recursive(arr, low, high - t)
    return arr


def stooge_sort(arr):
    return stooge_sort_recursive(arr, 0, len(arr) - 1)
# https://www.geeksforgeeks.org/python-program-for-stooge-sort/


def plot_time(dict_sorts, sizes, sorts):
    sort_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for sort in sorts:
        sort_num += 1
        d = dict_sorts[sort.__name__]
        x_axis = [j + 0.05 * sort_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=sort.__name__)
    plt.legend()
    plt.title("Run time of Sorting Algorithms")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time for ten trials (ms)")
    plt.savefig("Assignment2.png")
    plt.show()


def main():
    sizes = [10, 100]  # for element sizes
    trials = 10
    sorts = [native_sort, bubble_sort, selection_sort, insertion_sort, cocktail_sort, shell_sort,
             merge_sort, quick_sort, heap_sort, counting_sort, bucket_sort, radix_sort, pigeonhole_sort, stooge_sort]
    dict_sorts = {}
    for sort in sorts:
        dict_sorts[sort.__name__] = {}
    for size in sizes:
        for sort in sorts:
            dict_sorts[sort.__name__][size] = 0    # to initialize the dictionary
        for trial in range(1, trials + 1):
            arr = random_list(100000, size)
            for sort in sorts:
                unsorted_arr1 = copy.copy(arr)
                unsorted_arr2 = copy.copy(arr)
                start_time = time.time()
                test_sort = sort(unsorted_arr1)
                end_time = time.time()
                built_sort = native_sort(unsorted_arr2)
                if built_sort != test_sort:
                    print("We have found an error in", sort.__name__)
                net_time = end_time - start_time
                dict_sorts[sort.__name__][size] += 1000 * net_time
        dict_sorts[sort.__name__][size] /= trials
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_sorts).T
    print(df)
    plot_time(dict_sorts, sizes, sorts)


if __name__ == "__main__":
    main()
