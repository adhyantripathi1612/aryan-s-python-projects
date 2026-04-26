import tkinter as tk

class notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.text_area = tk.Text(self.root)
        self.text_area.pack(fill=tk.BOTH, expand=1)

    def file_new(self):
        self.text_area.delete(1.0, tk.END)
    
    def add_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.file_new)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)
    def save_file(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
        save_file = tk.Menu(self.root, tearoff=0)
        save_file.add_command(label="Save", command=self.save_file)
        menu_bar.add_cascade(label="File", menu=save_file)
        self.text_area.__new__(1.0, tk.END)
    def open_file(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
        self.text_area.open(1.0, tk.OptionMenu)
        open_file = tk.Menu(self.root, tearoff=0)
        open_file.add_command(label="Open", command=self.open_file)
        menu_bar.add_cascade(label="File", menu=open_file)


if __name__ == "__main__":
    root = tk.Tk()
    app = notepad(root)
    app.add_menu()
    root.mainloop()

