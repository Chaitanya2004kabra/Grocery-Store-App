from connection import get_sql_connection

def create_user(connection):
    print("Sign Up")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    address = input("Enter your address: ")
    phone = input("Enter your phone number: ")

    user_data = {
        'name': name,
        'email': email,
        'password': password,
        'address': address,
        'phone': phone
    }

    cursor = connection.cursor()
    query = ("INSERT INTO users "
             "(name, email, password, address, phone) "
             "VALUES (%s, %s, %s, %s, %s)")
    data = (user_data['name'], user_data['email'], user_data['password'], user_data['address'], user_data['phone'])
    cursor.execute(query, data)
    connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    print(f"Account created successfully! Your customer ID is: {user_id}")
    return user_id

def get_users(connection, id):
    cursor = connection.cursor()
    query = "SELECT * FROM users where id = %s;" % (id)
    cursor.execute(query)

    records = []
    for (id, name, email, password, address, phone) in cursor:
        records.append({
            'customer_id': id,
            'customer_name': name,
            'email': email,
            'pass': password,
            'address': address,
            'contact': phone
        })

    cursor.close()
    return records

if __name__ == '__main__':
    connection = get_sql_connection()
    user_id = create_user(connection)
    print(get_users(connection, user_id))
    connection.close()
