# CSCI 323 / 700
# Summer 2022
# Assignment 5 - Palindromic Substrings and Subsequences
# Ilma Shaharin
# Source: GeeksForGeeks.
# Special thanks to Professor Teitelman and fellow classmate, Sagar.
import time
import re
import texttable as texttable


# Source: https://www.geeksforgeeks.org/longest-palindrome-substring-set-1/ [Dynamic Approach]
def lpsst(s):
    n = len(s)
    table = [[0 for x in range(n)] for y in range(n)]  # a boolean table to fill up in a bottom-up style
    max_length = 1
    i = 0
    while i < n:
        table[i][i] = True   # palindrome found
        i += 1
    start = 0
    i = 0
    while i < n - 1:
        if s[i] == s[i + 1]:
            table[i][i + 1] = True  # palindrome found
            start = i
            max_length = 2
        i += 1
    k = 3
    while k <= n:
        i = 0
        while i < (n - k + 1):
            j = i + k - 1    # get the last index of sub-string from first index, i and length, k
            if table[i + 1][j - 1] and s[i] == s[j]:
                # check for sub-string from ith index to jth index if and only if s[i + 1] to s[j-1] is a palindrome
                table[i][j] = True
                if k > max_length:
                    start = i
                    max_length = k
            i += 1
        k += 1
    return s[start: start + max_length]
# Time Complexity: Quadratic


# Source: https://www.geeksforgeeks.org/print-longest-palindromic-subsequence/
def lpssq_helper(x, y):
    m = len(x)
    n = len(y)
    length = [[0] * (n + 1) for i in range(m + 1)]
    # there was a bug here previously, changes made: putting (m+1) inside a for-loop to not print garbage answers
    for i in range(n + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                length[i][j] = 0  # length[i][j] will contain the length of lcs of x[0,...,i-1] and y[0,...,j-1]
            elif x[i - 1] == y[j - 1]:
                length[i][j] = length[i - 1][j - 1] + 1
            else:
                length[i][j] = max(length[i - 1][j], length[i][j - 1])
    index = length[m][n]
    lcs2 = [""] * (index + 1)  # removed "\n" to avoid ambiguity
    i, j = m, n
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            # If current character in X[0,...,i-1] and Y[0,...,j-1] are same, then current character is part of LCS
            lcs2[index - 1] = x[i - 1]   # store that common character into the longest common subsequence array
            i -= 1
            j -= 1
            index -= 1
        elif length[i - 1][j] > length[i][j - 1]:
            # find the larger value between the sequences and go in that direction
            i -= 1
        else:
            j -= 1
    ans = ""
    for z in range(len(lcs2)):
        ans += lcs2[z]  # store the longest common subsequence in the ans and then returning its value
    return ans


def lpssq(s):
    rev = s[:: -1]  # reverse the passed string
    return lpssq_helper(s, rev)
# Time Complexity: Quadratic


def test_lpsst_and_lpssq(s):
    st = lpsst(s)
    sq = lpssq(s)
    print("The test string is ", s, "with length", len(s))
    print("Its Longest Palindromic Substring is", st, "with length", len(st))
    print("Its Longest Palindromic Subsequence is", sq, "with length", len(sq))


def process_file(file_name):
    results = []
    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            line = line.upper()
            line = re.sub(r'[^A-Z]', '', line)
            start_time = time.time()
            st = lpsst(line)
            end_time = time.time()
            time_st = end_time - start_time
            start_time = time.time()
            sq = lpssq(line)
            end_time = time.time()
            time_sq = end_time - start_time
            results.append([line, len(line), st, len(st), time_st, sq, len(sq), time_sq])
    return results


def main():
    print(test_lpsst_and_lpssq("ilmashaharin"))
    results = process_file("palindromes.txt")
    # results = process_file("sentences.txt")
    headers = ["String", "Length", "LPSST", "Length", "Time", "LPSSQ", "Length", "Time"]
    tt = texttable.Texttable(500)
    tt.set_cols_align(["l", "r", "l", "r", "r", "l", "r", "r"])
    tt.set_cols_dtype(["t", "i", "t", "i", "f", "t", "i", "f"])
    tt.add_rows(results)
    tt.header(headers)
    print(tt.draw())


if __name__ == "__main__":
    main()
