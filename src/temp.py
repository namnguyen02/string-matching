import numpy as np
from sequencedbase_algorithms import *
def sim_ident(s1, s2):
    return int(s1 == s2)
def needleman_wunsch(string1, string2, gap_cost=1.0, sim_score=sim_ident):

    dist_mat = np.zeros((len(string1) + 1, len(string2) + 1), dtype=float)
    # DP initialization
    for i in range(len(string1) + 1):
        dist_mat[i, 0] = -(i * gap_cost)
    # DP initialization
    for j in range(len(string2) + 1):
        dist_mat[0, j] = -(j * gap_cost)
    # Needleman-Wunsch DP calculation
    for i in range(1, len(string1) + 1):
        for j in range(1, len(string2) + 1):
            match = dist_mat[i - 1, j - 1] + sim_score(string1[i - 1], string2[j - 1])
            delete = dist_mat[i - 1, j] - gap_cost
            insert = dist_mat[i, j - 1] - gap_cost
            dist_mat[i, j] = max(match, delete, insert)
    return dist_mat[dist_mat.shape[0] - 1, dist_mat.shape[1] - 1]

def monge_elkan(bag1, bag2, second_measure_func=jaro_Winkler):
    # input validations
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

print(monge_elkan(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'], ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']))
# print(monge_elkan(['Niall'], ['Nigel']))
# print(monge_elkan(['Niall'], ['Neal']))
# print(monge_elkan(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'], ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'], sim_func=nw))
# print(monge_elkan(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'], ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'], sim_func=affine_gap_measure))