import numpy as np
from sequencedbase_algorithms import edit_distance

def find_max(matrix):
    if len(matrix) == 0:
        return 0, 0
    ele_max, m_max = matrix[0][0], matrix[0][1]
    for i in range(1, len(matrix)):
        if matrix[i][0] > ele_max:
            ele_max = matrix[i][0]
            m_max = matrix[i][1]

    return ele_max, m_max

#
def generalized_jascard_measure(str1, str2):
    set1 = list(set([ele.lower().strip() for ele in str1.split(',')]))
    set2 = list(set([ele.lower().strip() for ele in str2.split(',')]))
    set1_len = len(set1)
    set2_len = len(set2)
    k = 0.5
    matrix = np.zeros((set1_len, set2_len, 2))

    # initial
    for i in range(set2_len):
        point = edit_distance(set1[0], set2[i])
        if point > k:
            matrix[0][i] = [point, 1]
        else:
            matrix[0][i] = [0, 0]

    for i in range(1, set1_len):
        for j in range(set2_len):
            point = edit_distance(set1[i], set2[j])
            prev = find_max([matrix[i - 1][t] for t in range(set2_len) if t != j])
            if point > k:
                matrix[i][j] = [point + prev[0], prev[1] + 1]
            else:
                matrix[i][j] = [0 + prev[0], prev[1]]

    total_score, M = find_max(matrix[set1_len - 1])

    return total_score / (set1_len + set2_len - M)