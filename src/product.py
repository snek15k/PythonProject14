class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    category_count = 0  # Количество категорий
    product_count = 0  # Количество товаров

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.products = []  # Список объектов класса Product
        Category.category_count += 1

        # Добавляем продукты через add_product(), чтобы обновить product_count
        for product in products:
            self.add_product(product)

    def add_product(self, product: Product):
        """Добавляет продукт в категорию и обновляет счетчик товаров"""
        if isinstance(product, Product):
            self.products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product")
