from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# ==============================================================================
# 1. ABSTRACTION & ENCAPSULATION
# ==============================================================================
class Book:
    """Encapsulates book details and availability status."""
    def __init__(self, book_id: str, title: str, author: str, isbn: str):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._isbn = isbn
        self._is_available = True

    @property
    def book_id(self) -> str:
        return self._book_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def is_available(self) -> bool:
        return self._is_available

    @is_available.setter
    def is_available(self, status: bool):
        self._is_available = status

    def display_info(self):
        status = "Available" if self._is_available else "Checked Out"
        print(f"[{self._book_id}] '{self._title}' by {self._author} | Status: {status}")


class Transaction:
    """Tracks issuing and returning of books with fine calculation."""
    def __init__(self, transaction_id: str, book_id: str, member_id: str, borrow_days: int = 14):
        self.transaction_id = transaction_id
        self.book_id = book_id
        self.member_id = member_id
        self.issue_date = datetime.now()
        self.due_date = self.issue_date + timedelta(days=borrow_days)
        self.return_date = None
        self.fine_amount = 0.0

    def calculate_fine(self, fine_per_day: float = 2.0) -> float:
        current_time = self.return_date if self.return_date else datetime.now()
        if current_time > self.due_date:
            overdue_days = (current_time - self.due_date).days
            self.fine_amount = overdue_days * fine_per_day
        return self.fine_amount


# ==============================================================================
# 2. INHERITANCE & POLYMORPHISM
# ==============================================================================
class User(ABC):
    """Abstract Base Class representing a general system user."""
    def __init__(self, user_id: str, name: str, email: str):
        self._user_id = user_id
        self._name = name
        self._email = email

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def show_dashboard(self):
        """Abstract method implemented differently by subclasses (Polymorphism)."""
        pass


class Member(User):
    """Derived class for library members who borrow books."""
    def __init__(self, user_id: str, name: str, email: str, max_borrow_limit: int = 3):
        super().__init__(user_id, name, email)
        self.max_borrow_limit = max_borrow_limit
        self.borrowed_books = []  # List of currently borrowed book IDs

    def can_borrow(self) -> bool:
        return len(self.borrowed_books) < self.max_borrow_limit

    def show_dashboard(self):
        print(f"\n--- Member Dashboard: {self._name} ({self._user_id}) ---")
        print(f"Books Currently Borrowed ({len(self.borrowed_books)}/{self.max_borrow_limit}):")
        for b_id in self.borrowed_books:
            print(f" - Book ID: {b_id}")


class Librarian(User):
    """Derived class for administrators managing inventory and users."""
    def __init__(self, user_id: str, name: str, email: str, employee_id: str):
        super().__init__(user_id, name, email)
        self.employee_id = employee_id

    def show_dashboard(self):
        print(f"\n--- Librarian Admin Dashboard: {self._name} ---")
        print(f"Employee ID: {self.employee_id} | Status: Active Manager")


# ==============================================================================
# 3. COMPOSITION & SYSTEM MANAGEMENT
# ==============================================================================
class LibrarySystem:
    """Central Controller managing Books, Users, and Transactions."""
    def __init__(self, library_name: str):
        self.name = library_name
        self._books = {}         # book_id -> Book
        self._users = {}         # user_id -> User
        self._transactions = {}  # transaction_id -> Transaction
        self._tx_counter = 1000

    def add_book(self, book: Book):
        self._books[book.book_id] = book
        print(f"SUCCESS: Book '{book.title}' registered.")

    def register_user(self, user: User):
        self._users[user.user_id] = user
        print(f"SUCCESS: User '{user.name}' registered.")

    def issue_book(self, book_id: str, member_id: str):
        book = self._books.get(book_id)
        user = self._users.get(member_id)

        # Validation checks
        if not book:
            print("ERROR: Book ID not found.")
            return
        if not user or not isinstance(user, Member):
            print("ERROR: Valid Member required to issue a book.")
            return
        if not book.is_available:
            print(f"ERROR: '{book.title}' is currently unavailable.")
            return
        if not user.can_borrow():
            print(f"ERROR: Member '{user.name}' reached maximum borrow limit.")
            return

        # Perform Issue
        book.is_available = False
        user.borrowed_books.append(book_id)
        
        self._tx_counter += 1
        tx_id = f"TX{self._tx_counter}"
        tx = Transaction(tx_id, book_id, member_id)
        self._transactions[tx_id] = tx

        print(f"SUCCESS: Issued '{book.title}' to {user.name}. Transaction ID: {tx_id}")

    def return_book(self, transaction_id: str):
        tx = self._transactions.get(transaction_id)
        if not tx:
            print("ERROR: Invalid Transaction ID.")
            return

        book = self._books.get(tx.book_id)
        member = self._users.get(tx.member_id)

        tx.return_date = datetime.now()
        fine = tx.calculate_fine()
        
        book.is_available = True
        if isinstance(member, Member) and tx.book_id in member.borrowed_books:
            member.borrowed_books.remove(tx.book_id)

        print(f"SUCCESS: '{book.title}' returned by {member.name}.")
        if fine > 0:
            print(f"NOTICE: Outstanding Fine: ${fine:.2f}")
        else:
            print("NOTICE: Returned on time. No fine incurred.")


# ==============================================================================
# DEMONSTRATION DRIVER CODE
# ==============================================================================
if __name__ == "__main__":
    system = LibrarySystem("Central City Library")

    print("=== 1. REGISTERING BOOKS & USERS ===")
    b1 = Book("B001", "Design Patterns", "Erich Gamma", "978-0201633610")
    b2 = Book("B002", "Clean Code", "Robert C. Martin", "978-0132350884")
    system.add_book(b1)
    system.add_book(b2)

    m1 = Member("U101", "Alice Smith", "alice@example.com")
    lib1 = Librarian("L501", "Bob Johnson", "bob@library.org", "EMP-908")
    system.register_user(m1)
    system.register_user(lib1)

    print("\n=== 2. ISSUING BOOKS ===")
    system.issue_book("B001", "U101")
    system.issue_book("B001", "U101")  # Attempting to issue an already checked-out book

    print("\n=== 3. POLYMORPHIC DASHBOARD DISPLAY ===")
    users = [m1, lib1]
    for user in users:
        user.show_dashboard()  # Dynamic dispatch executes specific implementation

    print("\n=== 4. RETURNING BOOKS ===")
    system.return_book("TX1001")