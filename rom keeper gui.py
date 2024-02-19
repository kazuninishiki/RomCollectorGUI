import tkinter as tk
from tkinter import scrolledtext, Listbox
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

class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('File Organizer')
        self.geometry('1024x768')  # Window size
        self.configure(bg='#333333')  # Dark background color
        
        self.source_dir = 'D:\\final\\SDCARD\\nds'
        self.destination_dir = 'D:\\final\\SDCARD\\nds-r'
        
        self.groups = {}
        self.current_group_key = None
        self.init_ui()

    def init_ui(self):
        self.scan_button = tk.Button(self, text="Scan and Organize", command=self.scan_and_organize, bg='#555555', fg='white')
        self.scan_button.pack(pady=20)
        
        self.selection_frame = tk.Frame(self, bg='#333333')
        self.selection_frame.pack(pady=10, fill='both', expand=True)
        
        # File selection listbox with height set to 10
        self.listbox = Listbox(self.selection_frame, selectmode='multiple', width=100, height=10, bg='#222222', fg='white')
        self.listbox.pack(side='left', fill='both', expand=True)
        
        self.scrollbar = tk.Scrollbar(self.selection_frame, orient='vertical', command=self.listbox.yview, bg='#555555')
        self.scrollbar.pack(side='right', fill='y')
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        # Action buttons placed in their own frame for better positioning
        self.action_frame = tk.Frame(self, bg='#333333')
        self.action_frame.pack(pady=10)
        self.keep_button = tk.Button(self.action_frame, text="Keep Selected", command=self.keep_selected, bg='#555555', fg='white')
        self.keep_button.grid(row=0, column=0, padx=10)
        self.keep_all_button = tk.Button(self.action_frame, text="Keep All", command=self.keep_all, bg='#555555', fg='white')
        self.keep_all_button.grid(row=0, column=1, padx=10)
        
        # Message log with reduced height to 5 lines
        self.log = scrolledtext.ScrolledText(self, state='disabled', height=5, bg='#222222', fg='white')
        self.log.pack(pady=10, fill='both', expand=True)

    def update_log(self, message):
        self.log.config(state='normal')
        self.log.insert(tk.END, message + "\n")
        self.log.config(state='disabled')
        self.log.see(tk.END)

    def scan_and_organize(self):
        self.groups = scan_and_group(self.source_dir)
        self.process_next_group()

    def process_next_group(self):
        if self.groups:
            self.current_group_key, self.current_group_files = self.groups.popitem()
            sorted_group_files = sorted(self.current_group_files)
            self.listbox.delete(0, tk.END)
            for file in sorted_group_files:
                self.listbox.insert(tk.END, file)
        else:
            self.update_log("All groups processed.")

    def keep_selected(self):
        selections = [self.listbox.get(i) for i in self.listbox.curselection()]
        files_to_keep = selections
        files_to_move = [f for f in self.current_group_files if f not in files_to_keep]
        move_files(files_to_move, self.source_dir, self.destination_dir)
        self.update_log(f"Kept: {files_to_keep}\nMoved: {files_to_move}\n")
        self.process_next_group()

    def keep_all(self):
        self.update_log(f"All files in group {self.current_group_key} have been kept.")
        self.process_next_group()

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()
