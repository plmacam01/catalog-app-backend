from helpers.models import ProductStatus, ProductsTbl
from db import session

from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.ext.serializer import loads, dumps
from flask import jsonify, request
from json import dumps
from flask_restful import Resource, Api
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# db_connect = create_engine('postgresql+psycopg2:///catalog')
# database = 'catalog'
#
# import psycopg2
# myConnection = psycopg2.connect( dbname=database )

class Products(Resource):
    def get(self):
        d_result = {}

        qry_products = session.query(ProductsTbl).join(ProductsTbl.status).order_by(ProductsTbl.id.asc()).all()

# session.query(User, Address).join('addresses')
        list_products = []
        for product in qry_products:
            d_product = {
                'id': product.id,
                'name': product.name,
                'status': product.status.name,
                'price': str(product.price),
                'stock': product.stock
            }
            list_products.append(d_product)

        d_result.update({'data': list_products})

        return d_result, {'Content-Type': 'application/json; character=utf-8'}
    def post(self):
        data = request.get_json();
        req = ProductsTbl(name=data['name'], status_id=data['status'], price=data['price'], stock=data['stock']);

        session.add(req)
        session.commit()

        return "ok", 201
class Product(Resource):
    def put(self, id):
        data = request.get_json();

        d_product = {
            'name': data['name'],
            'status_id': data['status'],
            'price': str(data['price']),
            'stock': data['stock']
        }

        session.query(ProductsTbl).filter(ProductsTbl.id == id).update(d_product)
        session.commit()

        return "ok", 201
    def delete(self, id):

        session.query(ProductsTbl).filter(ProductsTbl.id == id).delete()
        session.commit()
        return "ok", 201
