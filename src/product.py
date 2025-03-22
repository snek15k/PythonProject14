from abc import ABC, abstractmethod


class InitPrintMixin:
    def __init__(self, *args, **kwargs):
        class_name = self.__class__.__name__
        print(f"Создан объект класса {class_name} с параметрами: {args}, {kwargs}")
        super().__init__(*args, **kwargs)


class BaseProduct(ABC):
    all_products = []  # Хранение всех созданных продуктов

    def __init__(self, name: str, description: str, price: float, quantity: int):
        if price <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        if quantity <= 0:  # Теперь проверяем и нулевое количество
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут
        self.quantity = quantity

        BaseProduct.all_products.append(self)  # Добавляем товар в общий список

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

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
            confirm = input(
                f"Вы уверены, что хотите понизить цену с {self.__price} до {new_price}? (y/n): "
            )
            if confirm.lower() != "y":
                print("Изменение цены отменено.")
                return

        self.__price = new_price


class Product(InitPrintMixin, BaseProduct):
    @classmethod
    def new_product(cls, product_data):
        # Проверяем, существует ли уже продукт с таким именем
        for product in cls.all_products:
            if product.name == product_data["name"]:
                # Обновляем количество товара
                product.quantity += product_data["quantity"]
                # Если новая цена выше текущей, обновляем её
                if product_data["price"] > product.price:
                    product.price = product_data["price"]
                return product  # Возвращаем обновленный объект, не создавая новый

        # Если такого продукта нет, создаём новый
        new_product = cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )
        cls.all_products.append(new_product)
        return new_product

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Складывать можно только объекты класса Product")
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        return (
            f"{self.name} ({self.model}), {self.memory}GB, {self.color}, "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )

    def __add__(self, other):
        if not isinstance(other, Smartphone):
            raise TypeError("Складывать можно только объекты класса Smartphone")
        return super().__add__(other)


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return (
            f"{self.name} ({self.color}), из {self.country}, "
            f"прорастает за {self.germination_period} дней, "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )

    def __add__(self, other):
        if not isinstance(other, LawnGrass):
            raise TypeError("Складывать можно только объекты класса LawnGrass")
        return super().__add__(other)


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

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product):
        """Добавляет продукт в категорию. Проверяет, является ли объект наследником Product."""
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты класса Product или его наследников"
            )

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

        return "\n".join(str(product) for product in self.__products)

    def middle_price(self):
        """Подсчитывает средний ценник всех товаров в категории."""
        try:
            total_price = sum(product.price for product in self.__products)
            total_products = len(self.__products)
            return total_price / total_products
        except ZeroDivisionError:
            return 0  # Если товаров нет, возвращаем 0 вместо ошибки
