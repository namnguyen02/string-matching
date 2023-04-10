import numpy as np
import pandas as pd
from candidate import *
from sequencedbase_algorithms import *
from setbase_algorithms import *
from hybrid import *

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
