# Модуль с основным классом книжного магазина и операциями с файлами


import json
import xml.etree.ElementTree as ET
from typing import List, Dict
from classes import Book, Employee, Customer, Sale
from exceptions import *

class Bookstore:
    """Основной класс книжного магазина"""

    def __init__(self, name: str):
        self.name = name
        self.books: Dict[int, Book] = {}  # book_id -> Book
        self.employees: Dict[int, Employee] = {}  # emp_id -> Employee
        self.customers: Dict[int, Customer] = {}  # cust_id -> Customer
        self.sales: Dict[int, Sale] = {}  # sale_id -> Sale
        self._next_book_id = 1
        self._next_emp_id = 1
        self._next_cust_id = 1
        self._next_sale_id = 1

    def _get_next_book_id(self) -> int:
        """Получить следующий доступный ID для книги"""
        # Если есть книги, находим максимальный ID и добавляем 1
        if self.books:
            max_id = max(self.books.keys())
            return max_id + 1
        return 1

    def _get_next_emp_id(self) -> int:
        """Получить следующий доступный ID для сотрудника"""
        if self.employees:
            max_id = max(self.employees.keys())
            return max_id + 1
        return 1

    def _get_next_cust_id(self) -> int:
        """Получить следующий доступный ID для клиента"""
        if self.customers:
            max_id = max(self.customers.keys())
            return max_id + 1
        return 1

    def add_book(self, book: Book) -> None:
        """Добавление книги в магазин"""
        try:
            # Если ID не установлен (0 или отрицательный), назначаем следующий доступный
            if book.book_id <= 0:
                book.book_id = self._get_next_book_id()

            if book.book_id in self.books:
                # Если книга уже есть, увеличиваем количество
                self.books[book.book_id].quantity += book.quantity
                print(f"Количество книги '{book.title}' увеличено. Теперь в наличии: {self.books[book.book_id].quantity}")
            else:
                self.books[book.book_id] = book
                # Обновляем счетчик следующего ID
                if book.book_id >= self._next_book_id:
                    self._next_book_id = book.book_id + 1
                print(f"Книга '{book.title}' успешно добавлена с ID: {book.book_id}")
        except Exception as e:
            raise BookstoreError(f"Ошибка при добавлении книги: {e}")

    def remove_book(self, book_id: int, quantity: int = 1) -> None:
        """Удаление книги из магазина"""
        try:
            if book_id not in self.books:
                raise BookNotFoundError(f"Книга с ID {book_id} не найдена")

            book = self.books[book_id]
            if book.quantity < quantity:
                raise InsufficientQuantityError(
                    f"Недостаточно книг. В наличии: {book.quantity}, запрошено: {quantity}"
                )

            book.quantity -= quantity
            if book.quantity == 0:
                del self.books[book_id]
                print(f"Книга '{book.title}' полностью удалена из магазина")
            else:
                print(f"Удалено {quantity} экз. книги '{book.title}'. Осталось: {book.quantity}")

        except (BookNotFoundError, InsufficientQuantityError):
            raise
        except Exception as e:
            raise BookstoreError(f"Ошибка при удалении книги: {e}")

    def sell_book(self, book_id: int, quantity: int, customer_id: int, employee_id: int) -> Sale:
        """Продажа книги клиенту с возвратом объекта Sale"""
        try:
            if book_id not in self.books:
                raise BookNotFoundError(f"Книга с ID {book_id} не найдена")

            if customer_id not in self.customers:
                raise CustomerNotFoundError(f"Клиент с ID {customer_id} не найден")

            if employee_id not in self.employees:
                raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден")


            book = self.books[book_id]
            if book.quantity < quantity:
                raise InsufficientQuantityError(
                    f"Недостаточно книг для продажи. В наличии: {book.quantity}"
                )

            total_price = book.price * quantity
            book.quantity -= quantity

            # Создаем запись о продаже
            sale = Sale(
                sale_id=self._next_sale_id,
                book_id=book_id,
                customer_id=customer_id,
                employee_id=employee_id,
                quantity=quantity,
                total_price=total_price
            )

            self.sales[self._next_sale_id] = sale
            self._next_sale_id += 1

            customer = self.customers[customer_id]
            employee = self.employees[employee_id]

            print(f"Продажа успешно завершена: {quantity} экз. '{book.title}' "
                  f"клиенту {customer.name} за {total_price} руб. "
                  f"(Продавец: {employee.name})")

            return sale

        except (BookNotFoundError, CustomerNotFoundError, EmployeeNotFoundError, InsufficientQuantityError):
            raise
        except Exception as e:
            raise BookstoreError(f"Ошибка при продаже книги: {e}")

    def add_employee(self, employee: Employee) -> None:
        """Добавление сотрудника"""
        try:
            # Если ID не установлен (0 или отрицательный), назначаем следующий доступный
            if employee.emp_id <= 0:
                employee.emp_id = self._get_next_emp_id()

            if employee.emp_id in self.employees:
                print(f"Сотрудник с ID {employee.emp_id} уже существует")
                return

            self.employees[employee.emp_id] = employee
            # Обновляем счетчик следующего ID
            if employee.emp_id >= self._next_emp_id:
                self._next_emp_id = employee.emp_id + 1
            print(f"Сотрудник {employee.name} успешно добавлен с ID: {employee.emp_id}")

        except Exception as e:
            raise BookstoreError(f"Ошибка при добавлении сотрудника: {e}")

    def add_customer(self, customer: Customer) -> None:
        """Добавление клиента"""
        try:
            # Если ID не установлен (0 или отрицательный), назначаем следующий доступный
            if customer.cust_id <= 0:
                customer.cust_id = self._get_next_cust_id()

            if customer.cust_id in self.customers:
                print(f"Клиент с ID {customer.cust_id} уже существует")
                return

            self.customers[customer.cust_id] = customer
            # Обновляем счетчик следующего ID
            if customer.cust_id >= self._next_cust_id:
                self._next_cust_id = customer.cust_id + 1
            print(f"Клиент {customer.name} успешно добавлен с ID: {customer.cust_id}")

        except Exception as e:
            raise BookstoreError(f"Ошибка при добавлении клиента: {e}")

    def search_books(self, **kwargs) -> List[Book]:
        """Поиск книг по различным критериям"""
        try:
            results = list(self.books.values())

            if 'title' in kwargs and kwargs['title']:
                results = [b for b in results if kwargs['title'].lower() in b.title.lower()]
            if 'author' in kwargs and kwargs['author']:
                results = [b for b in results if kwargs['author'].lower() in b.author.lower()]
            if 'genre' in kwargs and kwargs['genre']:
                results = [b for b in results if kwargs['genre'].lower() in b.genre.lower()]
            if 'max_price' in kwargs and kwargs['max_price']:
                results = [b for b in results if b.price <= kwargs['max_price']]

            return results

        except Exception as e:
            raise BookstoreError(f"Ошибка при поиске книг: {e}")


    def get_sales_by_customer(self, customer_id: int) -> List[Sale]:
        """Получение всех продаж для конкретного клиента"""
        try:
            return [sale for sale in self.sales.values() if sale.customer_id == customer_id]
        except Exception as e:
            raise BookstoreError(f"Ошибка при получении продаж клиента: {e}")

    def get_sales_by_employee(self, employee_id: int) -> List[Sale]:
        """Получение всех продаж для конкретного сотрудника"""
        try:
            return [sale for sale in self.sales.values() if sale.employee_id == employee_id]
        except Exception as e:
            raise BookstoreError(f"Ошибка при получении продаж сотрудника: {e}")

    def get_book_sales(self, book_id: int) -> List[Sale]:
        """Получение всех продаж конкретной книги"""
        try:
            return [sale for sale in self.sales.values() if sale.book_id == book_id]
        except Exception as e:
            raise BookstoreError(f"Ошибка при получении продаж книги: {e}")

    def get_total_revenue(self) -> float:
        """Получение общей выручки магазина"""
        try:
            return sum(sale.total_price for sale in self.sales.values())
        except Exception as e:
            raise BookstoreError(f"Ошибка при расчете выручки: {e}")

    def get_inventory_value(self) -> float:
        """Получение общей стоимости инвентаря"""
        try:
            return sum(book.price * book.quantity for book in self.books.values())
        except Exception as e:
            raise BookstoreError(f"Ошибка при расчете стоимости инвентаря: {e}")

    # Методы для работы с файлами

    def save_to_json(self, filename: str) -> None:
        """Сохранение данных в JSON файл"""
        try:
            data = {
                'name': self.name,
                'next_book_id': self._next_book_id,
                'next_emp_id': self._next_emp_id,
                'next_cust_id': self._next_cust_id,
                'next_sale_id': self._next_sale_id,
                'books': [book.to_dict() for book in self.books.values()],
                'employees': [emp.to_dict() for emp in self.employees.values()],
                'customers': [cust.to_dict() for cust in self.customers.values()],
                'sales': [sale.to_dict() for sale in self.sales.values()]
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"Данные успешно сохранены в {filename}")

        except Exception as e:
            raise FileOperationError(f"Ошибка при сохранении в JSON: {e}")

    def load_from_json(self, filename: str) -> None:
        """Загрузка данных из JSON файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.name = data['name']

            # Очищаем текущие данные
            self.books.clear()
            self.employees.clear()
            self.customers.clear()
            self.sales.clear()

            # Загружаем счетчики ID
            self._next_book_id = data.get('next_book_id', 1)
            self._next_emp_id = data.get('next_emp_id', 1)
            self._next_cust_id = data.get('next_cust_id', 1)
            self._next_sale_id = data.get('next_sale_id', 1)

            # Загружаем книги
            for book_data in data['books']:
                book = Book.from_dict(book_data)
                self.books[book.book_id] = book

            # Загружаем сотрудников
            for emp_data in data['employees']:
                employee = Employee.from_dict(emp_data)
                self.employees[employee.emp_id] = employee

            # Загружаем клиентов
            for cust_data in data['customers']:
                customer = Customer.from_dict(cust_data)
                self.customers[customer.cust_id] = customer

            # Загружаем продажи
            for sale_data in data.get('sales', []):
                sale = Sale.from_dict(sale_data)
                self.sales[sale.sale_id] = sale


            print(f"Данные успешно загружены из {filename}")

        except FileNotFoundError:
            raise FileOperationError(f"Файл {filename} не найден")
        except Exception as e:
            raise FileOperationError(f"Ошибка при загрузке из JSON: {e}")

    def save_to_xml(self, filename: str) -> None:
        """Сохранение данных в XML файл"""
        try:
            root = ET.Element('bookstore')

            # Название магазина
            name_elem = ET.SubElement(root, 'name')
            name_elem.text = self.name

            # Счетчики ID
            counters_elem = ET.SubElement(root, 'id_counters')
            ET.SubElement(counters_elem, 'next_book_id').text = str(self._next_book_id)
            ET.SubElement(counters_elem, 'next_emp_id').text = str(self._next_emp_id)
            ET.SubElement(counters_elem, 'next_cust_id').text = str(self._next_cust_id)
            ET.SubElement(counters_elem, 'next_sale_id').text = str(self._next_sale_id)

            # Книги
            books_elem = ET.SubElement(root, 'books')
            for book in self.books.values():
                book_elem = ET.SubElement(books_elem, 'book')
                for key, value in book.to_dict().items():
                    child = ET.SubElement(book_elem, key)
                    child.text = str(value)

            # Сотрудники
            employees_elem = ET.SubElement(root, 'employees')
            for employee in self.employees.values():
                emp_elem = ET.SubElement(employees_elem, 'employee')
                for key, value in employee.to_dict().items():
                    child = ET.SubElement(emp_elem, key)
                    child.text = str(value)

            # Клиенты
            customers_elem = ET.SubElement(root, 'customers')
            for customer in self.customers.values():
                cust_elem = ET.SubElement(customers_elem, 'customer')
                for key, value in customer.to_dict().items():
                    child = ET.SubElement(cust_elem, key)
                    child.text = str(value)

            # Продажи
            sales_elem = ET.SubElement(root, 'sales')
            for sale in self.sales.values():
                sale_elem = ET.SubElement(sales_elem, 'sale')
                for key, value in sale.to_dict().items():
                    child = ET.SubElement(sale_elem, key)
                    child.text = str(value)

            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)

            print(f"Данные успешно сохранены в {filename}")

        except Exception as e:
            raise FileOperationError(f"Ошибка при сохранении в XML: {e}")

    def load_from_xml(self, filename: str) -> None:
        """Загрузка данных из XML файла"""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            self.name = root.find('name').text

            # Очищаем текущие данные
            self.books.clear()
            self.employees.clear()
            self.customers.clear()
            self.sales.clear()

            # Загружаем счетчики ID
            counters_elem = root.find('id_counters')
            if counters_elem is not None:
                self._next_book_id = int(counters_elem.find('next_book_id').text)
                self._next_emp_id = int(counters_elem.find('next_emp_id').text)
                self._next_cust_id = int(counters_elem.find('next_cust_id').text)
                self._next_sale_id = int(counters_elem.find('next_sale_id').text)


            # Загружаем книги
            books_elem = root.find('books')
            if books_elem is not None:
                for book_elem in books_elem.findall('book'):
                    book_data = {child.tag: child.text for child in book_elem}
                    # Преобразуем типы данных
                    book_data['book_id'] = int(book_data['book_id'])
                    book_data['price'] = float(book_data['price'])
                    book_data['quantity'] = int(book_data['quantity'])
                    book_data['year'] = int(book_data['year'])

                    book = Book.from_dict(book_data)
                    self.books[book.book_id] = book

            # Загружаем сотрудников
            employees_elem = root.find('employees')
            if employees_elem is not None:
                for emp_elem in employees_elem.findall('employee'):
                    emp_data = {child.tag: child.text for child in emp_elem}
                    emp_data['emp_id'] = int(emp_data['emp_id'])
                    emp_data['salary'] = float(emp_data['salary'])

                    employee = Employee.from_dict(emp_data)
                    self.employees[employee.emp_id] = employee

            # Загружаем клиентов
            customers_elem = root.find('customers')
            if customers_elem is not None:
                for cust_elem in customers_elem.findall('customer'):
                    cust_data = {child.tag: child.text for child in cust_elem}
                    cust_data['cust_id'] = int(cust_data['cust_id'])

                    customer = Customer.from_dict(cust_data)
                    self.customers[customer.cust_id] = customer

            # Загружаем продажи
            sales_elem = root.find('sales')
            if sales_elem is not None:
                for sale_elem in sales_elem.findall('sale'):
                    sale_data = {child.tag: child.text for child in sale_elem}
                    sale_data['sale_id'] = int(sale_data['sale_id'])
                    sale_data['book_id'] = int(sale_data['book_id'])
                    sale_data['customer_id'] = int(sale_data['customer_id'])
                    sale_data['employee_id'] = int(sale_data['employee_id'])
                    sale_data['quantity'] = int(sale_data['quantity'])
                    sale_data['total_price'] = float(sale_data['total_price'])

                    sale = Sale.from_dict(sale_data)
                    self.sales[sale.sale_id] = sale

            print(f"Данные успешно загружены из {filename}")

        except FileNotFoundError:
            raise FileOperationError(f"Файл {filename} не найден")
        except Exception as e:
            raise FileOperationError(f"Ошибка при загрузке из XML: {e}")

    def display_info(self) -> None:
        """Отображение информации о магазине"""
        print(f"\n=== {self.name} ===")
        print(f"Книг в ассортименте: {len(self.books)}")
        print(f"Сотрудников: {len(self.employees)}")
        print(f"Клиентов: {len(self.customers)}")
        print(f"Всего продаж: {len(self.sales)}")
        print(f"Общая стоимость инвентаря: {self.get_inventory_value():.2f} руб.")
        print(f"Общая выручка: {self.get_total_revenue():.2f} руб.")

