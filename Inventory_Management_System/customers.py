import uuid


class CustomerManager:
    """
    Manages customers: add, find, and list.
    """

    def __init__(self, storage):
        """
        storage: JSONStorage for customers.
        """
        self.storage = storage
        self.customers = self.storage.load()

    def _save(self):
        self.storage.save(self.customers)

    def _generate_id(self):
        return str(uuid.uuid4())[:8]

    def add_customer(self, name, phone=None, email=None):
        customer = {
            "id": self._generate_id(),
            "name": name,
            "phone": phone or "",
            "email": email or "",
        }
        self.customers.append(customer)
        self._save()
        return customer

    def get_customer_by_id(self, customer_id):
        for c in self.customers:
            if c["id"] == customer_id:
                return c
        return None

    def find_or_create_customer(self, name, phone=None, email=None):
        # Very simple logic: if there is a customer with same name and phone, reuse
        for c in self.customers:
            if c["name"].lower() == name.lower() and (phone is None or c["phone"] == phone):
                return c
        return self.add_customer(name, phone, email)

    def get_all_customers(self):
        return list(self.customers)
