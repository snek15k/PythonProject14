import pytest
from src.product import Product, Category


def test_product_initialization():
    """Тест корректности создания объекта Product"""
    product = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)

    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_product_invalid_price():
    """Тест создания продукта с некорректной ценой"""
    with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
        Product("Test Product", "Description", 0, 10)


def test_product_invalid_quantity():
    """Тест создания продукта с отрицательным количеством"""
    with pytest.raises(ValueError, match="Количество товара не может быть отрицательным"):
        Product("Test Product", "Description", 100, -5)


def test_price_setter_negative():
    """Тест сеттера цены при попытке установить отрицательное значение"""
    product = Product("Test Product", "Description", 100, 10)
    product.price = -50
    assert product.price == 100  # Цена не должна измениться


def test_price_setter_decrease(monkeypatch):
    """Тест уменьшения цены с подтверждением"""
    product = Product("Test Product", "Description", 100, 10)

    monkeypatch.setattr('builtins.input', lambda _: "y")  # Эмулируем ввод 'y'
    product.price = 50
    assert product.price == 50  # Цена изменилась


def test_price_setter_decrease_cancel(monkeypatch):
    """Тест отмены уменьшения цены"""
    product = Product("Test Product", "Description", 100, 10)

    monkeypatch.setattr('builtins.input', lambda _: "n")  # Эмулируем ввод 'n'
    product.price = 50
    assert product.price == 100  # Цена не изменилась


def test_product_new_product():
    """Тест метода new_product() на создание нового продукта"""
    Product.all_products = []  # Очистка списка перед тестом
    product_data = {
        "name": "New Product",
        "description": "Some description",
        "price": 200,
        "quantity": 3
    }
    new_product = Product.new_product(product_data)

    assert new_product.name == "New Product"
    assert new_product.description == "Some description"
    assert new_product.price == 200
    assert new_product.quantity == 3
    assert len(Product.all_products) == 1


def test_product_new_product_existing():
    """Тест метода new_product() при добавлении существующего товара"""
    Product.all_products = []  # Очистка списка перед тестом
    existing_product = Product("Existing Product", "Description", 150, 5)
    product_data = {
        "name": "Existing Product",
        "description": "Description",
        "price": 180,  # Цена выше, чем у текущего товара
        "quantity": 2
    }

    updated_product = Product.new_product(product_data)

    assert updated_product is existing_product
    assert updated_product.quantity == 7  # Увеличилось на 2
    assert updated_product.price == 180  # Цена повысилась


def test_category_initialization():
    """Тест корректности создания объекта Category"""
    category = Category("Смартфоны", "Описание категории", [])

    assert category.name == "Смартфоны"
    assert category.description == "Описание категории"
    assert category.products == "В категории нет товаров."


def test_category_counts():
    """Тест корректного подсчета количества категорий и товаров"""
    Category.category_count = 0
    Category.product_count = 0

    product1 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product2 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2])
    category2 = Category("Телевизоры", "Категория телевизоров", [])

    assert Category.category_count == 2
    assert Category.product_count == 2


def test_add_product():
    """Тест добавления продуктов в категорию"""
    category = Category("Смартфоны", "Категория смартфонов", [])
    product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)

    category.add_product(product)

    assert "Iphone 15, 210000.0 руб. Остаток: 8 шт." in category.products


def test_add_product_existing():
    """Тест добавления уже существующего товара в категорию"""
    category = Category("Смартфоны", "Категория смартфонов", [])
    product1 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product2 = Product("Iphone 15", "512GB, Gray space", 220000.0, 2)  # Цена выше

    category.add_product(product1)
    category.add_product(product2)

    assert "Iphone 15, 220000.0 руб. Остаток: 10 шт." in category.products


def test_add_product_invalid():
    """Тест добавления некорректного объекта в категорию"""
    category = Category("Смартфоны", "Категория смартфонов", [])

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
        category.add_product("Не продукт")  # Передаем строку вместо объекта Product


def test_product_str():
    """Тест строкового представления продукта"""
    product = Product("MacBook Pro", "M3 Pro, 16GB RAM, 512GB SSD", 250000.0, 3)
    assert str(product) == "MacBook Pro, 250000.0 руб. Остаток: 3 шт."


def test_category_str():
    """Тест строкового представления категории"""
    product1 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product2 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category = Category("Смартфоны", "Категория смартфонов", [product1, product2])

    assert str(category) == "Смартфоны, количество продуктов: 22 шт."


def test_product_addition():
    """Тест сложения двух продуктов"""
    product1 = Product("Apple Watch", "Series 9", 45000.0, 5)
    product2 = Product("AirPods Pro", "2nd Gen", 30000.0, 3)

    total_value = product1 + product2
    expected_value = 45000 * 5 + 30000 * 3  # 225000 + 90000 = 315000

    assert total_value == expected_value


def test_product_addition_invalid():
    """Тест сложения продукта с невалидным объектом"""
    product = Product("MacBook Air", "M2, 16GB RAM, 256GB SSD", 180000.0, 2)

    with pytest.raises(TypeError, match="Складывать можно только объекты класса Product"):
        result = product + "не продукт"
