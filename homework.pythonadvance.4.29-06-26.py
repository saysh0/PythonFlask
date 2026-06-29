from decimal import Decimal
import sqlalchemy
from sqlalchemy import func
from sqlalchemy import Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

engine = sqlalchemy.create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)
session = Session()

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

Base.metadata.create_all(engine)

#task1 Наполнение данными. Добавьте в базу данных следующие категории и продукты.
category1 = Category(name='Электроника', description="Гаджеты и устройства.")
category2 = Category(name='Книги', description="Печатные книги и электронные книги.")
category3 = Category(name='Одежда', description="Одежда для мужчин и женщин.")

product1 = Product(name='Смартфон', price=Decimal(299.99), in_stock=True, category=category1)
product2 = Product(name='Ноутбук', price=Decimal(499.99), in_stock=True, category=category1)
product3 = Product(name='Научно-фантастический роман', price=Decimal(15.99), in_stock=True, category=category2)
product4 = Product(name='Джинсы', price=Decimal(40.50), in_stock=True, category=category3)
product5 =  Product(name='Футболка', price=Decimal(20), in_stock=True, category=category3)

session.add_all([category1, category2, category3, product1, product2, product3, product4, product5])
session.commit()

#task2 Чтение данных. Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все
#связанные с ней продукты, включая их названия и цены.

categoryis = session.query(Category).all()
for category in categoryis:
    product_names = [p.name for p in category.products]
    product_price = [p.price for p in category.products]
    print(f"id: {category.id}, name: {category.name}, description: {category.description}, product/products: {product_names}, product/products price: {product_price}")

#task3 Обновление данных. Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.
products = session.query(Product).filter(Product.name == 'Смартфон').one()
if products:
    products.price = Decimal(349.99)
    session.commit()

#task4 Агрегация и группировка. Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.
all_prod_in_category = (session.query(Category.name, func.count(Product.id)).join(Product, Category.id == Product.category_id).group_by(Category.name).all())
print('*' * 25)
for category in all_prod_in_category:
    print(category)

#task5 Группировка с фильтрацией. Отфильтруйте и выведите только те категории, в которых более одного продукта.
all_prod_in_category = (session.query(Category.name, func.count(Product.id).label('product_count')).join(Product, Category.id == Product.category_id).group_by(Category.name).having(func.count(Product.id) > 1).all())
print('*' * 25)
for category in all_prod_in_category:
    print(category)