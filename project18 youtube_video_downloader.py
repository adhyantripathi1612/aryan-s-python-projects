import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
import yt_dlp

# Set appearance and color theme for a premium look
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class DownloadApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Video Grabber")
        self.geometry("600x350")
        self.resizable(False, False)

        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Header
        self.label = ctk.CTkLabel(self, text="VIDEO GRABBER", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # URL Input
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Paste YouTube URL here...", width=480, height=35)
        self.url_entry.grid(row=1, column=0, padx=20, pady=10)

        # Path Selection Frame
        self.path_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.path_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.path_frame.grid_columnconfigure(0, weight=1)

        # Default path to Downloads folder
        default_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="Save to...", height=35)
        self.path_entry.insert(0, default_path)
        self.path_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.browse_button = ctk.CTkButton(self.path_frame, text="Browse", width=100, height=35,
                                           command=self.browse_file)
        self.browse_button.grid(row=0, column=1)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Status: Ready", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=3, column=0, padx=20, pady=5)

        # Download Button
        self.download_button = ctk.CTkButton(self, text="Start Download", font=ctk.CTkFont(size=15, weight="bold"),
                                             height=40, command=self.start_download)
        self.download_button.grid(row=4, column=0, padx=20, pady=(10, 20))

    def browse_file(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder_selected)

    def start_download(self):
        url = self.url_entry.get().strip()
        save_path = self.path_entry.get().strip()

        if not url:
            messagebox.showwarning("Input Error", "Please enter a YouTube URL.")
            return

        if not os.path.isdir(save_path):
            messagebox.showwarning("Path Error", "Please select a valid folder.")
            return

        # Disable button and update status
        self.download_button.configure(state="disabled")
        self.status_label.configure(text="Status: Downloading... (Check console for logs)", text_color="#FFCC00")

        # Start download in a background thread
        threading.Thread(target=self.download_logic, args=(url, save_path), daemon=True).start()

    def download_logic(self, url, save_path):
        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.after(0, lambda: self.finish_callback(True))
        except Exception as e:
            print(f"Download Error: {e}")
            self.after(0, lambda: self.finish_callback(False))

    def finish_callback(self, success):
        self.download_button.configure(state="normal")
        if success:
            self.status_label.configure(text="Status: Download Complete!", text_color="#00FF00")
            messagebox.showinfo("Success", "Video downloaded successfully!")
            self.url_entry.delete(0, "end")
        else:
            self.status_label.configure(text="Status: Download Failed", text_color="#FF0000")
            messagebox.showerror("Error", "Failed to download the video. Please check the URL.")


if __name__ == "__main__":
    app = DownloadApp()
    app.mainloop()