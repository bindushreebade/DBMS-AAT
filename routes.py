from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models import db, Product

app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        if Product.query.filter_by(name=name).first():
            return "Product already exists!"
        new_product = Product(name=name, price=price)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('app.get_products'))
    return render_template('add_product.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.price = float(request.form['price'])
        db.session.commit()
        return redirect(url_for('app.get_products'))
    return render_template('update_product.html', product=product)

@app.route('/apply_discount/<float:discount>', methods=['POST'])
def apply_discount(discount):
    products = Product.query.all()
    for product in products:
        product.price -= product.price * (discount / 100)
    db.session.commit()
    return redirect(url_for('app.get_products'))
