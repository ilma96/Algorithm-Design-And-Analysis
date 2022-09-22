# CSCI 323 / 700
# Summer 2022
# Assignment 6 - Sub-String Search
# Ilma Shaharin
import time
import pandas as pda
import matplotlib.pyplot as plt
import texttable

assn_num = 6
NO_OF_CHARS = 256


def native_search(text, pattern, verbose=True):
    return text.find(pattern)


# Source: https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/
# Slide the pattern over text one by one and check for a match.
# If a match is found, then slide by 1 again to check for subsequent matches.
def brute_force_search(text, pattern, verbose=True):
    m = len(pattern)
    n = len(text)
    for i in range(n - m + 1):
        j = 0
        while j < m:   # check for pattern match
            if verbose:
                print('i', i, 'j', j, 'm', m, 'n', n)
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            return i  # return the found indices of the pattern that matched the text
    return -1


# Source: https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/
# Match the hash value of the pattern with the hash value of current substring of text.
# If the hash values match, then only start matching individual characters.
def rabin_karp_search(text, pattern, verbose=True):
    m = len(pattern)
    n = len(text)
    j = 0
    p = 0  # hash value for pattern
    t = 0  # hash value for txt
    h = 1
    q = 101  # modulo
    d = 256  # num of characters
    for i in range(m - 1):
        h = (h * d) % q
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(n - m + 1):
        if p == t:            # if the hash values match, then only check for characters one by one
            if verbose:
                print('p', p, 't', t, 'i', i, 'j', j, 'm', m, 'n', n)
            for j in range(m):
                if text[i + j] != pattern[j]:
                    break
                else:
                    j += 1
            if j == m:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:        # to convert any negative values
                t = t + q
    return -1


# Source: https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
# We search for lps in sub-patterns. More clearly we focus on sub-strings of patterns that are prefix and also, suffix
def compute_lps_array(pattern, m, lps):
    length = 0
    lps[0] = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1


#  Slide the pattern by one and compare all characters at each shift, use a value from lps[] to decide
#  the next characters to be matched. Do not match a character that will match anyway.
def knuth_morris_pratt_search(text, pattern, verbose=True):
    m = len(pattern)
    n = len(text)
    lps = [0] * m
    j = 0  # index for pattern[]
    compute_lps_array(pattern, m, lps)
    i = 0  # index for text[]
    while (n - i) >= (m - j):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            if verbose:
                print('i', i, 'j', j, 'm', m, 'n', n)
                return i-j
            j = lps[j - 1]   # reset j as pattern is found, so, look for subsequent patterns
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]  # keep resetting j's value until j = 0
            else:
                i += 1   # j = 0, so, increment index for text[]


# Source: https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/
#  The character of the text that does not match with the current character of the pattern is called the Bad Character.
# case_1: shift the current pattern until a match is found, case_2: move past the mismatched character position
def bad_char_heuristic(string, size):
    bad_char = [-1] * NO_OF_CHARS
    for i in range(size):
        bad_char[ord(string[i])] = i
    return bad_char


def boyer_moore_search(text, pattern, verbose=True):
    m = len(pattern)
    n = len(text)
    bad_char = bad_char_heuristic(pattern, m)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            if verbose:
                print('s', s, 'm', m, 'n', n)
                return s
            s += (m - bad_char[ord(text[s + m])] if s + m < n else 1)
        else:
            s += max(1, j - bad_char[ord(text[s + j])])


# def plot_time(string_algs, sizes, algs, trials):
#     alg_num = 0
#     plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
#     for algs in algs:
#         alg_num += 1
#         d = string_algs[algs.__name__]
#         x_axis = [j + 0.05 * alg_num for j in range(len(sizes))]
#         y_axis = [d[i] for i in sizes]
#         plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=algs.__name__)
#     plt.legend()
#     plt.title("Run time of string search algorithms")
#     plt.xlabel("Size of Data")
#     plt.ylabel("Time for " + str(trials) + "Trails" "(ms)")
#     plt.savefig("Assignment" + str(assn_num) + ".png")
#     plt.show()
#
#
# def process_file(pattern_file_name, text_file_name):
#     with open(text_file_name) as file:
#         text = file.read().upper().strip()
#     with open(pattern_file_name) as file:
#         patterns = file.readlines()
#         for i in range(len(patterns)):
#             patterns[i] = patterns[i].upper().strip()
#         return text, patterns


def main():
    run_trials()
    # sizes = [10 * i for i in range(1, 11)]
    # trials = 10
    # str_algorithms = [native_search, brute_force_search, rabin_karp_search,
    #                   knuth_morris_pratt_search, boyer_moore_search]
    # results = []
    # with open("C:/Users/kashf/PycharmProjects/AlgorithmAnalysisAndDesignCSCI323/Assignment6_Text1.txt") as file:
    #     text_one = file.read()
    # with open("C:/Users/kashf/PycharmProjects/AlgorithmAnalysisAndDesignCSCI323/Assignment6_Text2.txt") as file:
    #     text_two = file.read()
    # combined_text = [text_one, text_two]
    # with open("C:/Users/kashf/PycharmProjects/AlgorithmAnalysisAndDesignCSCI323/Assignment6_Patterns.txt") as file:
    #     patterns = file.read()
    # string_algs = {}
    # for alg in str_algorithms:
    #     string_algs[alg.__name__] = {}
    #     for text in combined_text:
    #         for pattern in patterns:
    #             for trial in range(1, trials + 1):
    #                 for alg in str_algorithms:
    #                     string_algs[alg.__name__][sizes] = 0   # initialize the dictionary
    #                     result = process_file(pattern, text)
    #                     headers = ["Text", "Text-Length", "Pattern", "Pattern-Length", "String-Algo", "Position"]
    #                     tt = texttable.Texttable(500)
    #                     tt.set_cols_align(["l", "r", "l", "r", "l", "r"])
    #                     tt.set_cols_dtype(["t", "i", "t", "i", "t", "i"])
    #                     tt.add_rows(result)
    #                     tt.header(headers)
    #                     print(tt.draw())
    #                     start_time = time.time()
    #                     for pattern in result[0]:
    #                         idx = alg(text, pattern, verbose=True)
    #                         end_time = time.time()
    #                         net_time = end_time - start_time
    #                         # string_algs[alg.__name__][trials] += 1000 * net_time
    # pda.set_option("display.max_rows", 500)
    # pda.set_option("display.max_columns", 500)
    # pda.set_option("display.width", 1000)
    # # df = pda.DataFrame.from_dict(string_algs).T
    # plot_time(string_algs, sizes, str_algorithms, trials)


def run_trials():
    text = 'loopsjdbeiwm'
    pattern = 'jdb'
    idx1 = native_search(text, pattern, True)
    idx2 = brute_force_search(text, pattern, True)
    idx3 = rabin_karp_search(text, pattern, True)
    idx4 = knuth_morris_pratt_search(text, pattern, True)
    idx5 = boyer_moore_search(text, pattern, True)
    print('Native Search: ', idx1)
    print('Brute Force Search: ', idx2)
    print('Rabin_Karp_Search: ', idx3)
    print('Knuth_Morris_Pratt_Search: ', idx4)
    print('Boyer_Moore_Search: ', idx5)


if __name__ == "__main__":
    main()
