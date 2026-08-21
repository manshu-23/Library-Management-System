# 📚 Library Management System (OOP in Python)

A robust, object-oriented Library Management System built with Python. This project demonstrates core Object-Oriented Programming (OOP) concepts including **Abstraction**, **Encapsulation**, **Inheritance**, and **Polymorphism** to manage library operations like issuing books, returning books, and tracking overdue fines.

---

## ✨ Features

- **Class-Based Architecture**: Modeled real-world entities like `Book`, `User`, `Member`, `Librarian`, and `Transaction`.
- **User Roles & Authorization**: Separate dashboards and borrowing privileges for Members and Librarians using Inheritance & Polymorphism.
- **Fine Calculation System**: Automated calculation of daily fines for overdue book returns.
- **Transaction History**: Tracks borrowing/return dates and member activity.

---

## 🧩 OOP Concepts Applied

1. **Abstraction**:
   - `User` is defined as an Abstract Base Class (ABC) with abstract methods like `show_dashboard()`, hiding generic user implementation details.
2. **Encapsulation**:
   - Internal attributes (e.g., `_book_id`, `_is_available`, `_borrowed_books`) are kept protected and accessed using Python `@property` getters/setters.
3. **Inheritance**:
   - `Member` and `Librarian` extend the base `User` class to reuse core user logic.
4. **Polymorphism**:
   - Method overriding is used in `show_dashboard()` to render custom interfaces for different user roles dynamically.

---

## 🛠️ Project Structure

```text
Library-Management-System/
│
├── main.py          # Main implementation script containing OOP logic and driver code
└── README.md        # Project documentation
