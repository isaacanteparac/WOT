from itertools import permutations
import MySQLdb
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

#conexion database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root_ia'
app.config['MYSQL_PASSWORD'] = 'root_ia'
app.config['MYSQL_DB'] = 'syin'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login/verification')
def verification_login():
    mail = request.form['mail']
    password = request.form['password']
    '''consult_exe = mysql.connection.cursor()
    consult_exe.execute('SELECT * FROM `usuario` WHERE mail = %s AND password = %s',(mail,password))
    data = consult_exe.fetchall()
    mysql.connection.commit()'''
    print("mail = "+mail)
    print("password = "+password)
    return 'verificacion de login'




@app.route('/sign-up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign-up/create', methods=['POST'])
def data_signup():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        mail = request.form['mail']
        username = request.form['username']
        password= request.form['password']
        consult_exe = mysql.connection.cursor()
        consult_exe.execute('INSERT INTO usuario (name, last_name, mail, username, password)'+
                        'VALUES(%s,%s,%s,%s,%s)',(name,last_name,mail,username,password))
        mysql.connection.commit()
        return redirect(url_for('products'))


#DASHBOARD
@app.route('/dashboard')
def dashboard():
    return render_template('layout.html')


#PRODUCTS
@app.route('/products')
def products():
    return render_template('views_products.html', products = get_consult('products'))


@app.route('/products/create')
def create_product():
    return render_template('create_product.html', 
    ctl_measured_units = get_consult('ctl_measured_units'), 
    ctl_status = get_consult('ctl_status')
    ,ctl_types_products = get_consult('ctl_types_products'),
    ctl_inventory_methods = get_consult('ctl_inventory_methods')
    ,ctl_product_etiquette = get_consult('ctl_product_etiquette'))



@app.route('/products/create/add', methods=['POST'])
def create_add_products():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        amount = request.form['amount']
        description = request.form['description']
        ctl_status = request.form['id_ctl_status']
        ctl_measured = request.form['id_ctl_measured_units']
        ctl_types_products = request.form['id_ctl_types_products']
        ctl_inventory_methods = request.form['id_ctl_inventory_methods']
        ctl_product_etiquette = request.form['id_ctl_product_etiquette']
        consult_exe = mysql.connection.cursor()
        consult_exe.execute('INSERT INTO products (name, code, amount, description,id_ctl_status ,id_ctl_measured_units,id_ctl_types_products,id_ctl_inventory_methods,id_ctl_product_etiquette)'+
                        'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                        ,(name,code,amount,description,ctl_status,ctl_measured,ctl_types_products,ctl_inventory_methods,ctl_product_etiquette))
        mysql.connection.commit()
        return redirect(url_for('products'))



@app.route('/products/edit/<string:id>')
def edit_products(id):
    return render_template('edit_id_product.html', 
    products_data = get_consult('products WHERE id = {0}'.format(id))[0],
    ctl_measured_units = get_consult('ctl_measured_units'), 
    ctl_status = get_consult('ctl_status')
    ,ctl_types_products = get_consult('ctl_types_products'),
    ctl_inventory_methods = get_consult('ctl_inventory_methods')
    ,ctl_product_etiquette = get_consult('ctl_product_etiquette'))


@app.route('/products/edit/update/<string:id>', methods = ['POST'])
def edit_update_products(id):
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        amount = request.form['amount']
        description = request.form['description']
        ctl_status = request.form['id_ctl_status']
        ctl_measured = request.form['id_ctl_measured_units']
        ctl_types_products = request.form['id_ctl_types_products']
        ctl_inventory_methods = request.form['id_ctl_inventory_methods']
        ctl_product_etiquette = request.form['id_ctl_product_etiquette']
        #falta las imagenes
        consult_exe = mysql.connection.cursor()
        consult_exe.execute(""" 
        UPDATE products
        SET name = %s, amount = %s, code = %s, description = %s,id_ctl_status = %s, id_ctl_measured_units = %s,
        id_ctl_types_products = %s, id_ctl_inventory_methods = %s, id_ctl_product_etiquette = %s
        WHERE id = %s""",(name,amount,code,description,ctl_status,ctl_measured,ctl_types_products,ctl_inventory_methods,ctl_product_etiquette,id))
        mysql.connection.commit()
        return redirect(url_for('products'))

@app.route('/products/delete/<string:id>')
def delete_products(id):
    delete_consult('products WHERE id = {0}'.format(id))
    return redirect(url_for('products'))

@app.route('/products/view/table')
def view_table_products():
    return render_template('products_table.html', products = get_consult('products'))


@app.route('/products/view/detailed/<string:id>')
def view_detailed_products(id):
    return render_template('view_id_products.html', 
    products_data = get_consult('products WHERE id = {0}'.format(id))[0])


#PROVIDER
@app.route('/provider')
def provider():
    return "provider.html"

@app.route('/provider/create')
def create_provider():
    return "create provider"

@app.route('/provider/create/add', methods=['POST'])
def create_add_provider():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        mail =  request.form['mail']
        phone = request.form['phone']
        location = request.form['location']
        status = request.form['status']
        transaction = request.form['transaction']
        consult_exe = mysql.connection.cursor()
        consult_exe.execute('INSERT INTO provider (name, last_name, mail, phone, location,'+ 
                        'id_ctl_status, id_ctl_transaction_types)'+
                        'VALUES(%s,%s,%s,%s,%s,%s,%s)',
                        (name, last_name, mail, phone, location, status, transaction))
        mysql.connection.commit()
        return "create add provider"

@app.route('/provider/edit/<string:id>', methods = ['POST'])
def edit_provider(id):
    return "edit provider"

@app.route('/provider/edit/update/<string:id>', methods = ['POST'])
def update_provider(id):
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        mail =  request.form['mail']
        phone = request.form['phone']
        location = request.form['location']
        status = request.form['status']
        transaction = request.form['transaction']
        consult_exe = mysql.connection.cursor()
        consult_exe.execute('INSERT INTO provider (name, last_name, mail, phone, location,'+ 
                        'id_ctl_status, id_ctl_transaction_types)'+
                        'VALUES(%s,%s,%s,%s,%s,%s,%s)',
                        (name, last_name, mail, phone, location, status, transaction))
        mysql.connection.commit()
        return "update provider"

@app.route('/provider/delete/<string:id>')
def delete_provider(id):
    delete_consult('provider WHERE id = {0}'.format(id))
    return "delete provider"


def get_consult(writing):
    consult_exe = mysql.connection.cursor()
    consult_exe.execute(f'SELECT * FROM {writing}')
    data = consult_exe.fetchall()
    mysql.connection.commit()
    return data

def delete_consult(writing):
    consult_exe = mysql.connection.cursor()
    consult_exe.execute(f'DELETE FROM {writing}')
    mysql.connection.commit()

if __name__ == "__main__":
    app.run(debug=True)

