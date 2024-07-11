from connection import get_sql_connection
def verify_user(connection, email, password):
    cursor=connection.cursor()
    query = "SELECT * FROM users WHERE email = %s AND password = %s;"
    cursor.execute(query, (email,password))
    user = cursor.fetchone()
    cursor.close()

    return user
if __name__== '__main__':
    connection=get_sql_connection()
    a=input("Enter email :")
    b=input("Enter password: ")
    user=verify_user(connection,a,b)
    if(user):
        print("Logged in")
    else:
        print("Invalid Credentials")