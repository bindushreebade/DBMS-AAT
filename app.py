from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}


# Create database tables
with app.app_context():
    db.create_all()


# Add new product
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")

    if not name or price is None:
        return jsonify({"error": "Missing product details"}), 400

    new_product = Product(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "message": "Product added",
        "product": new_product.to_dict()
    }), 201


# List all products
@app.route('/list_products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200


# Update product price
@app.route('/update_product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    new_price = data.get("price")

    if new_price is None:
        return jsonify({"error": "New price required"}), 400

    product.price = new_price
    db.session.commit()

    return jsonify({
        "message": "Product updated",
        "product": product.to_dict()
    }), 200


# Apply discount to all products
@app.route('/apply_discount', methods=['POST'])
def apply_discount():
    data = request.get_json()
    discount_percentage = data.get("discount")

    if discount_percentage is None or discount_percentage < 0 or discount_percentage > 100:
        return jsonify({"error": "Invalid discount percentage"}), 400

    products = Product.query.all()
    for product in products:
        product.price -= product.price * (discount_percentage / 100)

    db.session.commit()

    return jsonify({
        "message":
        f"{discount_percentage}% discount applied to all products"
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
