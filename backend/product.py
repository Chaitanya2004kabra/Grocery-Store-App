from connection import get_sql_connection


def get_all_products (connection):
    cursor = connection.cursor()

    query = ("SELECT product_id,product_name, price,inventory, m.measure_name FROM grocery_store.products as s join measurement as m on s.measurement = m.measure_id")
    cursor.execute(query)
    response = []
    for (product_id,product_name,price, inventory ,measure_name) in cursor :
        response.append (
            {
                'product_id' : product_id,
                'product_name': product_name,
                'price': price, 
                'inventory' : inventory,
                'measure_name':measure_name
            }
        
        )            
    return response

def add_into_products (connection,product):
    cursor = connection.cursor()

    query = ("insert into products (product_name,price, inventory ,measurement) values (%s, %s,%s,%s)")
    data = (product['product_name'], product['price'], product['inventory'],product['measurement'])
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
    #     'inventory': '30',
    #     'measurement':'1'
    # }))

    