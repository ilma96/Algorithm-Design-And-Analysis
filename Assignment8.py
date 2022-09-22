# CSCI 323 / 700
# Summer 2022
# Assignment 8 - Recurrence Relations
# Ilma Shaharin
import math


dict_funcs = {}


def eval_func(func, n):
    func_name = func.__name__
    if func_name not in dict_funcs:
        dict_funcs[func_name] = {}
    dict_func = dict_funcs[func_name]
    if n not in dict_func:
        dict_func[n] = func(func, n)
    return dict_func[n]


# T(n) = 2T(n/2) + n
def f1_mergesort(func, n):
    if n == 1:
        return 0
    else:
        return 2 * eval_func(func, int(n / 2)) + n


# f(n) = f(n - 1) + f(n - 2)
def f2_fibonacci(func, n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return eval_func(func, n - 1) + eval_func(func, n - 2)


# f(n) = f(3n/4) + log(n/2)
def f3_improved_parallel_mergesort(func, n):
    if n == 1:
        return 1
    else:
        return eval_func(func, int(3 * n / 4)) + int(math.log(n / 2))


# f(n) = f(n - 1) + n - 1
def f4_bubblesort(func, n):
    if n == 1:
        return 0
    else:
        return eval_func(func, n - 1) + n - 1


# f(n) = f(n-1) + 1
def f5_linear_search(func, n):
    if n == 1:
        return 1
    else:
        return eval_func(func, n - 1) + 1


# f(n) = f(n/2) + 2
def f6_binary_search(func, n):
    if n == 1:
        return 1
    else:
        return eval_func(func, int(n / 2)) + 2


# f(n) = 4 * f(n/2) + n
def f7_dc_integer_mult(func, n):
    if n == 1:
        return 1
    else:
        return 4 * eval_func(func, int(n / 2)) + n


# f(n) = 3 * f(n/2) + n
def f8_karatsuba_integer_mult(func, n):
    if n == 1:
        return 1
    else:
        return 3 * eval_func(func, int(n / 2)) + n


# f(n) = 8 * f(n/2) + n^2
def f9_dc_matrix_mult(func, n):
    if n == 1:
        return 1
    else:
        return 8 * eval_func(func, int(n / 2)) + n * n


# f(n) = 7 * f(n/2) + n^2
def f10_strassen_matrix_mult(func, n):
    if n == 1:
        return 1
    else:
        return 7 * eval_func(func, int(n / 2)) + n * n


# T(n) = 125T(n/5) + 5n
def f11_midterm_winter_2022(func, n):
    if n == 1:
        return 1
    else:
        return 125 * eval_func(func, int(n / 5)) + 5 * n


# T(n) = 4T(n/3) + n
def f12_midterm_summer_2021(func, n):
    if n == 1:
        return 2
    else:
        return 4 * eval_func(func, int(n / 3)) + n


# T(n) = 4T(n/2) + 2n
def f13_midterm_spring_2016(func, n):
    if n == 1:
        return 2
    else:
        return 4 * eval_func(func, int(n / 2)) + 2 * n


# T(n) = 8T(n/2) + n
def f14_midterm_fall_2018(func, n):
    if n == 1:
        return 1
    else:
        return 8 * eval_func(func, int(n / 2)) + n


# T(n) = 9T(n/3) + n
def f15_midterm_summer_2019(func, n):
    if n == 1:
        return 1
    else:
        return 9 * eval_func(func, int(n / 3)) + n


# T(n) = sum i=0 to n of (T(i) * T(n-1-i))
def f16_catalan_number(func, n):
    if n == 0:
        return 1
    else:
        c = 0
        for i in range(n):
            c += eval_func(func, i) * eval_func(func, n - 1 - i)
        return c


# T(n) = T(n-1) + n^2
def f17_sum_of_squares(func, n):
    if n == 1:
        return 1
    else:
        return eval_func(func, n - 1) + n * n


# T(n) = T(n-1) + n^3
def f18_sum_of_cubes(func, n):
    if n == 1:
        return 1
    else:
        return eval_func(func, n - 1) + n * n * n


# T(n) = 2T(n/2) + n-1
def f19_quick_sort(func, n):
    if n == 1:
        return 0
    else:
        return 2 * eval_func(func, int(n / 2)) + n - 1


# # f(n) = f(n - 1) + f(n - 2)
def f20_lucas_number(func, n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n == 2:
        return 3
    else:
        return eval_func(func, n - 1) + eval_func(func, n - 2)


def call_and_print(func, n, desc):
    print(func.__name__, desc, "for n =", n, "is", eval_func(func, n))


def print_dicts():
    for func in dict_funcs:
        print(func, dict_funcs[func])


def main():
    call_and_print(f1_mergesort, 256, "f(n) = 2*f(n/2) + n")
    call_and_print(f2_fibonacci, 256, "f(n) = f(n-1) + f(n-2)")
    call_and_print(f3_improved_parallel_mergesort, 256, "f(n) = 3n/2 + log(n/2)")
    call_and_print(f4_bubblesort, 256, "f(n) = f(n-1) + n - 1")
    call_and_print(f5_linear_search, 256, "f(n) = f(n-1) + 1")
    call_and_print(f6_binary_search, 256, "f(n) = f(n/2) + 2")
    call_and_print(f7_dc_integer_mult, 256, "f(n) = 4 * f(n/2) + n")
    call_and_print(f8_karatsuba_integer_mult, 256, "f(n) = 3 * f(n/2) + n")
    call_and_print(f9_dc_matrix_mult, 256, "f(n) = 8 * f(n/2) + n^2")
    call_and_print(f10_strassen_matrix_mult, 256, "f(n) = 7 * f(n/2) + n^2")
    call_and_print(f11_midterm_winter_2022, 625, "T(n) = 125T(n/5) + 5n")
    call_and_print(f12_midterm_summer_2021, 243, "T(n) = 4T(n/3) + n")
    call_and_print(f13_midterm_spring_2016, 256, "T(n) = 4T(n/2) + 2n")
    call_and_print(f14_midterm_fall_2018, 256, "T(n) = 8T(n/2) + n")
    call_and_print(f15_midterm_summer_2019, 243, "T(n) = 9T(n/3) + n")
    call_and_print(f16_catalan_number, 100, "T(n) = sum i=0 to n of (T(i) * T(n-1-i))")
    call_and_print(f17_sum_of_squares, 150, "T(n) = T(n-1) + n^2")
    call_and_print(f18_sum_of_cubes, 256, "T(n) = T(n-1) + n^3")
    call_and_print(f19_quick_sort, 256, "f(n) = 2*f(n/2) + n - 1")
    call_and_print(f20_lucas_number, 256, "f(n) = f(n-1) + f(n-2)")
    print_dicts()


if __name__ == "__main__":
    main()
