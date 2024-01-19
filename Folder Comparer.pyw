import os
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext


dekstop_path="C:\\Users\\ahmet\\Desktop\\"


folder1=""
folder2=""
folder1files = []
folder2files = []




def are_files_equal(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        content1 = file1.read()
        content2 = file2.read()

        return content1 == content2


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
    
    add_files_to_list(folder1files,folder1,folder1)
    add_files_to_list(folder2files,folder2,folder2)

    folder1files=set(folder1files)
    folder2files=set(folder2files)

    folder1exclusive=folder1files-folder2files
    folder2exclusive=folder2files-folder1files

    if folder1exclusive:
        print(f"\nFiles which are only in '{os.path.basename(folder1)}' :")
        text_area.insert(tk.END, f"\nFiles which are only in '{os.path.basename(folder1)}' :\n")
        for i in folder1exclusive:
            print(i)
            text_area.insert(tk.END, f"{i}\n")
    if folder2exclusive:
        print(f"\nFiles which are only in '{os.path.basename(folder2)}' :")
        text_area.insert(tk.END, f"\nFiles which are only in '{os.path.basename(folder2)}' :\n")
        for i in folder2exclusive:
            text_area.insert(tk.END, f"{i}\n")
            print(i)


    commonfiles = folder1files-folder1exclusive

    not_same=[]
    for i in commonfiles:
        i=i.removeprefix("\\")
        if not are_files_equal(os.path.join(folder1,i),os.path.join(folder2,i)):
            not_same.append(i)

    if not_same:
        print("\nFollowing files' contents are not same: ")
        text_area.insert(tk.END, "\nFollowing files' contents are not same: \n")
        for i in not_same:
            if not i.startswith("\\"):
                i=f"\\{i}"
            print(i)
            text_area.insert(tk.END, f"{i}\n")

    if not folder1exclusive and not folder2exclusive and not not_same:
        print("Folders are exactly the same")
        text_area.insert(tk.END, "Folders are exactly the same\n")




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



def on_window_resize(event):
    # Adjust the text area size on window resize
    text_area.config(width=36, height=event.height // 15)




root = tk.Tk()
root.title("Folder Selection")
root.geometry("400x300")

# For Buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, pady=10)

select_button1 = tk.Button(button_frame, text="Folder 1", command=lambda: get_folder_path("folder1"))
select_button1.pack(side=tk.LEFT, padx=10)
select_button2 = tk.Button(button_frame, text="Folder 2", command=lambda: get_folder_path("folder2"))
select_button2.pack(side=tk.LEFT, padx=10)
compare_button = tk.Button(button_frame, text="Compare", command=lambda: compare_two_folders(folder1, folder2))
compare_button.pack(side=tk.LEFT, padx=10)

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
