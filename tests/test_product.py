import pytest
from src.product import Product, Category


def test_product_initialization():
    """Тест корректности создания объекта Product"""
    product = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)

    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_category_initialization():
    """Тест корректности создания объекта Category"""
    category = Category("Смартфоны", "Описание категории", [])

    assert category.name == "Смартфоны"
    assert category.description == "Описание категории"
    assert category.products == []


def test_category_counts():
    """Тест корректного подсчета количества категорий и товаров"""
    # Обнуляем счетчики перед тестом
    Category.category_count = 0
    Category.product_count = 0

    product1 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product2 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2])
    category2 = Category("Телевизоры", "Категория телевизоров", [])

    assert Category.category_count == 2  # Две категории
    assert Category.product_count == 2  # Два продукта


def test_add_product():
    """Тест добавления продуктов в категорию"""
    category = Category("Смартфоны", "Категория смартфонов", [])

    product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    category.add_product(product)

    assert len(category.products) == 1
    assert category.products[0] is product
    assert Category.product_count >= 1  # Количество продуктов увеличилось


def test_add_product_invalid():
    """Тест добавления некорректного объекта в категорию"""
    category = Category("Смартфоны", "Категория смартфонов", [])

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
        category.add_product("Не продукт")  # Передаем строку вместо объекта Product
