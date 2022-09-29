"""
Written by: Chanyoung Gwak, 20190936
Date: Sept 28th, 2022
Program that finds a closest pair from the 3-dimensional space
"""
import sys
from itertools import combinations
from operator import itemgetter
from bisect import bisect_left, bisect_right
import cProfile


# find the index such that val < lst[i]
def binary_search_left(lst, val, axis, left=None, right=None):
    if not left:
        left = 0
    if not right:
        right = len(lst)
    if left >= right:
        return left
    median = left + (right - left) // 2
    if lst[median][axis] < val:
        return binary_search_left(lst, val, axis, median+1, right)
    else:
        return binary_search_left(lst, val, axis, left, median)


def binary_search_right(lst, val, axis, left=None, right=None):
    if not left:
        left = 0
    if not right:
        right = len(lst)
    if left >= right:
        return right
    median = left + (right - left) // 2
    if lst[median][axis] > val:
        return binary_search_right(lst, val, axis, left, median)
    else:
        return binary_search_right(lst, val, axis, median+1, right)


# distance between two points
def dist(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])


# distance within a set
def min_dist_brute_force(pts, delta=None):
    if not pts:
        return delta
    if delta is None:
        delta = dist(pts[0], pts[1])
    for p1, p2 in combinations(pts, 2):
        d = dist(p1, p2)
        if delta > d:
            delta = d
    return delta


# distance between two bipartite set
def min_dist_bipartite(pts1, pts2, delta=None):
    if not pts1 or not pts2:
        return delta
    if delta is None:
        delta = dist(pts1[0], pts2[0])

    for p1 in pts1:
        for p2 in pts2:
            d = dist(p1, p2)
            if d < delta:
                delta = d
    return delta


def min_dist(pts, axis=0, delta=None):
    # if number of points smaller than 4, use brute-force algorithm
    p_len = len(pts)
    if p_len < 4:
        return min_dist_brute_force(pts, delta)

    # sort points with respect to the axis
    pts.sort(key=itemgetter(axis))

    # find pivot point
    piv_idx = p_len // 2
    piv_val = pts[piv_idx][axis]

    # divide region with the plane coord = pivot.coord, and recursively find min_dist for each region
    new_axis = (axis + 1) % 3
    dist1 = min_dist(pts[:piv_idx], new_axis, delta)
    dist2 = min_dist(pts[piv_idx:], new_axis, delta)

    # find the smallest distance delta
    delta = min(dist1, dist2)

    # print('='*10)
    # print('coord:', coord, 'dist:', dist1, dist2)
    # print('pts', pts)

    # There may be some pairs across two regions with smaller distances.
    # Find points in the region of 2*delta thickness
    lower_bound = piv_val - delta
    upper_bound = piv_val + delta
    axis_list = [p[axis] for p in pts]
    i = bisect_left(axis_list, lower_bound) + 1
    j = bisect_right(axis_list, upper_bound)
    piv_idx -= i

    # calculate distance in that region
    # print('pts_within', pts_within)
    delta_within = min_dist(pts[i:j], new_axis, delta)
    # if axis < 2:
    #     delta_within = min_dist(pts_within, axis + 1, delta)
    # else:
    #     delta_within = min_dist_brute_force(pts)
    # delta = min(delta, delta_within)

    return min(delta, delta_within)

if __name__ == '__main__':
    # set recursion limit
    sys.setrecursionlimit(10000000)
    #sys.stdin = open('input.txt', 'r')

    # receive input data
    n_test = int(sys.stdin.readline())
    testcases = []

    for _ in range(n_test):
        n_point = int(sys.stdin.readline())
        points = []
        for _ in range(n_point):
            points.append(tuple(map(int, sys.stdin.readline().split())))
        testcases.append(points)

    # evaluate data
    for points in testcases:
        print(min_dist(points))
        # cProfile.run('print(min_dist(points))')




