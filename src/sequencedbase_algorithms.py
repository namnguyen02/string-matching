from math import floor, ceil
import numpy as np
def nw(x, y, match=1, mismatch=1, gap=1):
    nx = len(x)
    ny = len(y)
    # Optimal score at each possible pair of characters.
    F = np.zeros((nx + 1, ny + 1))
    F[:, 0] = np.linspace(0, -nx * gap, nx + 1)
    F[0, :] = np.linspace(0, -ny * gap, ny + 1)
    # Pointers to trace through an optimal aligment.
    P = np.zeros((nx + 1, ny + 1))
    P[:, 0] = 3
    P[0, :] = 4
    # Temporary scores.
    t = np.zeros(3)
    for i in range(nx):
        for j in range(ny):
            if x[i] == y[j]:
                t[0] = F[i, j] + match
            else:
                t[0] = F[i, j] - mismatch
            t[1] = F[i, j+1] - gap
            t[2] = F[i+1, j] - gap
            tmax = np.max(t)
            F[i+1, j+1] = tmax
            if t[0] == tmax:
               #  print('a', tmax)
                P[i+1, j+1] += 2
            if t[1] == tmax:
               #  print('b', tmax)
                P[i+1, j+1] += 3
            if t[2] == tmax:
                P[i+1, j+1] += 4
    # Trace through an optimal alignment.
    i = nx
    j = ny
    rx = []
    ry = []
    while i > 0 or j > 0:
        if P[i, j] in [2, 5, 6, 9]:
            rx.append(x[i-1])
            ry.append(y[j-1])
            i -= 1
            j -= 1
        elif P[i, j] in [3, 5, 7, 9]:
            rx.append(x[i-1])
            ry.append('-')
            i -= 1
        elif P[i, j] in [4, 6, 7, 9]:
            rx.append('-')
            ry.append(y[j-1])
            j -= 1
    # Reverse the strings.
    rx = ''.join(rx)[::-1]
    ry = ''.join(ry)[::-1]
   #  print()
   #  return '\n'.join([rx, ry])
    return 1 - F[-1][-1] / max(len(x), len(y))
def jaro_distance(s1, s2):
    if (s1 == s2):
        return 1.0
    len1 = len(s1)
    len2 = len(s2)
    max_dist = floor(max(len1, len2) / 2) - 1
    match = 0
    hash_s1 = [0] * len(s1)
    hash_s2 = [0] * len(s2)
    for i in range(len1):
        for j in range(max(0, i - max_dist),
                       min(len2, i + max_dist + 1)):
            if (s1[i] == s2[j] and hash_s2[j] == 0):
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break
    if (match == 0):
        return 0.0

    # Number of transpositions
    t = 0
    point = 0

    for i in range(len1):
        if (hash_s1[i]):
            while (hash_s2[point] == 0):
                point += 1

            if (s1[i] != s2[point]):
                t += 1
            point += 1
    t = t//2
    return (match / len1 + match / len2 +
            (match - t) / match) / 3.0


def jaro_Winkler(s1, s2):

    jaro_dist = jaro_distance(s1, s2)
    if (jaro_dist > 0.7):
        prefix = 0

        for i in range(min(len(s1), len(s2))):
            if (s1[i] == s2[i]):
                prefix += 1
            else:
                break
        prefix = min(4, prefix)
        jaro_dist += 0.1 * prefix * (1 - jaro_dist)

    return jaro_dist

