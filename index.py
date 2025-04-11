import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1920x1080")

        self.filename = "books.csv"
        self.books = self.load_books()

        # Title Label
        title = tk.Label(self.root, text="Library Management System", font=("Arial", 20, "bold"), bg="#4CAF50", fg="white")
        title.pack(side=tk.TOP, fill=tk.X)

        # Left Frame - Book Form
        left_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, padx=10, pady=10, bg="#f4f4f4")
        left_frame.place(x=10, y=50, width=500, height=600)

        tk.Label(left_frame, text="Manage Books", font=("Arial", 14, "bold"), bg="#f4f4f4").grid(row=0, columnspan=2, pady=10)

        tk.Label(left_frame, text="Book ID:", bg="#f4f4f4").grid(row=1, column=0, sticky="w")
        self.book_id_entry = tk.Entry(left_frame)
        self.book_id_entry.grid(row=1, column=1)

        tk.Label(left_frame, text="Title:", bg="#f4f4f4").grid(row=2, column=0, sticky="w")
        self.title_entry = tk.Entry(left_frame)
        self.title_entry.grid(row=2, column=1)

        tk.Label(left_frame, text="Author:", bg="#f4f4f4").grid(row=3, column=0, sticky="w")
        self.author_entry = tk.Entry(left_frame)
        self.author_entry.grid(row=3, column=1)

        tk.Label(left_frame, text="Genre:", bg="#f4f4f4").grid(row=4, column=0, sticky="w")
        self.genre_entry = tk.Entry(left_frame)
        self.genre_entry.grid(row=4, column=1)

        tk.Label(left_frame, text="Published Year:", bg="#f4f4f4").grid(row=5, column=0, sticky="w")
        self.year_entry = tk.Entry(left_frame)
        self.year_entry.grid(row=5, column=1)

        tk.Label(left_frame, text="Availability:", bg="#f4f4f4").grid(row=6, column=0, sticky="w")
        self.availability_combo = ttk.Combobox(left_frame, values=["Available", "Not Available"])
        self.availability_combo.grid(row=6, column=1)

        # Buttons
        btn_frame = tk.Frame(left_frame, bg="#f4f4f4")
        btn_frame.grid(row=7, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Add", command=self.add_book, width=10, bg="#4CAF50", fg="white").grid(row=0, column=0)
        tk.Button(btn_frame, text="Delete", command=self.delete_book, width=10, bg="#FF6347", fg="white").grid(row=0, column=1)
        tk.Button(btn_frame, text="Clear", command=self.clear_fields, width=10, bg="#FFD700", fg="black").grid(row=0, column=2)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_books, width=10, bg="#87CEEB", fg="black").grid(row=0, column=3)
        tk.Button(btn_frame, text="Ascending", command=self.merge_sort_books, width=10, bg="#20B2AA", fg="white").grid(row=1, column=0)
        tk.Button(btn_frame, text="Descending", command=self.quick_sort_books, width=10, bg="#20B2AA", fg="white").grid(row=1, column=1)

        # Right Frame - Book List
        right_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, padx=10, pady=10, bg="#f4f4f4")
        right_frame.place(x=520, y=50, width=1350, height=600)

        tk.Label(right_frame, text="Search By:", bg="#f4f4f4").grid(row=0, column=0, padx=5)

        self.search_combo = ttk.Combobox(right_frame, values=["Book ID", "Title", "Author"], state="readonly")
        self.search_combo.grid(row=0, column=1)
        self.search_combo.current(0)

        self.search_entry = tk.Entry(right_frame)
        self.search_entry.grid(row=0, column=2, padx=5)

        tk.Button(right_frame, text="Search", command=self.search_book, bg="#8A2BE2", fg="white").grid(row=0, column=3, padx=5)
        tk.Button(right_frame, text="Show All", command=self.show_all_books, bg="#8A2BE2", fg="white").grid(row=0, column=4, padx=5)

        # Book Table
        self.book_table = ttk.Treeview(right_frame, columns=("Book ID", "Title", "Author", "Genre", "Year", "Availability"), show="headings")
        self.book_table.grid(row=1, column=0, columnspan=5, sticky='nsew')

        for col in ("Book ID", "Title", "Author", "Genre", "Year", "Availability"):
            self.book_table.heading(col, text=col)
            self.book_table.column(col, width=200)

        self.show_all_books()

    def load_books(self):
        """Load books from CSV file and handle missing headers."""
        books = []
        if os.path.exists(self.filename):
            with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header
                for row in reader:
                    books.append(tuple(row))
        return books

    def save_books(self):
        """Save books to CSV file with headers."""
        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Book ID", "Title", "Author", "Genre", "Year", "Availability"])  # Header
            writer.writerows(self.books)

    def add_book(self):
        """Add a new book."""
        book_id = self.book_id_entry.get().strip()
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        availability = self.availability_combo.get().strip()

        if not all([book_id, title, author, genre, year, availability]):
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        if any(book[0] == book_id for book in self.books):
            messagebox.showerror("Duplicate Error", "Book ID already exists!")
            return

        self.books.append((book_id, title, author, genre, year, availability))
        self.save_books()
        self.show_all_books()
        messagebox.showinfo("Success", "Book added successfully!")
        self.clear_fields()

    def delete_book(self):
        """Delete a selected book from the list."""
        selected_item = self.book_table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a book to delete.")
            return

        book_values = self.book_table.item(selected_item, "values")
        self.books = [book for book in self.books if book[0] != book_values[0]]
        self.save_books()
        self.show_all_books()
        messagebox.showinfo("Success", "Book deleted successfully!")

    def clear_fields(self):
        """Clear input fields."""
        self.book_id_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.availability_combo.set("")

    def search_book(self):
        """Search for a book by Book ID, Title, or Author."""
        search_by = self.search_combo.get()
        search_value = self.search_entry.get().strip().lower()

        if not search_value:
            messagebox.showwarning("Input Error", "Please enter a search term.")
            return

        self.book_table.delete(*self.book_table.get_children())

        found = False
        for book in self.books:
            book_str = book[0].lower() if search_by == "Book ID" else book[1].lower() if search_by == "Title" else book[2].lower()
            if search_value in book_str:
                self.book_table.insert("", tk.END, values=book)
                found = True

        if found:
            self.color_search_results()
        else:
            messagebox.showinfo("No Results", "No books found.")

    def show_all_books(self):
        """Show all books with color coding."""
        self.book_table.delete(*self.book_table.get_children())

        for book in self.books:
            if book[5] == "Available":
                self.book_table.insert("", tk.END, values=book, tags="available")
                self.book_table.tag_configure("available", background="#90EE90")  # Light green
            elif book[5] == "Not Available":
                self.book_table.insert("", tk.END, values=book, tags="not_available")
                self.book_table.tag_configure("not_available", background="#FF6347")  # Light red

    def refresh_books(self):
        """Reload books from the CSV and update the table."""
        self.books = self.load_books()
        self.show_all_books()
        messagebox.showinfo("Refreshed", "Books list refreshed successfully.")

    def merge_sort_books(self):
        """Merge Sort books by Title (ascending order)."""
        self.books = self.merge_sort(self.books)
        self.show_all_books()
        messagebox.showinfo("Sort Status", "Books sorted in ascending order by Title (Merge Sort).")

    def merge_sort(self, books):
        """Merge Sort function."""
        if len(books) > 1:
            mid = len(books) // 2
            left_half = books[:mid]
            right_half = books[mid:]

            left_half = self.merge_sort(left_half)
            right_half = self.merge_sort(right_half)

            return self.merge(left_half, right_half)
        else:
            return books

    def merge(self, left, right):
        """Merge two sorted lists."""
        sorted_list = []
        while left and right:
            if left[0][1].lower() < right[0][1].lower():
                sorted_list.append(left.pop(0))
            else:
                sorted_list.append(right.pop(0))
        sorted_list.extend(left)
        sorted_list.extend(right)
        return sorted_list

    def quick_sort_books(self):
        """Quick Sort books by Title (descending order)."""
        self.books = self.quick_sort(self.books)
        self.show_all_books()
        messagebox.showinfo("Sort Status", "Books sorted in descending order by Title (Quick Sort).")

    def quick_sort(self, books):
        """Quick Sort function."""
        if len(books) <= 1:
            return books
        pivot = books[len(books) // 2]
        left = [book for book in books if book[1].lower() > pivot[1].lower()]
        right = [book for book in books if book[1].lower() < pivot[1].lower()]
        return self.quick_sort(left) + [pivot] + self.quick_sort(right)

    def color_search_results(self):
        """Apply color coding to search results."""
        for item in self.book_table.get_children():
            book_values = self.book_table.item(item, "values")
            availability = book_values[5]
            if availability == "Available":
                self.book_table.item(item, tags="available")
                self.book_table.tag_configure("available", background="#90EE90")  # Light green
            elif availability == "Not Available":
                self.book_table.item(item, tags="not_available")
                self.book_table.tag_configure("not_available", background="#FF6347")  # Light red

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
