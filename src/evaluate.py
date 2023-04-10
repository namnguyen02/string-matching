from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import pandas as pd

def draw_chart(root, df_truth, df_mapping):
    labels = ['True', 'False']

    # Tạo hình tròn
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(evaluate(df_truth, df_mapping), labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    # Hiển thị hình tròn trên giao diện tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=9, column=1, columnspan=4)


def evaluate(df_truth, df_mapping):
    df_truth.columns = ['id1', 'id2']
    res = [0, df_mapping.shape[0]]
    for index, row in df_mapping.iterrows():
        df_tmp = df_truth[df_truth.id1 == row.id1]
        if df_tmp.shape[0] == 1 and df_tmp.id2.values[0] == row.id2:
            res[0] += 1
            res[1] -= 1
            continue

        df_tmp = df_truth[df_truth.id1 == row.id2]
        if df_tmp.shape[0] == 1 and df_tmp.id2.values[0] == row.id1:
            res[0] += 1
            res[1] -= 1
            continue

    return [res[0] * 100.0 / (res[0] + res[1]), res[1] * 100.0 / (res[0] + res[1])]

# df_truth = pd.read_csv('../data/cleanCleanErDatasets/DBLP-ACM/DBLP-ACM_perfectMapping.csv', encoding="ISO-8859-1")
# df_mapping = pd.read_csv('../result/ACM.csv_DBLP2.csv_mapping.csv', encoding="ISO-8859-1")
# print(evaluate(df_truth, df_mapping))


