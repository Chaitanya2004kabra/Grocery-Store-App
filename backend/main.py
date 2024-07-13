from show_and_track_past_orders import get_customer_orders, get_order_id, get_order_status
from orders import main1
from connection import get_sql_connection

def main():
    print("Welcome to GroceryMart!")

    customer_id = int(input("Please enter your customer ID: "))

    print("What would you like to do?")
    print("a) Order")
    print("b) Track Order")
    print("c) Show Previous Orders")

    choice = input("Enter your choice (a/b/c): ").lower()
    if choice == 'a':
        main1(customer_id)
    elif choice == 'b':
        connection=get_sql_connection()
        print("Here are your orders :")
        get_order_id(customer_id,connection)
        print("-" * 20)
        order_id = int(input("Enter the order_id you want to track :"))
        get_order_status(order_id,connection)
        connection.close()
    elif choice == 'c':
        connection=get_sql_connection()
        get_customer_orders(customer_id,connection)
        connection.close()
    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
