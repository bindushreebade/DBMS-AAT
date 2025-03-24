from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample database (Dictionary to store products)
products = {}

# Function to add a new product
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    product_id = data.get("id")
    name = data.get("name")
    price = data.get("price")

    if not product_id or not name or price is None:
        return jsonify({"error": "Missing product details"}), 400

    if product_id in products:
        return jsonify({"error": "Product ID already exists"}), 400

    products[product_id] = {"name": name, "price": price}
    return jsonify({"message": "Product added successfully", "product": products[product_id]}), 201

# Function to list all products
@app.route('/list_products', methods=['GET'])
def list_products():
    return jsonify(products), 200

# Function to update product price
@app.route('/update_product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    new_price = data.get("price")

    if new_price is None:
        return jsonify({"error": "New price is required"}), 400

    products[product_id]["price"] = new_price
    return jsonify({"message": "Product updated successfully", "product": products[product_id]}), 200

# Function to apply discount to all products
@app.route('/apply_discount', methods=['POST'])
def apply_discount():
    data = request.get_json()
    discount_percentage = data.get("discount")

    if discount_percentage is None or discount_percentage < 0 or discount_percentage > 100:
        return jsonify({"error": "Invalid discount percentage"}), 400

    for product in products.values():
        product["price"] -= product["price"] * (discount_percentage / 100)

    return jsonify({"message": f"{discount_percentage}% discount applied to all products"}), 200

if __name__ == '__main__':
    app.run(debug=True)
