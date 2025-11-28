# Главный модуль для запуска книжного магазина

from manager import BookstoreManager
from bookstore import Bookstore
from classes import Book, Employee, Customer


def create_initial_bookstore():
    """Создание начального магазина с демонстрационными данными"""
    bookstore = Bookstore("Книжный магазин")

    # Добавляем несколько книг
    books_data = [
        ("Мастер и Маргарита", "Михаил Булгаков", "Роман", 450.0, 15, 1967),
        ("Преступление и наказание", "Федор Достоевский", "Роман", 380.0, 12, 1866),
        ("1984", "Джордж Оруэлл", "Антиутопия", 520.0, 8, 1949),
        ("Гарри Поттер и философский камень", "Джоан Роулинг", "Фэнтези", 670.0, 20, 1997),
        ("Война и мир", "Лев Толстой", "Роман", 590.0, 10, 1869)
    ]

    for title, author, genre, price, quantity, year in books_data:
        try:
            book = Book(0, title, author, genre, price, quantity, year)
            bookstore.add_book(book)
        except Exception as e:
            print(f"Ошибка при создании книги: {e}")

    # Добавляем сотрудников
    employees_data = [
        ("Иван Петров", "Менеджер", 50000.0),
        ("Мария Сидорова", "Продавец", 35000.0)
    ]

    for name, position, salary in employees_data:
        try:
            employee = Employee(0, name, position, salary)
            bookstore.add_employee(employee)
        except Exception as e:
            print(f"Ошибка при создании сотрудника: {e}")

    # Добавляем клиентов
    customers_data = [
        ("Анна Смирнова", "anna@mail.com", "+7-123-456-7890"),
        ("Дмитрий Иванов", "dmitry@mail.com", "+7-987-654-3210")
    ]

    for name, email, phone in customers_data:
        try:
            customer = Customer(0, name, email, phone)
            bookstore.add_customer(customer)
        except Exception as e:
            print(f"Ошибка при создании клиента: {e}")

    return bookstore


def main():
    """Главная функция"""
    print("=" * 50)
    print("     СИСТЕМА УПРАВЛЕНИЯ КНИЖНЫМ МАГАЗИНОМ")
    print("=" * 50)

    # Создаем готовый магазин с начальными данными
    bookstore = create_initial_bookstore()
    manager = BookstoreManager(bookstore)

    # Сразу показываем информацию о магазине
    bookstore.display_info()

    # Запускаем интерактивный режим
    manager.interactive_mode()


if __name__ == "__main__":
    main()
