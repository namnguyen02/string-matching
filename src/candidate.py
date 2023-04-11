# Dùng để tìm ra các candidate
from sequencedbase_algorithms import jaro_distance
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


def inverted_index(query, documents):
    index = {}

    for i, doc in enumerate(documents):
        words = doc.lower().split()
        for word in words:
            if word not in index:
                index[word] = []
            index[word].append(i)

    words = query.lower().split()
    result = set(index[words[0]])
    for word in words[1:]:
        result = result.intersection(set(index[word]))
    return [documents[i] for i in result]


def position_filter(query, strings):
    query_len = len(query)
    result = []

    for string in strings:
        string_len = len(string)
        if query_len > string_len:
            continue
        i = 0
        while i <= string_len - query_len:
            j = 0
            while j < query_len and query[j] == string[i+j]:
                j += 1
            if j == query_len:
                result.append(string)
                break
            if j == 0:
                i += 1
            else:
                i += j

    return result
