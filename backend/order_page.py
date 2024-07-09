from datetime import datetime

from connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM products"
    cursor.execute(query)
    response = []
    for (product_id, product_name, price, quantity, measurement) in cursor:
        response.append({
            'product_id': product_id,
            'product_name': product_name,
            'price': price,
            'quantity': quantity,
            'measurement': measurement
        })
    return response

def insert_order(connection, order):
    cursor = connection.cursor()
    order_query = "INSERT INTO orders (order_date) VALUES (%s)"
    cursor.execute(order_query, (datetime.now(),))
    order_id = cursor.lastrowid

    order_item_query = "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)"
    for item in order:
        cursor.execute(order_item_query, (order_id, item['product']['product_id'], item['quantity'], item['product']['price']))

    connection.commit()
    return order_id

def main():
    connection = get_sql_connection()
    products = get_all_products(connection)

    print("Available products:")
    for product in products:
        print(f"{product['product_id']}: {product['product_name']} - {product['price']} per {product['measurement']}")

    total = 0
    order = []

    while True:
        product_id = input("Enter the product ID you want to order (or 'done' to finish): ")
        if product_id.lower() == 'done':
            break

        try:
            product_id = int(product_id)
            product = next((p for p in products if p['product_id'] == product_id), None)
            if not product:
                print("Product not found.")
                continue

            quantity = int(input(f"Enter the quantity for {product['product_name']}: "))
            order.append({'product': product, 'quantity': quantity})
            total += product['price'] * quantity

        except ValueError:
            print("Invalid input. Please enter numeric values.")

    print("\nYour order:")
    for item in order:
        product = item['product']
        quantity = item['quantity']
        print(f"{product['product_name']}: {quantity} {product['measurement']} @ {product['price']} each")

    print(f"\nTotal cost: {total}")

    order_id = insert_order(connection, order)
    print(f"Order ID {order_id} has been placed successfully.")

if __name__ == "__main__":
    main()
