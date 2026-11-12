from functools import wraps
def log_operation(func):
    """Library operation ki execution log karta hai."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n[LOG] Starting: {func.__name__}")

        result = func(*args, **kwargs)

        print(f"[LOG] Completed: {func.__name__}")
        return result

    return wrapper

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


class Library:
    """Library mein books aur lending operations manage karti hai."""

    def __init__(self):
        self.resources = []

    def add_resources(self, *books):
        """*args se aik se zyada books add hoti hain."""
        for book in books:
            if not isinstance(book, Book):
                print("Error: Invalid book object.")
                continue

            if any(
                item.get_isbn() == book.get_isbn()
                for item in self.resources
            ):
                print(f"Book already exists: {book.title}")
                continue

            self.resources.append(book)
            print(f"Book added: {book.title}")

    def display_all(self):
        if not self.resources:
            print("No books available in the library.")
            return

        for book in self.resources:
            book.display_details()
            print("-" * 30)

    def search_resources(self, **kwargs):
        """**kwargs se optional search filters apply hote hain."""
        results = self.resources

        title = kwargs.get("title")
        author = kwargs.get("author")
        resource_type = kwargs.get("resource_type")
        available = kwargs.get("available")

        if title:
            results = [
                book for book in results
                if title.lower() in book.title.lower()
            ]

        if author:
            results = [
                book for book in results
                if author.lower() in book.author.lower()
            ]

        if resource_type:
            results = [
                book for book in results
                if type(book).__name__.lower() == resource_type.lower()
            ]

        if available is not None:
            results = [
                book for book in results
                if book.is_available() == available
            ]

        return results

    def find_by_isbn(self, isbn):
        for book in self.resources:
            if book.get_isbn() == isbn:
                return book
        return None
    
    @log_operation   
    def lend_book(self, isbn):
        book = self.find_by_isbn(isbn)

        if book is None:
            print("Error: Book not found.")
        elif not book.is_available():
            print("Error: Book is already borrowed.")
        else:
            book.set_availability(False)
            print(f"Book borrowed successfully: {book.title}")
    
    @log_operation
    def return_book(self, isbn):
        book = self.find_by_isbn(isbn)

        if book is None:
            print("Error: Book not found.")
        elif book.is_available():
            print("Error: Book was not borrowed.")
        else:
            book.set_availability(True)
            print(f"Book returned successfully: {book.title}")
    
    def resource_generator(self, author=None, resource_type=None):
        """Author ya type ke mutabiq books aik aik karke deta hai."""

        for book in self.resources:
            if author and author.lower() not in book.author.lower():
                continue

            if resource_type:
                if type(book).__name__.lower() != resource_type.lower():
                    continue

            yield book



if __name__ == "__main__":
    library = Library()
    book1 = PrintedBook(
        "Python Basics", "John Smith",
        "ISBN001", 250, "A1"
    )

    book2 = EBook(
        "Learn Python", "David Lee",
        "ISBN002", 5.5, "PDF"
    )

    library.add_resources(book1, book2)
    print("\n--- All Library Books ---")
    library.display_all()

    print("\n--- Search by Author ---")
    results = library.search_resources(author="John")

    for book in results:
        book.display_details()

    print("\n--- Lending Book ---")
    library.lend_book("ISBN001")

    print("\n--- Lending Same Book Again ---")
    library.lend_book("ISBN001")

    print("\n--- Returning Book ---")
    library.return_book("ISBN001")

    print("\n--- Generator: Search by Author ---")

    for book in library.resource_generator(author="John"):
        book.display_details()

    print("\n--- Generator: Search EBooks ---")

    for book in library.resource_generator(resource_type="EBook"):
        book.display_details()

    print("\n--- Decorator Metadata Test ---")
    print("Method Name:", library.lend_book.__name__)