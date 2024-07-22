from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, json
from signup import create_user
from login import verify_user
from product import get_all_products
from orders import main1, cancel_order, insert_order, update_inventory
from show_and_track_past_orders import get_customer_orders, get_order_id, get_order_status
from connection import get_sql_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

connection = get_sql_connection()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        phone = request.form['phone']

        cursor = connection.cursor()
        query = ("INSERT INTO users "
                 "(name, email, password, address, phone) "
                 "VALUES (%s, %s, %s, %s, %s)")
        data = (name, email, password, address, phone)
        cursor.execute(query, data)
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        session['customer_id'] = user_id
        return redirect(url_for('home'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_id = verify_user(connection, email, password)

        if user_id:
            session['customer_id'] = user_id
            return redirect(url_for('home'))
        else:
            return "Invalid email or password."

    return render_template('login.html')


@app.route('/home')
def home():
    if 'customer_id' not in session:
        return redirect(url_for('login'))

    return render_template('home.html')


@app.route('/order', methods=['GET', 'POST'])
def order():

    products = get_all_products(connection)

    return render_template('order.html', products=products)


@app.route('/checkout', methods=['POST'])
def checkout():
    items = []
    total = 0

    products = get_all_products(connection)

    for key, value in request.form.items():
        if key.startswith('quantity_'):
            product_id = int(key.split('_')[1])
            quantity = int(value) if value else 0
            if quantity > 0:
                product = next((p for p in products if p['product_id'] == product_id), None)
                if product:
                    total_price = product['price'] * quantity
                    items.append({
                        'product_id': product_id,
                        'product_name': product['product_name'],
                        'quantity': quantity,
                        'price': product['price'],
                        'total_price': total_price
                    })
                    total += total_price

    return render_template('checkout.html', items=items, total=total)


@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    if 'customer_id' not in session:
        return redirect(url_for('home'))

    items = []
    total = 0

    products = get_all_products(connection)

    for key, value in request.form.items():
        if key.startswith('quantity_'):
            product_id = int(key.split('_')[1])
            quantity = int(value) if value.strip() else 0
            if quantity > 0:
                product = next((p for p in products if p['product_id'] == product_id), None)
                if product:
                    items.append({
                        'product_id': product_id,
                        'quantity': quantity,
                        'price': product['price']
                    })
                    total += product['price'] * quantity

    if not items:
        return "No items to order", 400

    # Insert order and update inventory
    order_id = insert_order(connection, items, total, session['customer_id'])
    update_inventory(connection, items)

    return render_template('order_status1.html',order_id=order_id)
    #return f"Order ID {order_id} has been placed successfully.<br><a href='{url_for('home')}'>Back to home</a>"


@app.route('/track_order', methods=['GET', 'POST'])
def track_order():
    if 'customer_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        order_id = request.form.get('order_id')
        if order_id:
            order_details, error = get_order_status(order_id, connection)
            if error:
                return render_template('order_status.html', error=error)
            else:
                return render_template('order_status.html', order_id=order_id, order_details=order_details)
        else:
            return render_template_string("""
                <p>Order ID is required.</p>
                <br><br>
                <a href="{{ url_for('home') }}">Back to Home</a>
            """)

    return render_template('track_order.html')


@app.route('/previous_orders')
def previous_orders():
    if 'customer_id' not in session:
        return redirect(url_for('login'))

    customer_id = session['customer_id']
    orders = get_customer_orders(customer_id, connection)

    return render_template('previous_orders.html', orders=orders)


@app.route('/view_order_ids', methods=['GET'])
def view_order_ids():
    if 'customer_id' not in session:
        return redirect(url_for('login'))

    customer_id = session['customer_id']
    order_data = get_order_id(customer_id, connection)

    return render_template('view_order_ids.html', orders=order_data)


@app.route('/cancel_order', methods=['GET', 'POST'])
def cancel_order_route():
    if 'customer_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        order_id = request.form['order_id']
        message = cancel_order(connection, order_id, session['customer_id'])
        return render_template('cancel_status.html', message=message)

    return render_template('cancel_order.html')


@app.route('/logout')
def logout():
    session.pop('customer_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
