import numpy as np
from sequencedbase_algorithms import *

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
        point = jaro_distance(set1[0], set2[i])
        if point > k:
            matrix[0][i] = [point, 1]
        else:
            matrix[0][i] = [0, 0]

    for i in range(1, set1_len):
        for j in range(set2_len):
            point = jaro_distance(set1[i], set2[j])
            prev = find_max([matrix[i - 1][t] for t in range(set2_len) if t != j])
            if point > k:
                matrix[i][j] = [point + prev[0], prev[1] + 1]
            else:
                matrix[i][j] = [0 + prev[0], prev[1]]

    total_score, M = find_max(matrix[set1_len - 1])

    return total_score / (set1_len + set2_len - M)

def monge_elkan(s1, s2, second_measure_func=jaro_Winkler):
    # input validations
    bag1 = str.split(s1, ' ')
    bag2 = str.split(s2, ' ')
    if bag1 is None:
        raise TypeError("First argument cannot be None")
    if bag2 is None:
        raise TypeError("Second argument cannot be None")
    
    if not isinstance(bag1, list):
        if not isinstance(bag1, set):
            raise TypeError('First argument is expected to be a python list or set')
    if not isinstance(bag2, list):
        if not isinstance(bag2, set):
            raise TypeError('Second argument is expected to be a python list or set')
    
    if bag1 == bag2:
        return 1.0

    if len(bag1) == 0 or len(bag2) == 0:
        return 0

    sum_of_maxes = 0
    for t1 in bag1:
        max_sim = float('-inf')
        for t2 in bag2:
            max_sim = max(max_sim, second_measure_func(t1, t2))
        sum_of_maxes += max_sim
    result = float(sum_of_maxes) / float(len(bag1))
    return result