import os
from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
from flask import request, redirect, url_for
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://products:Hello!123@ds047387.mlab.com:47387/construction-products?retryWrites=false"
mongo = PyMongo(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add_products")
def add_products():
    products = mongo.db.products.find()
    counties = mongo.db.county.find()

    return render_template("add_products.html", products=products, counties=counties)

@app.route("/select_products", methods=['POST'])
def select_products():
    county_id = request.form.get("county")
    product_id = request.form.get("product")

    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    diameters = mongo.db.diameters.find({'county_id': county_id})

    return render_template("add_product.html", product=product, diameters=diameters, county_id=county_id)

@app.route("/add_product", methods=['POST'])
def add_product():
    product_id = request.form.get("product_id")
    product_name = request.form.get("name")
    quantity = request.form.get("quantity")
    length = request.form.get("length")
    diameter = request.form.get("diameter")
    county_id = request.form.get("county_id")

    product = {
        "name": product_name,
        "product_id": product_id,
        "county_id": county_id,
        "quantity": quantity,
        "length": length,
        "diameter": diameter
    }

    mongo.db.products_inventory.insert_one(product)

    return redirect(url_for('home'))

@app.route("/products")
def products():
    products = mongo.db.products_inventory.find()
    return render_template("products.html", products=products)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=(os.environ.get('PORT')), debug=True)