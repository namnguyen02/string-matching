from tkinter import filedialog, messagebox, ttk
from tkinter import *
from algorithm import *
from evaluate import draw_chart
from candidate import *
from sequencedbase_algorithms import *
from setbase_algorithms import *
from hybrid import *

#initial
df1 = None
df2 = None
df_truth = None
df_mapping = None
algorithm = None
filter_method = None
# Create a new window
root = Tk()
root.title("Data mining assignment")
root.geometry("650x700")

def browse_file(filename_input, file_path):
    filepath = filedialog.askopenfilename()

    # Set the text of the label to the selected file's path
    filename_input.config(text=filepath.split('/')[-1])
    file_path.set(filepath)

def solve(fields):
    if 'venue' in fields:
        fields.remove('venue')
    print(fields)

    global df_mapping
    df_mapping = string_matching_solve(df1, df2, fields, algorithm, filter_method)

def handle_generate(path1, path2, path3):
    if algorithm is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn algorithm")
        return

    if filter_method is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn filter method")
        return

    if path1.get() == "" or path2.get() == "" or path3.get() == "":
        messagebox.showerror("Lỗi", "Không tìm thấy file")
        return

    global df1, df2, df_truth
    df1 = pd.read_csv(path1.get(), encoding="ISO-8859-1").dropna()
    df2 = pd.read_csv(path2.get(), encoding="ISO-8859-1").dropna()
    df_truth = pd.read_csv(path3.get(), encoding="ISO-8859-1").dropna()

    common_fields = set(df1.columns.values).intersection(df2.columns.values)
    common_fields.remove('id')
    field_to_solve = []
    for field in common_fields:
        if df1[field].dtype == 'O' and df2[field].dtype == 'O':
            field_to_solve.append(field)

    solve(field_to_solve)
    df_mapping.to_csv(f'../result/{filename_input1.cget("text")}_{filename_input2.cget("text")}_mapping.csv', index=False)
    draw_chart(root, df_truth, df_mapping)
    messagebox.showinfo("Info", "Done !")


Label(root, text="String matching problem", font="times 15 bold").grid(row=0, column=3)
########################################################################
file_path1 = StringVar()

label_input1 = Label(root, text="Choose The First File")
label_input1.grid(row=1, column=2)

filename_input1 = Label(root, text="")
filename_input1.grid(row=2, column=2)

btn1 = Button(text="Browse", command=lambda: browse_file(filename_input1, file_path1))
btn1.grid(row=1, column=3)

#########################################################################
file_path2 = StringVar()

label_input2 = Label(root, text="Choose The Second File")
label_input2.grid(row=3, column=2)

filename_input2 = Label(root, text="")
filename_input2.grid(row=4, column=2)

btn2 = Button(text="Browse", command=lambda: browse_file(filename_input2, file_path2))
btn2.grid(row=3, column=3)
########################################################################
file_path3 = StringVar()

label_input3 = Label(root, text="Choose The Truth File")
label_input3.grid(row=5, column=2)

filename_input3 = Label(root, text="")
filename_input3.grid(row=6, column=2)

btn3 = Button(text="Browse", command=lambda: browse_file(filename_input3, file_path3))
btn3.grid(row=5, column=3)

###############################      OPTIONS       #########################################
Label(root, text="Select algorithm").grid(row=7, column=1)
algorithm_var = IntVar()
def select_algorithm():
    global algorithm
    algo = algorithm_var.get()
    if algo == 1:
        algorithm = affine_gap_measure
    elif algo == 2:
        algorithm = nw
    elif algo == 3:
        algorithm = jaro_Winkler
    else:
        algorithm = generalized_jascard_measure


affine_gap_measure_radio = Radiobutton(root, text="affine gap", variable=algorithm_var, value=1, command=select_algorithm)
needleman_wunch_measure_radio = Radiobutton(root, text="needleman wunch", variable=algorithm_var, value=2, command=select_algorithm)
jaro_measure_radio = Radiobutton(root, text="jaro", variable=algorithm_var, value=3, command=select_algorithm)
generalized_jascard_measure_radio = Radiobutton(root, text="generalized jascard", variable=algorithm_var, value=4, command=select_algorithm)

affine_gap_measure_radio.grid(row=8, column=1)
needleman_wunch_measure_radio.grid(row=8, column=2)
jaro_measure_radio.grid(row=8, column=3)
generalized_jascard_measure_radio.grid(row=8, column=4)

######

Label(root, text="Select filtering method").grid(row=9, column=1)
filtering_method_var = IntVar()
def select_filtering_method():
    global filter_method
    filter = filtering_method_var.get()
    if filter == 1:
        filter_method = size_filtering

size_filtering_radio = Radiobutton(root, text="size filtering", variable=filtering_method_var, value=1, command=select_filtering_method)

size_filtering_radio.grid(row=10, column=1)

###############################      GENERATE      #########################################
btn_submit = Button(text="Generate mapping file", command=lambda: handle_generate(file_path1, file_path2, file_path3))
btn_submit.grid(row=11, column=3)

########################################################################
Label(root, text="").grid(row=12, column=1)
# Run the window loop
root.mainloop()
