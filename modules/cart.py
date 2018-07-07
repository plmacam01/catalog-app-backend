from helpers.models import CartTbl, CartProducts
from db import session

from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.ext.serializer import loads, dumps
from flask import jsonify, request
from json import dumps
from flask_restful import Resource, Api


class Cart(Resource):
    def get(self):
        d_result = {}

        qry_cart = session.query(CartTbl).first()

# session.query(User, Address).join('addresses')
        # list_carts = []
        # for cart in qry_cart:
        #     d_cart = {
        #         'id': product.id,
        #         'name': product.name,
        #         'total': str(product.total)
        #     }
        #     list_carts.append(d_cart)

        d_result.update({'data': qry_cart})

        return d_result, {'Content-Type': 'application/json; character=utf-8'}
    def post(self):
        data = request.get_json();

        req = ProductsTbl(name=data['name'], status=data['status'], price=data['price'], stock=data['stock'])

        session.add(req)
        session.commit()

        return "ok", 201
class Cart_Products(Resource):
    def put(self, id):
        data = request.get_json();

        d_product = {
            'name': data['name'],
            'status': data['status'],
            'stock': data['stock'],
            'price': str(data['price'])
        }

        session.query(ProductsTbl).filter(ProductsTbl.id == id).update(d_product)
        session.commit()

        return "ok", 201
    def delete(self, id):

        session.query(ProductsTbl).filter(ProductsTbl.id == id).delete()
        session.commit()
        return "ok", 201
