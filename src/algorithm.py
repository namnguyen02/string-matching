import pandas as pd

from candidate import bound_filtering
from hybrid import generalized_jascard_measure

def string_matching_solve(dataset1, dataset2, fields, algorithm, filter_method):
    mapping_dataset = []
    for index1, row1 in dataset1.iterrows():
        dataset2_after_filter = filter_method(row1, dataset2, fields)
        print(len(dataset2), len(dataset2_after_filter))
        for index2, row2 in dataset2_after_filter.iterrows():
            for field in fields:
                avg_point = algorithm(row1[field], row2[field])
                if(avg_point) < 0.8:
                    break

            if avg_point >= 0.8:
                print(avg_point)
                mapping_dataset.append({
                    "id1": dataset1.loc[index1].id,
                    "id2": dataset2_after_filter.loc[index2].id
                })
                print(f'Mapping df2 index = {index2}')
                dataset2.drop(index=index2, inplace=True)
                break

    return pd.DataFrame(mapping_dataset, columns=["id1", "id2"])


def string_matching_using_bound_filtering(dataset1, dataset2, fields):
    mapping_dataset = []
    threshold = 0.8
    for index1, row1 in dataset1.iterrows():
        for index2, row2 in dataset2.iterrows():
            # bound flitering
            # LB, UB = bound_filtering(row1, row2, fields)
            list = bound_filtering(row1, row2, fields)
            # print('Win')
            # LB >= thres
            if(list[1] < threshold):
                continue
            if list[0] >= threshold:
                mapping_dataset.append({
                    "id1": dataset1.loc[index1].id,
                    "id2": dataset2.loc[index2].id
                })
                print(f'Mapping df2 index = {index2}')
                dataset2.drop(index=index2, inplace=True)
                break
            # LB < <= UB: 
            elif list[0] < threshold <= list[1]:
                for field in fields:
                    avg_point = generalized_jascard_measure(row1[field], row2[field])
                    if(avg_point) < 7:
                        break
                if avg_point >= 0.7:
                    print(avg_point)
                    mapping_dataset.append({
                        "id1": dataset1.loc[index1].id,
                        "id2": dataset2.loc[index2].id
                    })
                    print(f'Mapping df2 index = {index2}')
                    dataset2.drop(index=index2, inplace=True)
                    break

    return pd.DataFrame(mapping_dataset, columns=["id1", "id2"])
