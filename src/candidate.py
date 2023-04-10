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