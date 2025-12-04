import uuid


class Inventory:
    """
    Manages product inventory: add, update, delete, search.
    """

    def __init__(self, storage):
        """
        storage: an object with load() and save(data) methods (JSONStorage).
        """
        self.storage = storage
        self.products = self.storage.load()

    def _save(self):
        self.storage.save(self.products)

    def _generate_id(self):
        # Short unique ID for a product
        return str(uuid.uuid4())[:8]

    def add_product(self, name, category, buying_price, selling_price, quantity):
        product = {
            "id": self._generate_id(),
            "name": name,
            "category": category,
            "buying_price": float(buying_price),
            "selling_price": float(selling_price),
            "quantity": int(quantity),
        }
        self.products.append(product)
        self._save()

    def get_all_products(self):
        return list(self.products)

    def get_product_by_id(self, product_id):
        for p in self.products:
            if p["id"] == product_id:
                return p
        return None

    def update_product(
        self,
        product_id,
        name=None,
        category=None,
        buying_price=None,
        selling_price=None,
        quantity=None,
    ):
        product = self.get_product_by_id(product_id)
        if not product:
            return False

        if name is not None:
            product["name"] = name
        if category is not None:
            product["category"] = category
        if buying_price is not None:
            product["buying_price"] = float(buying_price)
        if selling_price is not None:
            product["selling_price"] = float(selling_price)
        if quantity is not None:
            product["quantity"] = int(quantity)

        self._save()
        return True

    def delete_product(self, product_id):
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        self.products.remove(product)
        self._save()
        return True

    def search_products(self, keyword):
        keyword_lower = keyword.lower()
        results = []
        for p in self.products:
            if (
                keyword_lower in p["name"].lower()
                or keyword_lower == p["id"].lower()
            ):
                results.append(p)
        return results

    def reduce_stock(self, product_id, quantity):
        """
        Decrease stock for a given product.

        Returns:
            (success: bool, message: str)
        """
        product = self.get_product_by_id(product_id)
        if not product:
            return False, "Product not found."

        if quantity <= 0:
            return False, "Quantity must be positive."

        if product["quantity"] < quantity:
            return False, "Not enough stock for this sale."

        product["quantity"] -= quantity
        self._save()
        return True, "Stock updated."
