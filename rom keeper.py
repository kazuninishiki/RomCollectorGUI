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

def main():
    source_dir = 'D:\\final\\SDCARD\\nds'
    destination_dir = 'D:\\final\\SDCARD\\nds-r'
    groups = scan_and_group(source_dir)
    
    for key, files in groups.items():
        print(f"Group found with similar names: {files}")
        print("Which file(s) would you like to keep? Enter numbers separated by space, or 0 to keep all.")
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")
        choice = input("Your choice: ")
        if choice.strip() == "0":
            continue  # Do nothing, keep all files
        else:
            selected_indexes = [int(index) - 1 for index in choice.split()]
            files_to_keep = [files[i] for i in selected_indexes]
            files_to_move = [f for f in files if f not in files_to_keep]
            move_files(files_to_move, source_dir, destination_dir)
            print(f"Moved {len(files_to_move)} files to {destination_dir}")

if __name__ == "__main__":
    main()
