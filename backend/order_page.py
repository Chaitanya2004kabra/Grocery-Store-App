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

if __name__ == "__main__":
    main()
