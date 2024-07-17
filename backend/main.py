from show_and_track_past_orders import get_customer_orders, get_order_id, get_order_status
from orders import main1,cancel_order
from signup import create_user
from login import verify_user
from connection import get_sql_connection


def main():
    print("Welcome to GroceryMart!")

    customer_id = None
    connection = get_sql_connection()
    while True:
        if customer_id is None:
            print("\nAre you a new or existing customer?")
            print("1) New Customer (Sign Up)")
            print("2) Existing Customer (Log In)")
            user_choice = input("Enter your choice (1/2): ")

            if user_choice == '1':
                customer_id = create_user(connection)
            elif user_choice == '2':
                customer_id = verify_user(connection)
                if not customer_id:
                    #connection.close()
                    continue
            else:
                print("Invalid choice. Please try again.")
                #connection.close()
                continue
            #connection.close()

        print("\nWhat would you like to do?")
        print("a) Order")
        print("b) Track Order")
        print("c) Show Previous Orders")
        print("d) Logout")
        print("e) Cancel Order")
        print("f) Exit")

        choice = input("Enter your choice (a/b/c/d/e/f): ").lower()
        if choice == 'a':
            main1(customer_id,connection)
        elif choice == 'b':
            #connection = get_sql_connection()
            print("Here are your orders:")
            get_order_id(customer_id, connection)
            print("-" * 20)
            order_id = int(input("Enter the order_id you want to track: "))
            get_order_status(order_id, connection)
            #connection.close()
        elif choice == 'c':
            #connection = get_sql_connection()
            get_customer_orders(customer_id, connection)
            #connection.close()
        elif choice == 'd':
            customer_id = None
            print("You have been logged out.")
        elif choice == 'e':
            order_id=int(input("Enter the id of order you want to cancel : "))
            cancel_order(connection,order_id,customer_id)
        elif choice == 'f':
            print("Goodbye!")
            connection.close()
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
