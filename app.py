# -*- coding: utf-8 -*-
#!/usr/bin/python
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from modules.products import Products, Product
from modules.transactions import Transactions, Transaction

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Products, '/products') # Getting and Adding products
api.add_resource(Product, '/product/<string:id>') # Editing products
api.add_resource(Transactions, '/transactions') # Getting and creating transactions
api.add_resource(Transaction, '/transaction/<string:id>') # Updating transactions

if __name__ == '__main__':
    app.run(debug=True)
    app.run(port='5002')
