import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, scrolledtext

class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scrapper Pro")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f2f5")

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.6478.183 Safari/537.36'
        }
        self.urls = {
            'books_base': 'https://books.toscrape.com/catalogue/page-{}.html',
            'quotes_base': 'https://quotes.toscrape.com/page/{}/'
        }

        self.book_page = 1
        self.quote_page = 1

        self.setup_ui()

    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg="#f0f2f5", pady=20)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(header_frame, text="🚀 Web Scraper", font=("Helvetica", 18, "bold"), bg="#f0f2f5", fg="#1a73e8")
        title_label.pack()

        control_frame = tk.Frame(self.root, bg="#f0f2f5", pady=10)
        control_frame.pack(fill=tk.X)

        self.btn_books = tk.Button(control_frame, text="📚 Scrape Books", command=self.scraping_books, 
                                  font=("Helvetica", 10), bg="#34a853", fg="white", 
                                  activebackground="#2d8e47", padx=10, pady=5)
        self.btn_books.pack(side=tk.LEFT, padx=20, expand=True)

        self.btn_quotes = tk.Button(control_frame, text="💬 Scrape Quotes", command=self.scraping_quotes, 
                                   font=("Helvetica", 10), bg="#fbbc05", fg="black", 
                                   activebackground="#e5a700", padx=10, pady=5)
        self.btn_quotes.pack(side=tk.LEFT, padx=20, expand=True)

        self.btn_clear = tk.Button(control_frame, text="🗑️ Clear", command=self.clear_results, 
                                  font=("Helvetica", 10), bg="#ea4335", fg="white", 
                                  activebackground="#d13225", padx=15, pady=5)
        self.btn_clear.pack(side=tk.LEFT, padx=20, expand=True)

        self.text_area = scrolledtext.ScrolledText(self.root, font=("Consolas", 10), 
                                                wrap=tk.WORD, bg="white", fg="#202124", 
                                                padx=10, pady=10)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.status = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, 
                              font=("Helvetica", 9), bg="#e8eaed", padx=5)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def log(self, message):
        self.text_area.insert(tk.END, f"{message}\n")
        self.text_area.see(tk.END)

    def clear_results(self):
        self.text_area.delete(1.0, tk.END)
        self.status.config(text="Results cleared.")

    def update_status(self, text):
        self.status.config(text=text)
        self.root.update_idletasks()

    def scraping_books(self):
        self.update_status(f"Fetching books page {self.book_page}...")
        self.log(f"\n--- SCRAPING BOOKS (Page {self.book_page}) ---")
        
        try:
            url = self.urls['books_base'].format(self.book_page)
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 404:
                messagebox.showinfo("End of Results", "No more book pages found. Resetting to Page 1.")
                self.book_page = 1
                return self.scraping_books()
                
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            books = soup.find_all('article', class_='product_pod')
            
            if not books:
                messagebox.showinfo("End of Results", "No books found on this page. Resetting to Page 1.")
                self.book_page = 1
                return self.scraping_books()

            for book in books:
                title = book.h3.a['title']
                price = book.find('p', class_='price_color').text
                self.log(f"📖 {title} - {price}")
            
            self.update_status(f"Done! {len(books)} books found (Page {self.book_page}).")
            self.book_page += 1
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scrape books: {e}")
            self.update_status("Error occurred.")
                
                 
    def scraping_quotes(self):
        self.update_status(f"Fetching quotes page {self.quote_page}...")
        self.log(f"\n--- SCRAPING QUOTES (Page {self.quote_page}) ---")
        
        try:
            url = self.urls['quotes_base'].format(self.quote_page)
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 404:
                messagebox.showinfo("End of Results", "No more quotes found. Resetting to Page 1.")
                self.quote_page = 1
                return self.scraping_quotes()
                
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            quotes = soup.find_all('div', class_='quote')
            
            if not quotes:
                messagebox.showinfo("End of Results", "No quotes found on this page. Resetting to Page 1.")
                self.quote_page = 1
                return self.scraping_quotes()

            for quote in quotes:
                text = quote.find('span', class_='text').text
                author = quote.find('small', class_='author').text
                self.log(f"💬 {text} — {author}")
            
            self.update_status(f"Done! {len(quotes)} quotes found (Page {self.quote_page}).")
            self.quote_page += 1
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scrape quotes: {e}")
            self.update_status("Error occurred.")

if __name__ == '__main__':
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
