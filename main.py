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

def get_required_input(message):
    """Khali input accept nahi karta."""
    while True:
        value = input(message).strip()

        if value:
            return value

        print("Error: Input cannot be empty.")


def get_positive_number(message, number_type=int):
    while True:
        try:
            value = number_type(input(message))

            if value <= 0:
                print("Error: Enter a positive number.")
                continue

            return value

        except ValueError:
            print("Error: Please enter a valid number.")


def add_printed_book(library):
    print("\n--- Add Printed Book ---")

    title = get_required_input("Enter title: ")
    author = get_required_input("Enter author: ")
    isbn = get_required_input("Enter ISBN: ")
    pages = get_positive_number("Enter pages: ")
    shelf = get_required_input("Enter shelf number: ")

    book = PrintedBook(title, author, isbn, pages, shelf)
    library.add_resources(book)


def add_ebook(library):
    print("\n--- Add EBook ---")

    title = get_required_input("Enter title: ")
    author = get_required_input("Enter author: ")
    isbn = get_required_input("Enter ISBN: ")
    file_size = get_positive_number(
        "Enter file size (MB): ", float
    )
    file_format = get_required_input("Enter format: ")

    book = EBook(
        title, author, isbn, file_size, file_format
    )

    library.add_resources(book)


def search_books(library):
    print("\n--- Search Resources ---")

    print("1. Search by Title")
    print("2. Search by Author")
    print("3. Search by Resource Type")
    print("4. Search by Availability")

    choice = input("Enter search option: ").strip()

    if choice == "1":
        title = get_required_input("Enter title: ")
        results = library.search_resources(title=title)

    elif choice == "2":
        author = get_required_input("Enter author: ")
        results = library.search_resources(author=author)

    elif choice == "3":
        print("1. PrintedBook")
        print("2. EBook")

        book_type = input("Select type: ").strip()

        if book_type == "1":
            results = library.search_resources(
                resource_type="PrintedBook"
            )
        elif book_type == "2":
            results = library.search_resources(
                resource_type="EBook"
            )
        else:
            print("Invalid resource type.")
            return

    elif choice == "4":
        print("1. Available")
        print("2. Borrowed")

        status = input("Select status: ").strip()

        if status == "1":
            results = library.search_resources(available=True)
        elif status == "2":
            results = library.search_resources(available=False)
        else:
            print("Invalid status.")
            return

    else:
        print("Invalid search option.")
        return

    if not results:
        print("No matching resources found.")
        return

    for book in results:
        book.display_details()
        print("-" * 30)


def filter_with_generator(library):
    print("\n--- Generator Filter ---")
    print("1. Filter by Author")
    print("2. Filter by Resource Type")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        author = get_required_input("Enter author: ")
        generator = library.resource_generator(author=author)

    elif choice == "2":
        print("1. PrintedBook")
        print("2. EBook")

        book_type = input("Select type: ").strip()

        if book_type == "1":
            resource_type = "PrintedBook"
        elif book_type == "2":
            resource_type = "EBook"
        else:
            print("Invalid resource type.")
            return

        generator = library.resource_generator(
            resource_type=resource_type
        )

    else:
        print("Invalid option.")
        return

    found = False

    for book in generator:
        book.display_details()
        print("-" * 30)
        found = True

    if not found:
        print("No matching resources found.")




def main():
    """User ke liye interactive library menu."""
    library = Library()

    while True:
        print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
        print("1. Add Printed Book")
        print("2. Add EBook")
        print("3. Display All Books")
        print("4. Search Books")
        print("5. Lend Book")
        print("6. Return Book")
        print("7. Generator - Filter Resources")
        print("8. Exit")
        print("=" * 47)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_printed_book(library)

        elif choice == "2":
            add_ebook(library)

        elif choice == "3":
            print("\n--- All Library Resources ---")
            library.display_all()

        elif choice == "4":
            search_books(library)

        elif choice == "5":
            isbn = get_required_input("Enter ISBN to lend: ")
            library.lend_book(isbn)

        elif choice == "6":
            isbn = get_required_input("Enter ISBN to return: ")
            library.return_book(isbn)

        elif choice == "7":
            filter_with_generator(library)

        elif choice == "8":
            print("\nThank you for using the Library System!")
            break

        else:
            print("Invalid choice! Please select 1 to 8.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
