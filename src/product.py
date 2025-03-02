class Product:
    all_products = []  # Хранение всех созданных продуктов

    def __init__(self, name: str, description: str, price: float, quantity: int):
        if price <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        if quantity < 0:
            raise ValueError("Количество товара не может быть отрицательным")

        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут
        self.quantity = quantity

        Product.all_products.append(self)  # Добавляем товар в общий список

    @property
    def price(self):
        """Геттер для получения цены товара."""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """Сеттер для установки новой цены с проверками."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            confirm = input(f"Вы уверены, что хотите понизить цену с {self.__price} до {new_price}? (y/n): ")
            if confirm.lower() != "y":
                print("Изменение цены отменено.")
                return

        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict):
        """
        Создает новый объект Product на основе product_data.
        Если товар с таким же именем уже существует в Product.all_products,
        обновляет количество и выбирает наибольшую цену.
        """
        name = product_data.get("name")
        description = product_data.get("description")
        price = product_data.get("price")
        quantity = product_data.get("quantity")

        if not all([name, description, isinstance(price, (int, float)), isinstance(quantity, int)]):
            raise ValueError("Некорректные данные для создания продукта")

        for product in cls.all_products:
            if product.name == name:
                product.quantity += quantity
                product.price = max(product.price, price)
                return product

        return cls(name, description, price, quantity)


class Category:
    category_count = 0  # Количество категорий
    product_count = 0  # Количество товаров

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = []  # Приватный список товаров
        Category.category_count += 1

        for product in products:
            self.add_product(product)

    def add_product(self, product: Product):
        """Добавляет продукт в категорию. Если товар уже есть, обновляет количество."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")

        for existing_product in self.__products:
            if existing_product.name == product.name:
                existing_product.quantity += product.quantity
                existing_product.price = max(existing_product.price, product.price)
                return

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Геттер для списка товаров. Возвращает строку с описанием товаров."""
        if not self.__products:
            return "В категории нет товаров."

        return "\n".join(
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            for product in self.__products
        )
