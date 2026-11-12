class Book:
    """Represents a basic library book."""

    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self._isbn = isbn
        self._available = True

    def get_isbn(self):
        """Return the book ISBN."""
        return self._isbn

    def is_available(self):
        """Check whether the book is available."""
        return self._available

    def set_availability(self, status):
        """Update book availability."""
        if not isinstance(status, bool):
            raise ValueError("Availability must be True or False.")
        self._available = status

    def display_details(self):
        """Display book information."""
        status = "Available" if self._available else "Not Available"

        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN: {self._isbn}")
        print(f"Status: {status}")


if __name__ == "__main__":
    book1 = Book("Python Basics", "John Smith", "ISBN001")
    book1.display_details()
