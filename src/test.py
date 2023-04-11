from tkinter import filedialog, messagebox, ttk
from tkinter import *
from sequencedbase_algorithms import *
from setbase_algorithms import *
from hybrid import *


algorithm = None
# Create a new window
root = Tk()
root.title("String matching algorithm test")
root.geometry("300x300")

def calculate(str1, str2):
    if algorithm is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn algorithm")
        return

    print(str1)
    print(str2)
    score.config(text=f"Score:  {round(algorithm(str1, str2), 2)}")

str1_var = StringVar()
str2_var = StringVar()

Label(root, text="String matching test", font="times 15 bold").grid(row=0, column=1)

str1_label = Label(root, text="String 1:")
str1_entry = Entry(root, textvariable=str1_var)

str2_label = Label(root, text="String 2:")
str2_entry = Entry(root, textvariable=str2_var)

str1_label.grid(row=1, column=0, sticky="w")
str1_entry.grid(row=1, column=1)

str2_label.grid(row=2, column=0, sticky="w")
str2_entry.grid(row=2, column=1)

###############################      OPTIONS       #########################################
Label(root, text="Select algorithm").grid(row=3, column=0)
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
    elif algo == 4:
        algorithm = generalized_jascard_measure
    else:
        algorithm = monge_elkan

affine_gap_measure_radio = Radiobutton(root, text="affine gap", variable=algorithm_var, value=1, command=select_algorithm)
needleman_wunch_measure_radio = Radiobutton(root, text="needleman wunch", variable=algorithm_var, value=2, command=select_algorithm)
jaro_measure_radio = Radiobutton(root, text="jaro", variable=algorithm_var, value=3, command=select_algorithm)
generalized_jascard_measure_radio = Radiobutton(root, text="generalized jascard", variable=algorithm_var, value=4, command=select_algorithm)
monge_elkan_radio = Radiobutton(root, text="monge elkan", variable=algorithm_var, value=5, command=select_algorithm)

affine_gap_measure_radio.grid(row=4, column=1)
needleman_wunch_measure_radio.grid(row=5, column=1)
jaro_measure_radio.grid(row=6, column=1)
generalized_jascard_measure_radio.grid(row=7, column=1)
monge_elkan_radio.grid(row=8, column=1)

###############################      CALCULATE      #########################################
btn_submit = Button(text="Calculate similarity score", command=lambda: calculate(str1_var.get(), str2_var.get()))
btn_submit.grid(row=9, column=1)

##########        SCORE          #########
score = Label(root, text="")
score.grid(row=10, column=0)

# Run the window loop
root.mainloop()