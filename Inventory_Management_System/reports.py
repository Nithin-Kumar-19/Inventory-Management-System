from datetime import datetime, date
from collections import defaultdict


class ReportManager:
    """
    Generates and prints various reports based on inventory and sales.
    """

    def __init__(self, inventory, sales_manager):
        self.inventory = inventory
        self.sales_manager = sales_manager

    def print_current_inventory(self):
        products = self.inventory.get_all_products()
        if not products:
            print("No products in inventory.")
            return

        print("\n=== Current Inventory ===")
        print("ID | Name | Category | Qty | Buy | Sell | Stock Value (Buy) | Stock Value (Sell)")
        print("-" * 90)

        total_buy_value = 0.0
        total_sell_value = 0.0

        for p in products:
            qty = p["quantity"]
            buy_val = qty * p["buying_price"]
            sell_val = qty * p["selling_price"]
            total_buy_value += buy_val
            total_sell_value += sell_val

            print(
                f"{p['id']} | {p['name']} | {p['category']} | {qty} | "
                f"{p['buying_price']} | {p['selling_price']} | "
                f"{buy_val:.2f} | {sell_val:.2f}"
            )

        print("-" * 90)
        print(f"Total stock value (buying): {total_buy_value:.2f}")
        print(f"Total stock value (selling): {total_sell_value:.2f}")

    def print_low_stock(self, threshold):
        products = self.inventory.get_all_products()
        low_stock_items = [p for p in products if p["quantity"] <= threshold]

        print(f"\n=== Low Stock (<= {threshold}) ===")
        if not low_stock_items:
            print("No low-stock items.")
            return

        print("ID | Name | Category | Qty")
        print("-" * 40)
        for p in low_stock_items:
            print(f"{p['id']} | {p['name']} | {p['category']} | {p['quantity']}")

    def _filter_sales_by_period(self, period):
        sales = self.sales_manager.get_all_sales()
        if period == "today":
            today_str = date.today().isoformat()
            filtered = []
            for s in sales:
                try:
                    ts = datetime.fromisoformat(s["timestamp"])
                    if ts.date().isoformat() == today_str:
                        filtered.append(s)
                except ValueError:
                    continue
            return filtered
        return sales

    def print_sales_summary(self, period="all"):
        sales = self._filter_sales_by_period(period)
        if not sales:
            print("\nNo sales for the selected period.")
            return

        print(f"\n=== Sales Summary ({period}) ===")
        total_revenue = sum(s["total_amount"] for s in sales)
        total_items = sum(s["total_quantity"] for s in sales)

        print(f"Total sales (orders): {len(sales)}")
        print(f"Total items sold: {total_items}")
        print(f"Total revenue: {total_revenue:.2f}")

        print("\nRecent sales (up to 5):")
        print("ID | Time | Customer | Items | Amount")
        print("-" * 70)
        for s in sales[-5:]:
            print(
                f"{s['id']} | {s['timestamp']} | {s['customer_name']} | "
                f"{s['total_quantity']} | {s['total_amount']:.2f}"
            )

    def print_top_selling_products(self, period="all", top_n=5):
        sales = self._filter_sales_by_period(period)
        print(f"\n=== Top Selling Products ({period}) ===")
        if not sales:
            print("No sales for the selected period.")
            return

        product_totals = defaultdict(int)
        revenue_totals = defaultdict(float)

        for s in sales:
            for item in s["items"]:
                pid = item["product_id"]
                pname = item["product_name"]
                key = (pid, pname)
                product_totals[key] += item["quantity"]
                revenue_totals[key] += item["line_total"]

        # Sort by total quantity sold
        ranked = sorted(
            product_totals.items(),
            key=lambda kv: kv[1],
            reverse=True,
        )

        print("Product ID | Name | Qty Sold | Revenue")
        print("-" * 60)
        for (pid, pname), qty in ranked[:top_n]:
            rev = revenue_totals[(pid, pname)]
            print(f"{pid} | {pname} | {qty} | {rev:.2f}")

    def print_sales_by_customer(self, period="all"):
        sales = self._filter_sales_by_period(period)
        print(f"\n=== Sales by Customer ({period}) ===")
        if not sales:
            print("No sales for the selected period.")
            return

        customer_revenue = defaultdict(float)
        customer_items = defaultdict(int)

        for s in sales:
            cname = s["customer_name"]
            customer_revenue[cname] += s["total_amount"]
            customer_items[cname] += s["total_quantity"]

        print("Customer | Orders | Items | Revenue")
        print("-" * 60)
        counts = defaultdict(int)
        for s in sales:
            counts[s["customer_name"]] += 1

        for cname, rev in customer_revenue.items():
            print(
                f"{cname} | {counts[cname]} | {customer_items[cname]} | {rev:.2f}"
            )
