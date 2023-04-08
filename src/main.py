from tkinter import filedialog, messagebox, ttk
from tkinter import *
from algorithm import *

#initial
df1 = None
df2 = None
df_mapping = None
# Create a new window
root = Tk()
root.title("Data mining assignment")
root.geometry("400x200")

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
    df_mapping = string_matching_solve(df1, df2, fields)

def handle_generate_option(path1, path2):
    if path1.get() == "" or path2.get() == "":
        messagebox.showerror("Lỗi", "Không tìm thấy file")
        return

    global df1, df2
    df1 = pd.read_csv(path1.get(), encoding="ISO-8859-1").dropna()
    df2 = pd.read_csv(path2.get(), encoding="ISO-8859-1").dropna()
    common_fields = set(df1.columns.values).intersection(df2.columns.values)
    common_fields.remove('id')
    field_to_solve = []
    for field in common_fields:
        if df1[field].dtype == 'O' and df2[field].dtype == 'O':
            field_to_solve.append(field)

    solve(field_to_solve)
    df_mapping.to_csv(f'../result/{filename_input1.cget("text")}_{filename_input2.cget("text")}_mapping.csv', index=False)
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
btn_submit = Button(text="Generate mapping file", command=lambda: handle_generate_option(file_path1, file_path2))
btn_submit.grid(row=5, column=3)

########################################################################
Label(root, text="").grid(row=6, column=1)
# Run the window loop
root.mainloop()






# y1 = "Gottfried Vossen, Mathias Weske"
# y2 = "Jan van den Bussche"
# print(generalized_jascard_measure(y1, y2))