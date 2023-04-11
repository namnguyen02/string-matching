from math import floor, ceil
import numpy as np

def affine_gap_measure(str1, str2):
  str1 = str1.lower()
  str2 = str2.lower()
  str1_len = len(str1)
  str2_len = len(str2)

  matrix = np.zeros((str1_len+1, str2_len+1, 3))
  co = 0.2
  cr = 0.02
  matrix[0][0] = [0, -co, -co]

  #intial step
  for i in range(1, str1_len + 1):
    matrix[i][0][0] = -np.inf
    matrix[i][0][1] = matrix[i-1][0][1] - cr
    matrix[i][0][2] = -np.inf

  for i in range(1, str2_len + 1):
    matrix[0][i][0] = -np.inf
    matrix[0][i][1] = -np.inf
    matrix[0][i][2] = matrix[0][i-1][2] - cr

  for i in range(1, str1_len + 1):
    for j in range(1, str2_len + 1):
      c = 1 if str1[i-1] == str2[j-1] else -0.2
      matrix[i][j][0] = max((matrix[i-1][j-1][0] + c, matrix[i-1][j-1][1] + c, matrix[i-1][j-1][2] + c))
      matrix[i][j][1] = max((matrix[i-1][j][0] - co, matrix[i-1][j][1] - cr))
      matrix[i][j][2] = max((matrix[i][j-1][0] - co, matrix[i][j-1][2] - cr))

  return max(matrix[str1_len][str2_len]) / max(str1_len, str2_len)


def edit_distance(str1, str2):
    str1_len = len(str1)
    str2_len = len(str2)

    # calculate edit distance
    matrix = np.zeros((str1_len + 1, str2_len + 1))
    matrix[0][0] = 0

    # intial step
    for i in range(1, str1_len + 1):
        matrix[i][0] = matrix[i - 1][0] + 1

    for i in range(1, str2_len + 1):
        matrix[0][i] = matrix[0][i - 1] + 1

    for i in range(1, str1_len + 1):
        for j in range(1, str2_len + 1):
            c = 0 if str1[i - 1] == str2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j - 1] + c, matrix[i - 1][j] + 1, matrix[i][j - 1] + 1)

    return 1 - (matrix[str1_len][str2_len] / max(str1_len, str2_len))

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
    return F[-1][-1] / max(nx, ny)

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


def jaro_Winkler(s1, s2, prefix_weight=0.1):

    jaro_dist = jaro_distance(s1, s2)
 
    prefix = 0

    for i in range(min(len(s1), len(s2))):
        if s1[i] == s2[i] :
            prefix += 1
        else :
            break

    # Maximum of 4 characters are allowed in prefix
    prefix = min(4, prefix)

    # Calculate jaro winkler Similarity
    jaro_dist += prefix_weight * prefix * (1 - jaro_dist)
 
    return jaro_dist




