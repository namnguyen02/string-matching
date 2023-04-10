import pandas as pd

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
