"""
Written by: Chanyoung Gwak, 20190936
Date: Sept 29th, 2022
Program that computes the possible
"""
import sys
from collections import namedtuple


def extend_zeros(c, ln):
    nc = len(c)
    ln_ext = ln - nc
    if ln_ext > 0:
        c.extend([0] * ln_ext)


def remove_zeros(c):
    while len(c) > 0 and c[-1] == 0:
        c.pop()


def num_cases(pr):
    m, n, k, m_list, n_list = pr

    a = [i-1 for i in reversed(m_list)]
    b = [j-1 for j in n_list]
    c = karatsuba(a, b)
    extend_zeros(c, len(a) + len(b) - 1)

    # print(f'a: {a}')
    # print(f'b: {b}')
    # print(f'c: {c}')
    # c_ = mult_nsquare(a, b)
    # print(f'c_: {c_}')
    # print(f'len: {len(c)}, {len(c_)}')

    all_cases = 0
    for i, product in enumerate(c):
        left = min(0, -m + 1 + i)
        right = max(n, 1 + i)
        merge_len = right - left
        # print(f'[{left}:{right}] len: {merge_len}')
        if product == 0:
            all_cases += max(0, k - merge_len + 1)
    return all_cases


# O(n^2) time multiplication without carry
def mult_nsquare(a, b):
    na, nb = len(a), len(b)
    c = [0] * (na+nb-1)
    for i in range(na):
        for j in range(nb):
            c[i+j] += a[i] * b[j]
    return c


def add_to(a, b, k=0):
    # print(f'a:{a}, b: {b}, k: {k}')
    extend_zeros(a, len(b)+k)
    for i, bi in enumerate(b):
        a[k+i] += bi
    remove_zeros(a)


def sub_from(a, b):
    remove_zeros(b)
    remove_zeros(a)
    na, nb = len(a), len(b)
    assert na >= nb, f'a:{a}, b: {b}'
    for i, bi in enumerate(b):
        a[i] -= bi
        assert a[i] >= 0, f'a[i] = {a[i]}, b[i] = {b[i]}'
    remove_zeros(a)

# def plus(a, b, k=0):
#     na, nb = len(a), len(b)
#     c = [0] * (max(na, nb) + k)
#     for i, ai in enumerate(a):
#         c[i] += ai
#     for j, bi in enumerate(b):
#         c[k+j] += bi
#     return c
#
# def minus(a, b):
#     na, nb = len(a), len(b)
#     c = [0] * max(na, nb)
#     for i, ai in enumerate(a):
#         c[i] += ai
#     for j, bi in enumerate(b):
#         c[j] -= bi
#         assert c[j] >= 0
#     # while len(c) > 0 and c[-1] == 0:
#     #     c.pop()
#     return c


def karatsuba(a, b):
    na, nb = len(a), len(b)
    if na < nb:
        return karatsuba(b, a)
    if na == 0 or nb == 0:
        return [0]
    if na < 20:
        return mult_nsquare(a, b)
    md = na // 2
    a0 = a[:md]
    a1 = a[md:]
    b0 = b[:md]
    b1 = b[md:]
    """
    c2 = a1*b1, c0 = a0*b0, c1 = (a0+a1) * (b0+b1) - c2 -c0,
    """
    c2 = karatsuba(a1, b1)
    c0 = karatsuba(a0, b0)
    add_to(a0, a1)
    add_to(b0, b1)
    c1 = karatsuba(a0, b0)
    sub_from(c1, c2)
    sub_from(c1, c0)

    add_to(c0, c1, md)
    add_to(c0, c2, 2 * md)

    return c0


def two_indices(pattern):
    idx_list = []
    for i, p in enumerate(pattern):
        if p == 2:
            idx_list.append(i)
    return idx_list


def num_cases_by_conflict(pr):
    m, n, k, m_list, n_list = pr

    # construct a list with m_list that n_list has to match with
    # print(f'm: {m_list}')
    # print(f'n: {n_list}')
    m_idx = two_indices(m_list)
    n_idx = two_indices(n_list)
    n_idx.reverse()
    # print(f'm_idx: {m_idx}')
    # print(f'n_idx: {n_idx}')

    match_count = (k - m + 1)*(k - n + 1)  # if there is no match
    mi_len = len(m_idx)
    ni_len = len(n_idx)
    if mi_len == 0 or ni_len == 0:
        return match_count

    conflict_count = 0
    i, j = 0, 0
    while True:
        # count number of conflict for each case
        mi = m_idx[i]
        ni = n_idx[j]
        left = min(ni, mi)
        right = max(m+ni, n+mi)
        merged_len = right - left
        if merged_len <= k:
            conflict_count += (k - merged_len + 1)
        m_end = i >= mi_len - 1
        n_end = j >= ni_len - 1

        # if all the ends are computed
        if m_end and n_end:
            break
        elif m_end:
            j += 1
        elif n_end:
            i += 1
            j = 0
        else:
            gap_m = m_idx[i+1] - mi
            gap_n = n_idx[0] - n_idx[j+1]

            if gap_m <= gap_n:
                i += 1
                j = 0
            else:
                j += 1

    return match_count - conflict_count


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
            match_count += (k - total_len + 1)
    for j in range(1, k - n + 1):
        if not check_conflict(m_list, j, n_list, 0):
            total_len = max(m, n+j)
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
        print(num_cases(prob))
        # print(num_possible_cases(prob))
        # print(num_cases_by_conflict(prob))
