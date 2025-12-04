from datetime import datetime


class SalesManager:
    """
    Handles recording of sales orders and storage of sales data.
    Each sale can contain multiple line items and an optional customer.
    """

    def __init__(self, inventory, storage, customer_manager):
        """
        inventory: Inventory instance.
        storage: JSONStorage for sales records.
        customer_manager: CustomerManager instance.
        """
        self.inventory = inventory
        self.storage = storage
        self.customer_manager = customer_manager
        self.sales = self.storage.load()

    def _save(self):
        self.storage.save(self.sales)

    def create_sale(self, customer_name=None, phone=None, email=None):
        """
        Start a new sale with a customer (optional).
        Returns a sale dict that the caller can add items to.
        """
        customer = None
        if customer_name:
            customer = self.customer_manager.find_or_create_customer(
                customer_name, phone, email
            )
        sale = {
            "id": f"SALE-{len(self.sales)+1}",
            "customer_id": customer["id"] if customer else None,
            "customer_name": customer["name"] if customer else "Walk-in",
            "items": [],
            "total_quantity": 0,
            "total_amount": 0.0,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
        return sale

    def add_item_to_sale(self, sale, product_id, quantity):
        """
        Add one line item to a sale (does not save yet).

        Returns:
            (success: bool, message: str)
        """
        success, msg = self.inventory.reduce_stock(product_id, quantity)
        if not success:
            return False, msg

        product = self.inventory.get_product_by_id(product_id)
        line_total = product["selling_price"] * quantity

        item = {
            "product_id": product_id,
            "product_name": product["name"],
            "quantity": quantity,
            "unit_price": product["selling_price"],
            "line_total": line_total,
        }
        sale["items"].append(item)
        sale["total_quantity"] += quantity
        sale["total_amount"] += line_total
        return True, f"Added {quantity} x {product['name']} (line total {line_total:.2f})"

    def finalize_sale(self, sale):
        """
        Save a completed sale and return a confirmation message.
        """
        if not sale["items"]:
            return False, "Cannot finalize a sale with no items."

        self.sales.append(sale)
        self._save()
        return True, f"Sale {sale['id']} recorded. Total: {sale['total_amount']:.2f}"

    def get_all_sales(self):
        return list(self.sales)
