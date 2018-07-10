from helpers.models import ProductStatus, ProductsTbl
from db import session

from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.ext.serializer import loads, dumps
from flask import jsonify, request
from json import dumps
from flask_restful import Resource, Api
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

class Products(Resource):
    def get(self):
        d_result = {}

        try:
            qry_products = session.query(ProductsTbl).join(ProductsTbl.status).order_by(ProductsTbl.id.asc()).all()

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

        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            return dumps(e), 400

        return d_result, {'Content-Type': 'application/json; character=utf-8'}
    def post(self):
        data = request.get_json();

        try:
            req = ProductsTbl(name=data['name'], status_id=data['status'], price=data['price'], stock=data['stock']);
        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            return dumps(e), 400

        try:
            session.add(req)
            session.commit()
        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            return dumps(e), 400

        return dumps({}), 201
class Product(Resource):
    def put(self, id):
        data = request.get_json();

        d_product = {
            'name': data['name'],
            'status_id': data['status'],
            'price': str(data['price']),
            'stock': data['stock']
        }

        try:
            session.query(ProductsTbl).filter(ProductsTbl.id == id).update(d_product)
            session.commit()
        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            return dumps(e), 400

        return dumps({}), 201
    def delete(self, id):

        session.query(ProductsTbl).filter(ProductsTbl.id == id).delete()
        session.commit()
        return dumps({}), 201
