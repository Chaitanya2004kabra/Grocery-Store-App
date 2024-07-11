import os

def main():
    print("Welcome to GroceryMart!")

    customer_id = input("Please enter your customer ID: ")

    print("What would you like to do?")
    print("a) Order")
    print("b) Track Order")
    print("c) Show Previous Orders")

    choice = input("Enter your choice (a/b/c): ").lower()

    if choice == 'a':
        os.system(f"python order_page.py {customer_id}")
    elif choice == 'b':
        os.system("python track_order.py")
    elif choice == 'c':
        os.system(f"python show_prev_order.py")
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
