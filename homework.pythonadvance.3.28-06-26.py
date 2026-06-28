#task1 Создайте экземпляр движка для подключения к SQLite базе данных в памяти.
from decimal import Decimal

import sqlalchemy
from sqlalchemy import Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

engine = sqlalchemy.create_engine("sqlite:///:memory:")

#task2 Создайте сессию для взаимодействия с базой данных, используя созданный движок.
Session = sessionmaker(bind=engine)
session = Session()

#task3 Определите модель продукта Product со следующими типами колонок.
#task4 Определите связанную модель категории Category со следующими типами колонок:
#task5 Установите связь между таблицами Product и Category с помощью колонки category_id.
class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    products: Mapped[list["Product"]] = relationship(back_populates="category")

class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="products")