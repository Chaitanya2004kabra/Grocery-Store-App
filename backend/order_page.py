import sys
from datetime import datetime
from product import get_all_products
from connection import get_sql_connection

def insert_order(connection, order, total, customer_id):
    cursor = connection.cursor()
    order_query = "INSERT INTO orders (order_date, total, customer_id) VALUES (%s, %s, %s)"
    cursor.execute(order_query, (datetime.now(), total, customer_id))
    order_id = cursor.lastrowid

    order_item_query = "INSERT INTO order_items (order_id, product_id, quantity, price, customer_id) VALUES (%s, %s, %s, %s, %s)"
    for item in order:
        cursor.execute(order_item_query, (order_id, item['product']['product_id'], item['quantity'], item['product']['price'], customer_id))

    connection.commit()
    return order_id

def update_inventory(connection, order):
    cursor = connection.cursor()
    
    for item in order:
        product_id = item['product']['product_id']
        quantity = item['quantity']
        update_query = "UPDATE products SET inventory = inventory - %s WHERE product_id = %s"
        cursor.execute(update_query, (quantity, product_id))
    connection.commit()

def show_inventory(connection):
    products = get_all_products(connection)

    print("Remaining inventory:")
    for product in products:
        print(f"{product['product_id']}: {product['product_name']} inventory {product['inventory']}")

def main(customer_id):
    connection = get_sql_connection()
    products = get_all_products(connection)

    print("\nAvailable products:")
    for product in products:
        print(f"{product['product_id']}: {product['product_name']} - {product['price']} per {product['measure_name']}")

    total = 0
    order = []

    while True:
        product_id = input("\nEnter the product ID you want to order (or 'done' to finish): ")
        if product_id.lower() == 'done':
            break
        
        try:
            product_id = int(product_id)
            product = next((p for p in products if p['product_id'] == product_id), None)
            if not product:
                print("Product not found.")
                continue

            if product['inventory'] == 0:
                print(f"Warning: {product['product_name']} is out of stock.")
                continue

            quantity = int(input(f"Enter the quantity for {product['product_name']}(available: {product['inventory']}): "))

            if quantity <= 0:
                print("Quantity must be greater than zero.")
                continue
            if quantity > product['inventory']:
                print(f"Warning: Insufficient inventory for {product['product_name']}. Available quantity: {product['inventory']}.")
                continue

            order.append({'product': product, 'quantity': quantity})
            total += product['price'] * quantity

        except ValueError:
            print("Invalid input. Please enter numeric values.")

    print("\nYour order:")
    for item in order:
        product = item['product']
        quantity = item['quantity']
        print(f"{product['product_name']}: {quantity} {product['measure_name']} @ {product['price']} each")

    print(f"\nTotal cost: {total}")

    order_id = insert_order(connection, order, total, customer_id)
    update_inventory(connection, order)
    print(f"Order ID {order_id} has been placed successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python order_page.py <customer_id>")
        sys.exit(1)

    customer_id = sys.argv[1]
    main(customer_id)


if __name__ == "__main__":
    main()
