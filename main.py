class Book:
    """Library ki books ke liye base class."""

    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self._isbn = isbn
        self._available = True

    def get_isbn(self):
        
        return self._isbn

    def is_available(self):
        
        return self._available

    def set_availability(self, status):
        
        if not isinstance(status, bool):
            raise ValueError("Availability must be True or False.")
        self._available = status

    def display_details(self):
        
        status = "Available" if self._available else "Not Available"

        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN: {self._isbn}")
        print(f"Status: {status}")
class PrintedBook(Book):
    """Printed books ki extra details store karti hai."""

    def __init__(self, title, author, isbn, pages, shelf):
        super().__init__(title, author, isbn)
        self.pages = pages
        self.shelf = shelf

    def display_details(self):
        print("\n--- Printed Book ---")
        super().display_details()
        print(f"Pages: {self.pages}")
        print(f"Shelf: {self.shelf}")


class EBook(Book):
    """Digital books ki extra details store karti hai."""

    def __init__(self, title, author, isbn, file_size, file_format):
        super().__init__(title, author, isbn)
        self.file_size = file_size
        self.file_format = file_format

    def display_details(self):
        print("\n--- EBook ---")
        super().display_details()
        print(f"File Size: {self.file_size} MB")
        print(f"Format: {self.file_format}")



if __name__ == "__main__":
    book1 = PrintedBook(
        "Python Basics", "John Smith",
        "ISBN001", 250, "A1"
    )

    book2 = EBook(
        "Learn Python", "David Lee",
        "ISBN002", 5.5, "PDF"
    )

    book1.display_details()
    book2.display_details()
