import numpy as np
import pandas as pd

def affine_gap_measure(str1, str2):
  str1 = str1.lower()
  str2 = str2.lower()
  str1_len = len(str1)
  str2_len = len(str2)

  matrix = np.zeros((str1_len+1, str2_len+1, 3))
  co = 1
  cr = 0.5
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
      c = 2 if str1[i-1] == str2[j-1] else -1
      matrix[i][j][0] = max((matrix[i-1][j-1][0] + c, matrix[i-1][j-1][1] + c, matrix[i-1][j-1][2] + c))
      matrix[i][j][1] = max((matrix[i-1][j][0] - co, matrix[i-1][j][1] - cr))
      matrix[i][j][2] = max((matrix[i][j-1][0] - co, matrix[i][j-1][2] - cr))

  return max(matrix[str1_len][str2_len]) / max(str1_len, str2_len)


def score(str1, str2):
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
        point = score(set1[0], set2[i])
        if point > k:
            matrix[0][i] = [point, 1]
        else:
            matrix[0][i] = [0, 0]

    for i in range(1, set1_len):
        for j in range(set2_len):
            point = score(set1[i], set2[j])
            prev = find_max([matrix[i - 1][t] for t in range(set2_len) if t != j])
            if point > k:
                matrix[i][j] = [point + prev[0], prev[1] + 1]
            else:
                matrix[i][j] = [0 + prev[0], prev[1]]

    total_score, M = find_max(matrix[set1_len - 1])

    return total_score / (set1_len + set2_len - M)

# Dùng để tìm ra các candidate
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


def string_matching_solve(dataset1, dataset2, fields):
    mapping_dataset = []
    for index1, row1 in dataset1.iterrows():
        dataset2_after_filter = size_filtering(row1, dataset2, fields)
        print(len(dataset2), len(dataset2_after_filter))
        for index2, row2 in dataset2_after_filter.iterrows():
            for field in fields:
                avg_point = generalized_jascard_measure(row1[field], row2[field])
                if(avg_point) < 7:
                    break

            if avg_point >= 0.7:
                print(avg_point)
                mapping_dataset.append({
                    "id1": dataset1.loc[index1].id,
                    "id2": dataset2_after_filter.loc[index2].id
                })
                print(f'Mapping df2 index = {index2}')
                dataset2.drop(index=index2, inplace=True)
                break

    return pd.DataFrame(mapping_dataset, columns=["id1", "id2"])
