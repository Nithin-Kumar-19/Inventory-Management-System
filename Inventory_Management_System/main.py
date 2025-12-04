from inventory import Inventory
from sales import SalesManager
from reports import ReportManager
from storage import JSONStorage
from customers import CustomerManager


def main_menu():
    print("\n=== Inventory Management System ===")
    print("1. Manage Products")
    print("2. Record Sale")
    print("3. Reports")
    print("4. Manage Customers")
    print("5. Exit")


def products_menu():
    print("\n--- Product Management ---")
    print("1. Add Product")
    print("2. Update Product")
    print("3. Delete Product")
    print("4. View All Products")
    print("5. Search Product")
    print("6. Back to Main Menu")


def reports_menu():
    print("\n--- Reports ---")
    print("1. Current Inventory")
    print("2. Low Stock Report")
    print("3. Sales Summary")
    print("4. Top Selling Products")
    print("5. Sales by Customer")
    print("6. Back to Main Menu")


def customers_menu():
    print("\n--- Customer Management ---")
    print("1. Add Customer")
    print("2. View All Customers")
    print("3. Back to Main Menu")


def get_int_input(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank and value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid integer.")


def get_float_input(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank and value == "":
            return None
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")


def run():
    # Storage and managers
    product_storage = JSONStorage("products.json")
    sales_storage = JSONStorage("sales.json")
    customer_storage = JSONStorage("customers.json")

    inventory = Inventory(product_storage)
    customer_manager = CustomerManager(customer_storage)
    sales_manager = SalesManager(inventory, sales_storage, customer_manager)
    report_manager = ReportManager(inventory, sales_manager)

    print("Welcome to the Inventory Management System!")

    while True:
        main_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # Product management
            while True:
                products_menu()
                p_choice = input("Enter your choice: ").strip()

                if p_choice == "1":
                    name = input("Product name: ").strip()
                    category = input("Category: ").strip()
                    buying_price = get_float_input("Buying price: ")
                    selling_price = get_float_input("Selling price: ")
                    quantity = get_int_input("Initial quantity: ")

                    inventory.add_product(
                        name=name,
                        category=category,
                        buying_price=buying_price,
                        selling_price=selling_price,
                        quantity=quantity,
                    )
                    print("Product added successfully.")

                elif p_choice == "2":
                    product_id = input("Enter product ID to update: ").strip()
                    product = inventory.get_product_by_id(product_id)
                    if not product:
                        print("Product not found.")
                        continue

                    print("Leave a field blank to keep current value.")
                    new_name = input(f"Name [{product['name']}]: ").strip()
                    new_category = input(f"Category [{product['category']}]: ").strip()
                    new_buying_price = get_float_input(
                        f"Buying price [{product['buying_price']}]: ", allow_blank=True
                    )
                    new_selling_price = get_float_input(
                        f"Selling price [{product['selling_price']}]: ",
                        allow_blank=True,
                    )
                    new_quantity = get_int_input(
                        f"Quantity [{product['quantity']}]: ", allow_blank=True
                    )

                    inventory.update_product(
                        product_id,
                        name=new_name or None,
                        category=new_category or None,
                        buying_price=new_buying_price,
                        selling_price=new_selling_price,
                        quantity=new_quantity,
                    )
                    print("Product updated successfully.")

                elif p_choice == "3":
                    product_id = input("Enter product ID to delete: ").strip()
                    if inventory.delete_product(product_id):
                        print("Product deleted.")
                    else:
                        print("Product not found.")

                elif p_choice == "4":
                    products = inventory.get_all_products()
                    if not products:
                        print("No products in inventory.")
                    else:
                        print("\nID | Name | Category | Buy | Sell | Qty")
                        print("-" * 60)
                        for p in products:
                            print(
                                f"{p['id']} | {p['name']} | {p['category']} | "
                                f"{p['buying_price']} | {p['selling_price']} | {p['quantity']}"
                            )

                elif p_choice == "5":
                    keyword = input("Enter product name or ID to search: ").strip()
                    results = inventory.search_products(keyword)
                    if not results:
                        print("No matching products found.")
                    else:
                        print("\nID | Name | Category | Buy | Sell | Qty")
                        print("-" * 60)
                        for p in results:
                            print(
                                f"{p['id']} | {p['name']} | {p['category']} | "
                                f"{p['buying_price']} | {p['selling_price']} | {p['quantity']}"
                            )

                elif p_choice == "6":
                    break
                else:
                    print("Invalid choice. Please select from the menu.")

        elif choice == "2":
            # Record a sale with multiple items and optional customer
            print("\n--- Record Sale ---")
            cust_choice = input("Is this a known customer? (y/n): ").strip().lower()
            customer_name = None
            phone = None
            email = None

            if cust_choice == "y":
                # Optionally list customers or just ask name
                sub = input("Do you want to view all customers? (y/n): ").strip().lower()
                if sub == "y":
                    customers = customer_manager.get_all_customers()
                    if not customers:
                        print("No customers yet.")
                    else:
                        print("ID | Name | Phone | Email")
                        print("-" * 50)
                        for c in customers:
                            print(
                                f"{c['id']} | {c['name']} | {c['phone']} | {c['email']}"
                            )
                customer_name = input("Enter customer name (existing or new): ").strip()
                phone = input("Phone (optional): ").strip() or None
                email = input("Email (optional): ").strip() or None
            else:
                customer_name = "Walk-in"

            sale = sales_manager.create_sale(
                customer_name=customer_name, phone=phone, email=email
            )

            while True:
                product_id = input("Enter product ID to add (or 'done' to finish): ").strip()
                if product_id.lower() == "done":
                    break

                quantity = get_int_input("Quantity to sell: ")
                success, message = sales_manager.add_item_to_sale(
                    sale, product_id, quantity
                )
                print(message)

            success, message = sales_manager.finalize_sale(sale)
            print(message)

        elif choice == "3":
            # Reports
            while True:
                reports_menu()
                r_choice = input("Enter your choice: ").strip()

                if r_choice == "1":
                    report_manager.print_current_inventory()

                elif r_choice == "2":
                    threshold = get_int_input("Enter low stock threshold (e.g., 5): ")
                    report_manager.print_low_stock(threshold)

                elif r_choice == "3":
                    print("Sales summary options:")
                    print("1. All time")
                    print("2. Today only")
                    period_choice = input("Enter your choice: ").strip()
                    if period_choice == "1":
                        report_manager.print_sales_summary(period="all")
                    elif period_choice == "2":
                        report_manager.print_sales_summary(period="today")
                    else:
                        print("Invalid choice. Showing all-time summary.")
                        report_manager.print_sales_summary(period="all")

                elif r_choice == "4":
                    print("Top selling products options:")
                    print("1. All time")
                    print("2. Today only")
                    period_choice = input("Enter your choice: ").strip()
                    if period_choice == "1":
                        report_manager.print_top_selling_products(period="all")
                    elif period_choice == "2":
                        report_manager.print_top_selling_products(period="today")
                    else:
                        print("Invalid choice. Showing all-time top sellers.")
                        report_manager.print_top_selling_products(period="all")

                elif r_choice == "5":
                    print("Sales by customer options:")
                    print("1. All time")
                    print("2. Today only")
                    period_choice = input("Enter your choice: ").strip()
                    if period_choice == "1":
                        report_manager.print_sales_by_customer(period="all")
                    elif period_choice == "2":
                        report_manager.print_sales_by_customer(period="today")
                    else:
                        print("Invalid choice. Showing all-time customer stats.")
                        report_manager.print_sales_by_customer(period="all")

                elif r_choice == "6":
                    break
                else:
                    print("Invalid choice. Please select from the menu.")

        elif choice == "4":
            # Customer management
            while True:
                customers_menu()
                c_choice = input("Enter your choice: ").strip()

                if c_choice == "1":
                    name = input("Customer name: ").strip()
                    phone = input("Phone (optional): ").strip() or None
                    email = input("Email (optional): ").strip() or None
                    customer = customer_manager.add_customer(name, phone, email)
                    print(f"Customer added with ID: {customer['id']}")

                elif c_choice == "2":
                    customers = customer_manager.get_all_customers()
                    if not customers:
                        print("No customers yet.")
                    else:
                        print("ID | Name | Phone | Email")
                        print("-" * 50)
                        for c in customers:
                            print(
                                f"{c['id']} | {c['name']} | {c['phone']} | {c['email']}"
                            )

                elif c_choice == "3":
                    break
                else:
                    print("Invalid choice. Please select from the menu.")

        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select from the menu.")


if __name__ == "__main__":
    run()
