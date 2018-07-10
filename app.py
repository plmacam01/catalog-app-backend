# -*- coding: utf-8 -*-
#!/usr/bin/python
from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api
from flask_cors import CORS
from modules.products import Products, Product
from modules.transactions import Transactions, Transaction

app = Flask(__name__)
CORS(app)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Products, '/products') # Getting and Adding products
api.add_resource(Product, '/product/<string:id>') # Editing products
api.add_resource(Transactions, '/transactions') # Getting and creating transactions
api.add_resource(Transaction, '/transaction/<string:id>') # Updating transactions

app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(port='5002')
