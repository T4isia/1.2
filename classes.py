# Модуль с основными классами книжного магазина

from datetime import datetime
from typing import Dict
from exceptions import *

class Book:
    """Класс для представления книги"""

    def __init__(self, book_id: int, title: str, author: str, genre: str,
                 price: float, quantity: int, year: int):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.quantity = quantity
        self.year = year

        self._validate_data()

    def _validate_data(self):
        """Валидация данных книги"""
        if self.book_id < 0:
            raise ValueError("ID книги не может быть отрицательным")
        if not self.title:
            raise ValueError("Название книги не может быть пустым")
        if not self.author:
            raise ValueError("Автор не может быть пустым")
        if not self.genre:
            raise ValueError("Жанр не может быть пустым")
        if self.price <= 0:
            raise InvalidPriceError("Цена должна быть положительной")
        if self.quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        if self.year < 1000 or self.year > datetime.now().year:
            raise ValueError("Неверный год издания")

    def to_dict(self):
        """Преобразование книги в словарь"""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'price': self.price,
            'quantity': self.quantity,
            'year': self.year
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Создание книги из словаря"""
        return cls(
            book_id=data['book_id'],
            title=data['title'],
            author=data['author'],
            genre=data['genre'],
            price=data['price'],
            quantity=data['quantity'],
            year=data['year']
        )

    def __str__(self):
        return f"ID: {self.book_id} | '{self.title}' - {self.author} ({self.year}) | {self.price} руб. | В наличии: {self.quantity}"

