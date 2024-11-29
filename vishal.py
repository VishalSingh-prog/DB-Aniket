#Apna kaam kiya kar bhai
#Aise rote hue muh mat bana
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pyperclip

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("File Management System")
        self.root.geometry("800x600")

        self.current_path = os.path.expanduser("~")

        self.path_var = tk.StringVar()
        self.path_var.set(self.current_path)

        self.command_entry = tk.Entry(self.root, textvariable=self.path_var, font=("Arial", 12), bg="#F0F0F0", fg="#333333", borderwidth=0, highlightthickness=1, highlightbackground="#CCCCCC", highlightcolor="#0066CC")
        self.command_entry.pack(padx=10, pady=(10, 5), fill=tk.X)
        self.command_entry.bind("<Return>", self.navigate_to_path)

        self.file_list = tk.Listbox(self.root, font=("Arial", 12), bg="#FFFFFF", fg="#333333", selectmode=tk.SINGLE, borderwidth=0, highlightthickness=1, highlightbackground="#CCCCCC", highlightcolor="#0066CC")
        self.file_list.pack(padx=10, pady=(5, 10), fill=tk.BOTH, expand=True)
        self.file_list.bind("<Double-Button-1>", self.open_file_or_directory)

        button_frame = tk.Frame(self.root, bg="#F0F0F0")
        button_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        button_style = {"font": ("Arial", 10), "bg": "#0066CC", "fg": "#FFFFFF", "activebackground": "#004C99", "activeforeground": "#FFFFFF", "padx": 10, "pady": 5, "borderwidth": 0, "highlightthickness": 0}

        copy_button = tk.Button(button_frame, text="Copy", command=self.copy_file, **button_style)
        copy_button.pack(side=tk.LEFT, padx=(0, 5))

        paste_button = tk.Button(button_frame, text="Paste", command=self.paste_file, **button_style)
        paste_button.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_file, **button_style)
        delete_button.pack(side=tk.LEFT, padx=5)

        move_button = tk.Button(button_frame, text="Move", command=self.move_file, **button_style)
        move_button.pack(side=tk.LEFT, padx=5)

        rename_button = tk.Button(button_frame, text="Rename", command=self.rename_file, **button_style)
        rename_button.pack(side=tk.LEFT, padx=5)

        new_folder_button = tk.Button(button_frame, text="New Folder", command=self.create_new_folder, **button_style)
        new_folder_button.pack(side=tk.LEFT, padx=5)

        copy_path_button = tk.Button(button_frame, text="Copy Path", command=self.copy_path_to_clipboard, **button_style)
        copy_path_button.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(button_frame, text="Search", command=self.search_files, **button_style)
        search_button.pack(side=tk.LEFT, padx=5)

        self.update_file_list()

    def update_file_list(self):
        self.file_list.delete(0, tk.END)
        files = os.listdir(self.current_path)
        for file in files:
            self.file_list.insert(tk.END, file)

    def open_file_or_directory(self, event):
        selected_item = self.file_list.get(self.file_list.curselection())
        item_path = os.path.join(self.current_path, selected_item)
        if os.path.isfile(item_path):
            os.startfile(item_path)
        elif os.path.isdir(item_path):
            self.current_path = item_path
            self.path_var.set(self.current_path)
            self.update_file_list()

    def copy_file(self):
        selected_file = self.file_list.get(self.file_list.curselection())
        self.clipboard = os.path.join(self.current_path, selected_file)
        print("File copied:", self.clipboard)
        
    def paste_file(self):
        if self.clipboard:
            destination = os.path.join(self.current_path, os.path.basename(self.clipboard))
            if os.path.exists(destination):
                print("File already exists in the destination.")
            else:
                shutil.copy(self.clipboard, destination)
                print("File pasted to:", destination)
                self.update_file_list()
        else:
            print("Clipboard is empty.")    

    def delete_file(self):
        selected_file = self.file_list.get(self.file_list.curselection())
        file_path = os.path.join(self.current_path, selected_file)
        if messagebox.askyesno("Delete", f"Are you sure you want to delete {selected_file}?"):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                self.update_file_list()
                messagebox.showinfo("Delete", f"{selected_file} deleted successfully.")
            except Exception as e:
                messagebox.showerror("Delete Error", str(e))

    def move_file(self):
        selected_file = self.file_list.get(self.file_list.curselection())
        source_path = os.path.join(self.current_path, selected_file)
        destination_path = filedialog.askdirectory()
        if destination_path:
            try:
                shutil.move(source_path, destination_path)
                self.update_file_list()
                messagebox.showinfo("Move", f"{selected_file} moved successfully.")
            except Exception as e:
                messagebox.showerror("Move Error", str(e))

    def rename_file(self):
        selected_file = self.file_list.get(self.file_list.curselection())
        old_path = os.path.join(self.current_path, selected_file)
        new_name = simpledialog.askstring("Rename", "Enter the new name:", initialvalue=selected_file)
        if new_name:
            new_path = os.path.join(self.current_path, new_name)
            try:
                os.rename(old_path, new_path)
                self.update_file_list()
                messagebox.showinfo("Rename", f"{selected_file} renamed successfully.")
            except Exception as e:
                messagebox.showerror("Rename Error", str(e))

    def create_new_folder(self):
        folder_name = simpledialog.askstring("New Folder", "Enter the folder name:")
        if folder_name:
            folder_path = os.path.join(self.current_path, folder_name)
            try:
                os.makedirs(folder_path, exist_ok=True)
                self.update_file_list()
                messagebox.showinfo("New Folder", f"{folder_name} created successfully.")
            except Exception as e:
                messagebox.showerror("New Folder Error", str(e))

    def navigate_to_path(self, event=None):
        path = self.path_var.get()
        if os.path.exists(path):
            self.current_path = path
            self.update_file_list()
        else:
            messagebox.showerror("Invalid Path", "The specified path does not exist.")

    def copy_path_to_clipboard(self):
        selected_file = self.file_list.get(self.file_list.curselection())
        file_path = os.path.join(self.current_path, selected_file)
        try:
            pyperclip.copy(file_path)
            messagebox.showinfo("Copy Path", f"Path copied to clipboard: {file_path}")
        except Exception as e:
            messagebox.showerror("Copy Path Error", str(e))

    def search_files(self):
        search_query = simpledialog.askstring("Search", "Enter the search query:")
        if search_query:
            self.file_list.delete(0, tk.END)
            for root, dirs, files in os.walk(self.current_path):
                for file in files:
                    if search_query.lower() in file.lower():
                        file_path = os.path.join(root, file)
                        self.file_list.insert(tk.END, file_path)


root = tk.Tk()
file_manager = FileManager(root)
root.mainloop()
