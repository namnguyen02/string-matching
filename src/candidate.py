# Dùng để tìm ra các candidate
from jaro import jaro_distance
import numpy as np

def size_filtering(row, dataset, fields):
    x = ""
    for field in fields:
        x += row[field] + ","
    x = x.replace(',', ' ').split()
    max = len(x) / 0.9
    min = len(x) * 0.9
    lst = []

    for index, ele in dataset.iterrows():
        y = ""
        for field in fields:
            y += ele[field] + ","
        y = y.replace(',', ' ').split()
        if len(y) <= max and len(y) >= min:
            lst.append(index)

    return dataset.loc[lst]
def bound_filtering(row1, row2, fields):
    ans = []
    x = ""
    for field in fields:
        x += row1[field] + ","
    bag1 = x.replace(',', ' ').split()
    y = ""
    for field in fields:
        y += row2[field] + ","
    bag2 = y.replace(',', ' ').split()

    n = len(bag1)
    m = len(bag2)

    matrix = np.zeros((n, m))
    bx = []
    by = []
    for i in range(n):
        for j in range(m):
            matrix[i][j] = jaro_distance(bag1[i], bag2[j])
    for i in range(n):
        maxval = -np.inf
        pos = 0
        for j in range(m):
            if matrix[i][j] > maxval:
                maxval = matrix[i][j]
                pos = j
        bx.append((i, pos, matrix[i][pos]))
    for j in range(m):
        maxval = -np.inf
        pos = 0
        for i in range(n):
            if matrix[i][j] > maxval:
                maxval = matrix[i][j]
                pos = i
        by.append((pos, j, matrix[pos][j]))
    
    # Upper bound
    common = set()
    for i in bx: common.add(i)
    for i in by: common.add(i)
    sum = 0
    for i in common:
        sum += i[2]
    UB = sum / (n + m - len(common))
    # Lower bound
    size = 0
    sum = 0
    for i in bx:
        if i in by:
            size += 1
            sum += i[2]
    LB = sum / (n + m - size)
    return [LB, UB]