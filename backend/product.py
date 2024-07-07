from connection import get_sql_connection


def get_all_products (connection):
    cursor = connection.cursor()

    query = ("select * from products")
    cursor.execute(query)
    response = []
    for (product_id,product_name,price, quantity ,measurement) in cursor :
        response.append (
            {
                'product_id' : product_id,
                'product_name': product_name,
                'price': price, 
                'quantity' : quantity,
                'measurement':measurement
            }
        
        )            
    return response

def add_into_products (connection,product):
    cursor = connection.cursor()

    query = ("insert into products (product_name,price, quantity ,measurement) values (%s, %s,%s,%s)")
    data = (product['product_name'], product['price'], product['quantity'],product['measurement'])
    cursor.execute(query,data)
    connection.commit()

    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products where product_id=" + str(product_id))
    cursor.execute(query)
    connection.commit()



if __name__ == '__main__':
    connection = get_sql_connection()

    print(get_all_products(connection))
    # int(add_into_products(connection, {
    #     'product_name': 'potatoes',
    #     'price': '15',
    #     'quantity': '30',
    #     'measurement':'1'
    # }))

    