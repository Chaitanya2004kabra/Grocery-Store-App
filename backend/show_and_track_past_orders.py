import mysql.connector
from datetime import datetime, timedelta

def get_customer_orders(customer_id):
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )

        cursor = connection.cursor(dictionary=True)

        # Fetch customer orders
        cursor.execute("""
            SELECT order_id, order_date, order_details 
            FROM orders 
            WHERE customer_id = %s
        """, (customer_id,))

        orders = cursor.fetchall()

        # Display orders and track delivery status
        for order in orders:
            order_id = order['order_id']
            order_date = order['order_date']
            order_details = order['order_details']

            # Calculate the time difference
            current_time = datetime.now()
            time_difference = current_time - order_date

            # Determine delivery status
            if time_difference > timedelta(hours=1):
                status = 'Delivered'
            else:
                status = 'Delivery in transit'

            # Display order details
            print(f"Order ID: {order_id}")
            print(f"Order Date: {order_date}")
            print(f"Order Details: {order_details}")
            print(f"Status: {status}")
            print("-" * 20)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    customer_id = input("Enter customer ID: ")
    get_customer_orders(customer_id)
