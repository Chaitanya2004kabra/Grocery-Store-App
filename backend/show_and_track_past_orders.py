from datetime import datetime, timedelta


def get_customer_orders(customer_id,connection):
    cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get dictionaries instead of tuples

    cursor.execute("""
                SELECT o.order_date,p.product_name
                FROM orders o
                JOIN order_items od ON o.order_id = od.order_id
                JOIN products p ON od.product_id = p.product_id
                WHERE o.customer_id = %s
                ORDER BY o.order_date DESC
                """, (customer_id,))
    orders = cursor.fetchall()

    # Display orders and dynamically determine delivery status
    for order in orders:
        order_date = order['order_date']
        product_name = order['product_name']

        current_time = datetime.now()
        time_difference = current_time - order_date
        if time_difference > timedelta(hours=0.5):
            status = 'Delivered'
        else:
            status = 'Delivery in transit'
        print(f"Your order for {product_name} is {status}")
    cursor.close()


def get_order_status(order_id,connection):
    cursor = connection.cursor(dictionary=True)
    sql = """
                   SELECT o.order_date, p.product_name
                   FROM orders o
                   JOIN order_items oi ON o.order_id = oi.order_id
                   JOIN products p ON oi.product_id = p.product_id
                   WHERE o.order_id = %s
               """
    cursor.execute(sql, (order_id,))
    results = cursor.fetchall()
    if not results:
        print(f"No order found with order_id {order_id}")
        return

    for result in results:
        order_date = result['order_date']
        product_name = result['product_name']
        time_difference = datetime.now() - order_date

        if time_difference > timedelta(hours=0.5):
            status = "delivered"
        else:
            status = "in transit"
        print(f"Your order for {product_name} is {status}")
    cursor.close()


def get_order_id(customer_id,connection):
    cursor = connection.cursor(dictionary=True)
    query = """
                SELECT o.order_id, p.product_name
                FROM orders o
                JOIN order_items od ON o.order_id = od.order_id
                JOIN products p ON od.product_id = p.product_id
                WHERE o.customer_id = %s
            """
    cursor.execute(query, (customer_id,))  # Note the comma to create a single-element tuple
    results = cursor.fetchall()
    # Print the results
    for result in results:
        order_id = result['order_id']
        product_name = result['product_name']
        print(f"Order ID: {order_id}, Product Name: {product_name}")
    cursor.close()
