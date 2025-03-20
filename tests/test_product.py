import pytest
from src.product import Product, Category, Smartphone, LawnGrass


def test_product_initialization():
    """Тест корректности создания объекта Product"""
    product = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )

    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_product_invalid_price():
    """Тест создания продукта с некорректной ценой"""
    with pytest.raises(
        ValueError, match="Цена не должна быть нулевая или отрицательная"
    ):
        Product("Test Product", "Description", 0, 10)


def test_product_invalid_quantity():
    """Тест создания продукта с нулевым или отрицательным количеством"""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Test Product", "Description", 100, 0)

    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Test Product", "Description", 100, -5)


def test_price_setter_negative():
    """Тест сеттера цены при попытке установить отрицательное значение"""
    product = Product("Test Product", "Description", 100, 10)
    product.price = -50
    assert product.price == 100  # Цена не должна измениться


def test_price_setter_decrease(monkeypatch):
    """Тест уменьшения цены с подтверждением"""
    product = Product("Test Product", "Description", 100, 10)

    monkeypatch.setattr("builtins.input", lambda _: "y")  # Эмулируем ввод 'y'
    product.price = 50
    assert product.price == 50  # Цена изменилась


def test_price_setter_decrease_cancel(monkeypatch):
    """Тест отмены уменьшения цены"""
    product = Product("Test Product", "Description", 100, 10)

    monkeypatch.setattr("builtins.input", lambda _: "n")  # Эмулируем ввод 'n'
    product.price = 50
    assert product.price == 100  # Цена не изменилась


def test_product_new_product():
    """Тест метода new_product() на создание нового продукта"""
    Product.all_products = []  # Очистка списка перед тестом
    product_data = {
        "name": "New Product",
        "description": "Some description",
        "price": 200,
        "quantity": 3,
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

    # Создаем существующий продукт и добавляем его в список
    existing_product = Product("Existing Product", "Description", 150, 5)
    Product.all_products.append(existing_product)

    # Продукт, который будет добавлен
    product_data = {
        "name": "Existing Product",
        "description": "Description",
        "price": 180,  # Цена выше, чем у текущего товара
        "quantity": 2,
    }

    # Вызываем метод new_product
    updated_product = Product.new_product(product_data)

    # Проверяем, что обновленный товар — это тот же объект, что и existing_product
    assert updated_product is existing_product
    # Проверяем, что цена и количество обновились
    assert updated_product.price == 180
    assert updated_product.quantity == 7  # Суммируем старое количество с новым


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

    with pytest.raises(
        TypeError, match="Можно добавлять только объекты класса Product"
    ):
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

    with pytest.raises(
        TypeError, match="Складывать можно только объекты класса Product"
    ):
        result = product + "не продукт"


def test_smartphone_creation():
    phone = Smartphone(
        "iPhone", "Apple smartphone", 100000, 5, "High", "13 Pro", 256, "Blue"
    )
    assert phone.name == "iPhone"
    assert phone.model == "13 Pro"
    assert phone.memory == 256
    assert phone.color == "Blue"
    assert phone.price == 100000
    assert phone.quantity == 5


def test_lawngrass_creation():
    grass = LawnGrass(
        "Green Lawn", "Premium quality grass", 500, 20, "USA", 14, "Green"
    )
    assert grass.name == "Green Lawn"
    assert grass.country == "USA"
    assert grass.germination_period == 14
    assert grass.color == "Green"
    assert grass.price == 500
    assert grass.quantity == 20


def test_category_add_product():
    phone = Smartphone(
        "Samsung Galaxy", "Android smartphone", 80000, 3, "High", "S22", 128, "Black"
    )
    grass = LawnGrass(
        "Luxury Lawn", "High-quality grass", 700, 15, "Canada", 10, "Light Green"
    )
    category = Category("Tech & Home", "Various products", [])

    category.add_product(phone)
    category.add_product(grass)

    assert "Samsung Galaxy" in category.products
    assert "Luxury Lawn" in category.products
    assert Category.product_count == 8


def test_init_print_mixin(capsys):
    """Тест миксина InitPrintMixin: проверка вывода информации о создании объекта"""
    product = Product("Test Product", "Test Description", 500, 10)
    captured = capsys.readouterr()
    assert (
        "Создан объект класса Product с параметрами: ('Test Product', 'Test Description', 500, 10), {}"
        in captured.out
    )


def test_smartphone_init_print_mixin(capsys):
    """Тест миксина InitPrintMixin на объекте Smartphone"""
    phone = Smartphone(
        "iPhone", "Apple smartphone", 100000, 5, "High", "13 Pro", 256, "Blue"
    )
    captured = capsys.readouterr()
    assert "Создан объект класса Smartphone с параметрами:" in captured.out


def test_lawn_grass_init_print_mixin(capsys):
    """Тест миксина InitPrintMixin на объекте LawnGrass"""
    grass = LawnGrass(
        "Luxury Lawn", "High-quality grass", 700, 15, "Canada", 10, "Light Green"
    )
    captured = capsys.readouterr()
    assert "Создан объект класса LawnGrass с параметрами:" in captured.out


def test_product_creation_with_mixin(capsys):
    """Тест корректности создания объекта Product с вызовом InitPrintMixin"""
    product = Product("MacBook", "Apple Laptop", 150000, 2)
    captured = capsys.readouterr()
    assert "Создан объект класса Product с параметрами:" in captured.out


def test_product_price_cannot_be_zero():
    """Тест, что цена не может быть нулевой"""
    with pytest.raises(
        ValueError, match="Цена не должна быть нулевая или отрицательная"
    ):
        Product("Test Product", "Description", 0, 10)


def test_product_price_cannot_be_negative():
    """Тест, что цена не может быть отрицательной"""
    with pytest.raises(
        ValueError, match="Цена не должна быть нулевая или отрицательная"
    ):
        Product("Test Product", "Description", -100, 10)


def test_product_price_setter_negative():
    """Тест сеттера цены при попытке установить отрицательное значение"""
    product = Product("Test Product", "Description", 100, 10)
    product.price = -50
    assert product.price == 100  # Цена не должна измениться


def test_product_price_setter_zero():
    """Тест сеттера цены при попытке установить 0"""
    product = Product("Test Product", "Description", 100, 10)
    product.price = 0
    assert product.price == 100  # Цена не должна измениться


def test_product_addition_1():
    """Тест сложения двух продуктов"""
    product1 = Product("Item 1", "Description 1", 500, 3)
    product2 = Product("Item 2", "Description 2", 1000, 2)

    total_price = product1 + product2
    expected_total = (500 * 3) + (1000 * 2)  # 1500 + 2000 = 3500

    assert total_price == expected_total


def test_product_addition_invalid_1():
    """Тест сложения продукта с невалидным объектом"""
    product = Product("MacBook", "Laptop", 200000, 2)

    with pytest.raises(
        TypeError, match="Складывать можно только объекты класса Product"
    ):
        result = product + "не продукт"


def test_smartphone_addition():
    """Тест сложения двух смартфонов"""
    phone1 = Smartphone(
        "iPhone", "Apple smartphone", 100000, 2, "High", "13 Pro", 256, "Blue"
    )
    phone2 = Smartphone(
        "Samsung", "Android smartphone", 80000, 3, "Medium", "S21", 128, "Black"
    )

    total_price = phone1 + phone2
    expected_total = (100000 * 2) + (80000 * 3)  # 200000 + 240000 = 440000

    assert total_price == expected_total


def test_smartphone_addition_invalid():
    """Тест сложения смартфона с невалидным объектом"""
    phone = Smartphone(
        "iPhone", "Apple smartphone", 100000, 2, "High", "13 Pro", 256, "Blue"
    )

    with pytest.raises(
        TypeError, match="Складывать можно только объекты класса Smartphone"
    ):
        result = phone + "не смартфон"


def test_lawn_grass_addition():
    """Тест сложения двух газонов"""
    grass1 = LawnGrass(
        "Luxury Lawn", "High-quality grass", 700, 10, "Canada", 14, "Green"
    )
    grass2 = LawnGrass(
        "Premium Lawn", "Top-tier grass", 900, 15, "USA", 12, "Light Green"
    )

    total_price = grass1 + grass2
    expected_total = (700 * 10) + (900 * 15)  # 7000 + 13500 = 20500

    assert total_price == expected_total


def test_lawn_grass_addition_invalid():
    """Тест сложения газона с невалидным объектом"""
    grass = LawnGrass(
        "Luxury Lawn", "High-quality grass", 700, 15, "Canada", 10, "Light Green"
    )

    with pytest.raises(
        TypeError, match="Складывать можно только объекты класса LawnGrass"
    ):
        result = grass + "не газон"


def test_base_product_zero_quantity():
    """Проверка, что нельзя создать товар с нулевым количеством."""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Тестовый товар", "Описание", 100, 0)


def test_middle_price():
    """Проверка вычисления среднего ценника товаров в категории."""
    category = Category("Электроника", "Различные гаджеты", [])

    # Проверяем, что при отсутствии товаров средняя цена = 0
    assert category.middle_price() == 0

    # Добавляем товары
    product1 = Product("Товар 1", "Описание 1", 100, 5)
    product2 = Product("Товар 2", "Описание 2", 200, 3)

    category.add_product(product1)
    category.add_product(product2)

    # Средняя цена: (100 + 200) / 2 = 150
    assert category.middle_price() == 150


def test_middle_price_with_one_product():
    """Проверка среднего ценника с одним товаром."""
    category = Category("Одежда", "Мужская одежда", [])
    product = Product("Футболка", "Хлопок", 500, 10)
    category.add_product(product)

    assert category.middle_price() == 500


def test_middle_price_with_one_product_1():
    """Проверка среднего ценника с одним товаром."""
    category = Category("Одежда", "Мужская одежда", [])
    product = Product("Футболка", "Хлопок", 500, 10)
    category.add_product(product)

    assert category.middle_price() == 500
