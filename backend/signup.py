from connection import get_sql_connection
def create_user(connection, user_data):
    cursor = connection.cursor()
    query = ("INSERT INTO users "
             "(name, email, password, address, phone) "
             "VALUES (%s, %s, %s, %s, %s)")
    data = (user_data['name'], user_data['email'],user_data['password'], user_data['address'], user_data['phone'])
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
def get_users(connection, id):
    cursor = connection.cursor()
    query = "SELECT * FROM users where user_id= %s;" % (id);
    cursor.execute(query)

    records = []
    for (user_id ,name,email, password, address, phone) in cursor:
        records.append({
            'user_id': user_id,
            'customer_name':  name,
            'email': email,
            'pass': password,
            'address': address,
            'contact': phone
        })

    cursor.close()

    return records


if __name__ == '__main__':
    connection = get_sql_connection() 
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

    create_user(connection, user_data)

    print("User created successfully!")

    print(get_users(connection,1))
    connection.close()
