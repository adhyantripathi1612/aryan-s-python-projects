import os 
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
import logging

logging.basicConfig(
    filename='pdf_merger_error.log', 
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

BG_COLOR = "#2b2d31"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#5865f2"
SUCCESS_COLOR = "#43b581"
ERROR_COLOR = "#f04747"
ENTRY_BG = "#383a40"

class PDFMergerApp:
    def __init__(self, mw):
        self.mw = mw
        self.mw.title("PDF Merger by ADHYAN TRIPATHI")
        self.mw.geometry("800x750")
        self.mw.configure(bg='black')
        self.mw.resizable(True, True)

        self.pdf_list = []

        self.setup_ui()

    def setup_ui(self):
        self.back = tk.Frame(master=self.mw, bg='black')
        self.back.pack(padx=20, pady=20, fill="both", expand=True)

        header_font = ("Segoe UI", 24, "bold")
        tk.Label(self.back, text="PDF Merger By AdHYAN TRIPATHI", font=header_font, bg='black', fg=FG_COLOR).pack(pady=(0, 20))

        self.main_container = tk.Frame(self.back, bg='black')
        self.main_container.pack(fill="both", expand=True)

        self.list_frame = tk.Frame(self.main_container, bg='black')
        self.list_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        tk.Label(self.list_frame, text="Files to Merge:", bg='black', fg=FG_COLOR, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        scroll_y = tk.Scrollbar(self.list_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.files_listbox = tk.Listbox(
            self.list_frame, 
            bg=ENTRY_BG, 
            fg=FG_COLOR, 
            selectbackground=ACCENT_COLOR, 
            borderwidth=0, 
            height=15,
            font=("Segoe UI", 10),
            yscrollcommand=scroll_y.set
        )
        self.files_listbox.pack(fill="both", expand=True, pady=5)
        scroll_y.config(command=self.files_listbox.yview)
        
        self.files_listbox.bind('<<ListboxSelect>>', self.on_select)

        self.btn_frame = tk.Frame(self.main_container, bg='black')
        self.btn_frame.pack(side="right", fill="y", pady=25)

        btn_style = {
            "bg": ACCENT_COLOR, 
            "fg": FG_COLOR, 
            "borderwidth": 0, 
            "padx": 15, 
            "pady": 8, 
            "font": ("Segoe UI", 9, "bold"),
            "cursor": "hand2"
        }
        
        tk.Button(self.btn_frame, text="Add Files", command=self.add_files, **btn_style).pack(fill="x", pady=5)
        tk.Button(self.btn_frame, text="Remove Selected", command=self.remove_file, **btn_style).pack(fill="x", pady=5)
        tk.Button(self.btn_frame, text="Move Up", command=self.move_up, **btn_style).pack(fill="x", pady=5)
        tk.Button(self.btn_frame, text="Move Down", command=self.move_down, **btn_style).pack(fill="x", pady=5)
        tk.Button(self.btn_frame, text="Clear All", command=self.clear_all, **btn_style).pack(fill="x", pady=5)

        self.options_frame = tk.LabelFrame(self.back, text="Selected File Settings", bg='black', fg=ACCENT_COLOR, font=("Segoe UI", 10, "bold"), padx=15, pady=15)
        self.options_frame.pack(fill="x", pady=15)

        tk.Label(self.options_frame, text="Page Selection (e.g., 1-5, 7, 10-end):", bg='black', fg=FG_COLOR).grid(row=0, column=0, sticky="w")
        self.pages_entry = tk.Entry(self.options_frame, bg=ENTRY_BG, fg=FG_COLOR, borderwidth=0, insertbackground="white", font=("Segoe UI", 10))
        self.pages_entry.grid(row=0, column=1, padx=15, sticky="ew", ipady=3)
        self.pages_entry.bind("<KeyRelease>", self.update_pages)
        self.options_frame.columnconfigure(1, weight=1)

        self.bottom_frame = tk.Frame(self.back, bg='black')
        self.bottom_frame.pack(fill="x", pady=10)

        self.optimize_var = tk.IntVar()
        tk.Checkbutton(
            self.bottom_frame, 
            text="Compress Metadata and Content (Reduced File Size)", 
            variable=self.optimize_var, 
            bg='black', 
            fg=FG_COLOR, 
            selectcolor='black', 
            activebackground='black', 
            activeforeground=FG_COLOR,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        tk.Label(self.bottom_frame, text="Output Filename (Optional - browser will open if empty):", bg='black', fg=FG_COLOR, font=("Segoe UI", 9)).pack(anchor="w", pady=(15, 0))
        self.output_entry = tk.Entry(self.bottom_frame, bg=ENTRY_BG, fg=FG_COLOR, borderwidth=0, insertbackground="white", font=("Segoe UI", 10))
        self.output_entry.pack(fill="x", pady=5, ipady=8)

        self.merge_btn = tk.Button(
            self.back, 
            text="MERGE PDFS NOW", 
            command=self.merge_pdfs, 
            bg=SUCCESS_COLOR, 
            fg="white", 
            font=("Segoe UI", 14, "bold"),
            borderwidth=0,
            height=2,
            cursor="hand2",
            activebackground="#3e9c6f"
        )
        self.merge_btn.pack(fill="x", pady=20)


    def add_files(self):
        files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])
        if files:
            for f in files:
                self.pdf_list.append({'path': f, 'pages': ''})
                self.files_listbox.insert(tk.END, os.path.basename(f))
            self.files_listbox.selection_clear(0, tk.END)
            self.files_listbox.selection_set(tk.END)
            self.on_select(None)

    def remove_file(self):
        selected = self.files_listbox.curselection()
        if not selected: return
        idx = selected[0]
        self.pdf_list.pop(idx)
        self.files_listbox.delete(idx)
        self.pages_entry.delete(0, tk.END)

    def move_up(self):
        selected = self.files_listbox.curselection()
        if not selected or selected[0] == 0: return
        idx = selected[0]
        self.pdf_list[idx], self.pdf_list[idx-1] = self.pdf_list[idx-1], self.pdf_list[idx]
        self.refresh_listbox(idx-1)

    def move_down(self):
        selected = self.files_listbox.curselection()
        if not selected or selected[0] == len(self.pdf_list) - 1: return
        idx = selected[0]
        self.pdf_list[idx], self.pdf_list[idx+1] = self.pdf_list[idx+1], self.pdf_list[idx]
        self.refresh_listbox(idx+1)

    def refresh_listbox(self, select_idx=None):
        self.files_listbox.delete(0, tk.END)
        for item in self.pdf_list:
            self.files_listbox.insert(tk.END, os.path.basename(item['path']))
        if select_idx is not None:
            self.files_listbox.selection_set(select_idx)
            self.on_select(None)

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear entire list?"):
            self.pdf_list = []
            self.files_listbox.delete(0, tk.END)
            self.pages_entry.delete(0, tk.END)

    def on_select(self, event):
        selected = self.files_listbox.curselection()
        self.pages_entry.delete(0, tk.END)
        if not selected: return
        idx = selected[0]
        self.pages_entry.insert(0, self.pdf_list[idx]['pages'])

    def update_pages(self, event):
        selected = self.files_listbox.curselection()
        if not selected: return
        idx = selected[0]
        self.pdf_list[idx]['pages'] = self.pages_entry.get()

    def parse_pages(self, page_str, max_pages):
        if not page_str.strip():
            return list(range(max_pages))
        
        pages = []
        parts = page_str.split(',')
        for p in parts:
            p = p.strip().lower()
            if not p: continue
            if '-' in p:
                start, end = p.split('-')
                start_val = int(start) - 1 if start else 0
                if end == 'end' or not end:
                    end_val = max_pages
                else:
                    end_val = int(end)
                pages.extend(range(start_val, end_val))
            else:
                pages.append(int(p) - 1)
        return [p for p in pages if 0 <= p < max_pages]

    def merge_pdfs(self):
        if not self.pdf_list:
            messagebox.showerror("Error", "Please add at least one PDF file.")
            return
        
        out_name = self.output_entry.get().strip()
        if not out_name:
            out_name = filedialog.asksaveasfilename(
                title="Save Merged PDF",
                defaultextension=".pdf", 
                filetypes=[("PDF files", "*.pdf")]
            )
            if not out_name: return
        
        if not out_name.lower().endswith('.pdf'): out_name += '.pdf'

        try:
            writer = PdfWriter()
            for item in self.pdf_list:
                reader = PdfReader(item['path'])
                max_p = len(reader.pages)
                try:
                    selected_pages = self.parse_pages(item['pages'], max_p)
                    for p_num in selected_pages:
                        writer.add_page(reader.pages[p_num])
                except Exception as pe:
                    logging.error(f"Page parsing error for {item['path']}: {pe}")
                    messagebox.showwarning("Warning", f"Could not parse pages for {os.path.basename(item['path'])}. Including all pages.")
                    for page in reader.pages:
                        writer.add_page(page)

            if self.optimize_var.get():
                for page in writer.pages:
                    page.compress_content_streams()

            with open(out_name, "wb") as f:
                writer.write(f)
            
            messagebox.showinfo("Success", f"Merged PDF saved as:\n{os.path.basename(out_name)}")
        except Exception as e:
            logging.error(f"Merge error: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to merge PDFs. Details logged to pdf_merger_error.log\n\nError: {e}")

def main():
    mw = tk.Tk()
    app = PDFMergerApp(mw)
    mw.mainloop()

if __name__ == '__main__':
    main()
