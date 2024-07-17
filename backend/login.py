from connection import get_sql_connection


def verify_user(connection):
    print("Log In")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE email = %s AND password = %s;"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        print(f"Welcome back, {user[1]}!")  # Assuming the second element is the name
        return user[0]  # Assuming the first element is the customer ID
    else:
        print("Invalid email or password. Please try again.")
        return None


if __name__ == '__main__':
    connection = get_sql_connection()
    user_id = verify_user(connection)
    if user_id:
        print(f"Logged in with user ID: {user_id}")
    connection.close()
