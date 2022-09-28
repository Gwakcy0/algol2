"""
Written by: Chanyoung Gwak, 20190936
Date: Sept 28th, 2022
Program that finds a closest pair from the 3-dimensional space
"""
import sys
from itertools import combinations
import cProfile

def dist(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])


def min_dist_brute_force(pts, delta=None):
    assert (len(pts) > 1 or delta is not None)
    if len(pts) <= 1:
        return delta
    if delta is None:
        delta = dist(pts[0], pts[1])
    for p1, p2 in combinations(pts, 2):
        d = dist(p1, p2)
        if delta > d:
            delta = d
    return delta


def min_dist(pts, coord=0, delta=None):
    assert (len(pts) > 1 or delta is not None)
    if len(pts) <= 1:
        return delta
    if delta is None:
        delta = dist(pts[0], pts[1])

    # if number of points smaller than 5, use brute-force algorithm
    if len(pts) < 5:
        return min_dist_brute_force(pts)

    # sort points with respect to x (or other axes)
    pts.sort(key=lambda p: p[coord])

    # find pivot point
    piv_idx = len(pts) // 2
    piv_crd = pts[piv_idx][coord]

    # divide region with the plane coord = pivot.coord, and recursively find min_dist for each region
    dist1 = min_dist(pts[0:piv_idx], coord, delta)
    dist2 = min_dist(pts[piv_idx:], coord, delta)

    # find a smallest distance delta
    delta = min(dist1, dist2)

    # print('='*10)
    # print('coord:', coord, 'dist:', dist1, dist2)
    # print('pts', pts)

    # There may be some pairs across two regions with smaller distances.
    # Find points in the region of 2*delta thickness
    pts_within = []
    lower_bound = piv_crd - delta
    upper_bound = piv_crd + delta
    for pt in pts:
        if lower_bound < pt[coord] < upper_bound:
            pts_within.append(pt)

    # calculate distance in that region, and, if possible switch the coordinate
    # print('pts_within', pts_within)
    if coord < 2:
        delta_within = min_dist(pts_within, coord + 1, delta)
    else:
        delta_within = min_dist_brute_force(pts)

    return min(delta, delta_within)


if __name__ == '__main__':
    # set recursion limit
    sys.setrecursionlimit(1000000)

    # receive input data
    n_test = int(input())
    testcases = []

    for _ in range(n_test):
        n_point = int(input())
        points = []
        for _ in range(n_point):
            points.append(tuple(map(int, input().split())))
        testcases.append(points)

    # evaluate data
    for points in testcases:
        cProfile.run('print(min_dist(points))')


