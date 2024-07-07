from flask import Flask, request, jsonify
import product
from connection import get_sql_connection

app = Flask(__name__)

connection = get_sql_connection()

@app.route('/getproducts', methods=['GET'])
def get_products():
    products = product.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if  __name__ == "__main__":
    print("starting python flask server for grocery store managemnet system")
    app.run(debug= True, port=5000)
