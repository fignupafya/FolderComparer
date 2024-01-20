import os
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter.simpledialog import askstring


folder1=""
folder2=""
folder1files = []
folder2files = []




def are_files_equal(file1_path, file2_path):
    try:
        with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
            content1 = file1.read()
            content2 = file2.read()

            return content1 == content2
    except Exception as e:
        print(f"ERROR: {e}: {file1_path} {file2_path}")
        return f"ERROR: Could not compare files' contents: {file1_path} {file2_path}"

def add_files_to_list(array,path,basepath):
    for i in os.listdir(path):
        temppath=os.path.join(path,i)
        if os.path.isdir(temppath):
            add_files_to_list(array,temppath,basepath)
        else:
            array.append(temppath.removeprefix(basepath))

def compare_two_folders(folder1,folder2):
    global folder1files
    global folder2files
    folder1files = []
    folder2files = []

    text_area.delete('1.0', tk.END)

    add_files_to_list(folder1files,folder1,folder1)
    add_files_to_list(folder2files,folder2,folder2)

    folder1files=set(folder1files)
    folder2files=set(folder2files)

    folder1exclusive=folder1files-folder2files
    folder2exclusive=folder2files-folder1files
    commonfiles = folder1files-folder1exclusive

    if folder1exclusive:
        print(f"\n$ Files which are only in '{folder2}' :")
        text_area.insert(tk.END, f"\n$ Files which are only in '{folder1}' :\n")
        folder1exclusive=sorted(folder1exclusive)
        for i in folder1exclusive:
            print(i)
            text_area.insert(tk.END, f"{i}\n")

    if folder2exclusive:
        print(f"\n$ Files which are only in '{folder2}' :")
        text_area.insert(tk.END, f"\n$ Files which are only in '{folder2}' :\n")
        folder2exclusive=sorted(folder2exclusive)
        for i in folder2exclusive:
            text_area.insert(tk.END, f"{i}\n")
            print(i)



    not_same=[]
    for i in commonfiles:
        i=i.removeprefix("\\")
        are_equal=are_files_equal(os.path.join(folder1,i),os.path.join(folder2,i))
        if not are_equal:
            not_same.append(i)
        elif type(are_equal)==str:
            not_same.append(are_equal)

    if not_same:
        print("\n$ Following files' contents are not same: ")
        text_area.insert(tk.END, "\n$ Following files' contents are not same: \n")
        not_same.sort()
        for i in not_same:
            if not i.startswith("\\") and not "ERROR: Could not compare" in i :
                i=f"\\{i}"
            print(i)
            text_area.insert(tk.END, f"{i}\n")

    if not folder1exclusive and not folder2exclusive and not not_same:
        print("$ Folders are exactly the same")
        text_area.insert(tk.END, "$ Folders are exactly the same\n")



    print("DONE!")


def get_folder_path(folder):
    global folder1
    global folder2
    folder_path = filedialog.askdirectory()
    if folder=="folder1":
        folder1=folder_path
        text_area.insert(tk.END, f"Folder1: {folder_path}\n")

    else:
        folder2=folder_path
        text_area.insert(tk.END, f"Folder2: {folder_path}\n")

def center_window(width=400, height=300):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def exclude_from_text():
    string = text_ops_textbox.get()
    if string:  # Check if the textbox is not empty
        text = text_area.get("1.0", "end-1c").splitlines()
        text_area.delete('1.0', tk.END)
        for i in text:
            if "Files which are only in" in i or "Following files' contents are not same" in i or string not in i:
                text_area.insert(tk.END, f"{i}\n")

def search_in_text():
    string = text_ops_textbox.get()
    if string:  # Check if the textbox is not empty
        text = text_area.get("1.0", "end-1c").splitlines()
        text_area.delete('1.0', tk.END)
        for i in text:
            if string in i or "Files which are only in" in i or "Following files' contents are not same" in i:
                text_area.insert(tk.END, f"{i}\n")

root = tk.Tk()
center_window(520, 400)
root.title("Folder Selection")

# For Buttons
left_frame = tk.Frame(root)
left_frame.pack(side=tk.TOP, pady=10,padx=10)

select_button1 = tk.Button(left_frame, text="Folder 1", command=lambda: get_folder_path("folder1"))
select_button1.pack(side=tk.LEFT, padx=10)
select_button2 = tk.Button(left_frame, text="Folder 2", command=lambda: get_folder_path("folder2"))
select_button2.pack(side=tk.LEFT, padx=0)
compare_button = tk.Button(left_frame, text="Compare", command=lambda: compare_two_folders(folder1, folder2))
compare_button.pack(side=tk.LEFT,padx=20)

right_frame = tk.Frame(left_frame)
right_frame.pack(side=tk.TOP, padx=10)

text_ops_textbox = tk.Entry(right_frame)
text_ops_textbox.pack(side=tk.LEFT,padx=10)

search_button = tk.Button(right_frame, text="Search", command=search_in_text)
search_button.pack(side=tk.LEFT,padx=(0,5))

filter_button = tk.Button(right_frame, text="Filter Out", command=exclude_from_text)
filter_button.pack(side=tk.LEFT)







# For Text Area
textContainer = tk.Frame(root, borderwidth=1, relief="sunken")
text_area = tk.Text(textContainer, width=24, height=13, wrap="none", borderwidth=0)
textVsb = tk.Scrollbar(textContainer, orient="vertical", command=text_area.yview)
textHsb = tk.Scrollbar(textContainer, orient="horizontal", command=text_area.xview)
text_area.configure(yscrollcommand=textVsb.set, xscrollcommand=textHsb.set)

text_area.grid(row=0, column=0, sticky="nsew")
textVsb.grid(row=0, column=1, sticky="ns")
textHsb.grid(row=1, column=0, sticky="ew")

textContainer.grid_rowconfigure(0, weight=1)
textContainer.grid_columnconfigure(0, weight=1)

textContainer.pack(side="top", fill="both", expand=True)

root.mainloop()