import tkinter as tk
from tkinter import messagebox, filedialog
import os
import shutil
import re

def alphanumeric(s):
    return re.sub(r'[^a-zA-Z0-9]', '', s)

def scan_and_group(directory):
    files = os.listdir(directory)
    grouped_files = {}
    for file in files:
        key = alphanumeric(file[:10])
        if key in grouped_files:
            grouped_files[key].append(file)
        else:
            grouped_files[key] = [file]
    return {k: v for k, v in grouped_files.items() if len(v) > 1}

def move_files(files_to_move, source_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    for file in files_to_move:
        shutil.move(os.path.join(source_dir, file), os.path.join(destination_dir, file))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('File Organizer')
        self.geometry('600x400')
        
        self.source_dir = 'D:\\final\\SDCARD\\nds'
        self.destination_dir = 'D:\\final\\SDCARD\\nds-r'
        
        self.init_ui()

    def init_ui(self):
        self.label = tk.Label(self, text="Select files to keep (others will be moved):")
        self.label.pack(pady=10)
        
        self.listbox = tk.Listbox(self, selectmode='multiple', width=100)
        self.listbox.pack(pady=10)
        
        self.scan_button = tk.Button(self, text="Scan for groups", command=self.scan_groups)
        self.scan_button.pack(pady=5)
        
        self.keep_button = tk.Button(self, text="Keep Selected", command=self.keep_selected)
        self.keep_button.pack(pady=5)
        
        self.keep_all_button = tk.Button(self, text="Keep All", command=self.keep_all)
        self.keep_all_button.pack(pady=5)

    def scan_groups(self):
        self.listbox.delete(0, tk.END)
        self.groups = scan_and_group(self.source_dir)
        for key, files in self.groups.items():
            for file in files:
                self.listbox.insert(tk.END, file)

    def keep_selected(self):
        selections = [self.listbox.get(i) for i in self.listbox.curselection()]
        for key, files in self.groups.items():
            files_to_move = [f for f in files if f not in selections]
            move_files(files_to_move, self.source_dir, self.destination_dir)
        messagebox.showinfo("Operation Complete", "Selected files have been kept, others moved.")
        self.scan_groups()

    def keep_all(self):
        messagebox.showinfo("Operation Complete", "No files have been moved.")
        self.scan_groups()

if __name__ == "__main__":
    app = App()
    app.mainloop()
