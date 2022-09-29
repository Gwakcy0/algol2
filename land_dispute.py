"""
Written by: Chanyoung Gwak, 20190936
Date: Sept 29th, 2022
Program that computes the possible
"""
import sys
from collections import namedtuple


# check if any conflict occurs
def check_conflict(arr1, offset1, arr2, offset2):
    ln = min(len(arr1)-offset1, len(arr2)-offset2)
    for i in range(ln):
        if arr1[offset1 + i] + arr2[offset2 + i] == 4:
            return True
    return False


def num_possible_cases(pr):
    """
    There are k - m + 1 possible cases for m
    and k - n + 1 cases for n

    Let Taekang starts from index i, Seungjun from index j,
    where i is in range(k-m+1) and j is in range(k-n+1).
    Two areas are allocated without conflict if
        m_list[p-i] + n_list[p-j] < 3 for all p in range(k)

    For other approach, we can compute the relative position of two lands first,
    and then compute number of cases according to the remaining margin.
    """
    match_count = 0
    m, n, k, m_list, n_list = pr

    for i in range(k - m + 1):
        if not check_conflict(m_list, 0, n_list, i):
            total_len = max(m+i, n)
            # print(f'i:{i}', total_len)
            match_count += (k - total_len + 1)
    for j in range(1, k - n + 1):
        if not check_conflict(m_list, j, n_list, 0):
            total_len = max(m, n+j)
            # print(f'j:{j}', total_len)
            match_count += (k - total_len + 1)

    return match_count % 1234567890


if __name__ == '__main__':
    # set recursion limit
    sys.setrecursionlimit(10000000)
    sys.stdin = open('input2.txt', 'r')

    # receive input data
    n_test = int(input())
    testcases = []

    Problem = namedtuple('Problem', 'm n k m_list n_list')

    for _ in range(n_test):
        m, n, k = map(int, sys.stdin.readline().split())
        m_list = list(map(int, sys.stdin.readline().split()))
        n_list = list(map(int, sys.stdin.readline().split()))
        assert (len(m_list) == m and len(n_list) == n)
        testcases.append(Problem(m, n, k, m_list, n_list))

    # evaluate data
    for prob in testcases:
        # print(prob)
        print(num_possible_cases(prob))
