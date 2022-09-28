"""
Written by: Chanyoung Gwak, 20190936
Date: Sept 28th, 2022
Program that finds a personal color using some algorithm
"""
import sys


# convert string to hexadicimal
def str_to_hex(hex_string: str):
    return int(hex_string, 16)


# compress rgb numbers to a hexadecimal number
# also returns boolean of whether it is achromatic
def compress(rgb):
    digits = [rgb >> 8, (rgb >> 4) & 15, rgb & 15]

    # if achromatic
    if digits[0] == digits[1] == digits[2]:
        return digits[0], True
    # if chromatic
    else:
        return sum(digits) & 15, False


# find personal color
def find_color(rgb, k):
    if len(rgb) <= 1:
        return rgb[0]
    else:
        # merge every 3 elements and save
        new_rgb = []
        for i in range(0, len(rgb), 3):
            c1, b1 = compress(rgb[i])
            c2, b2 = compress(rgb[i+1])
            c3, b3 = compress(rgb[i+2])
            if b1 and b2 and b3:
                c2 = 15
            clr = (c1 << 8) + (c2 << 4) + c3
            # print('c1~3: ', hex(c1), hex(c2), hex(c3))
            # print('in sum:', hex(clr))
            new_rgb.append(clr)
        return find_color(new_rgb, k-1)


if __name__ == '__main__':
    # set recursion limit
    sys.setrecursionlimit(10000000)

    # receive input data
    n_test = int(input())
    testcases = []
    colors = []

    for _ in range(n_test):
        n = int(input())
        rgb_nums = list(input().split())
        testcases.append((n, rgb_nums))

    # evaluate data
    for n, nums in testcases:
        # convert input data into hexadecimal number
        nums_hex = list(map(str_to_hex, nums))
        # find personal color recursively
        colors.append(find_color(nums_hex, n))

    # print output
    for color in colors:
        print(str.upper(hex(color)[2:]).zfill(3))
