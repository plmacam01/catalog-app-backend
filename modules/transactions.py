from helpers.models import TransactionsTbl, TransactionProducts, ProductsTbl
from db import session

from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.ext.serializer import loads, dumps
from flask import jsonify, request
from json import dumps
from flask_restful import Resource, Api
import datetime
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

now = datetime.datetime.now()

class Transactions(Resource):
    def get(self):
        d_result = {}

        try:
            qry_transactions = session.query(TransactionsTbl).join(TransactionsTbl.status).order_by(TransactionsTbl.id.asc()).all()

            list_transactions = []
            for transaction in qry_transactions:
                qry_products = session.query(TransactionProducts).join(TransactionProducts.product).filter(TransactionProducts.transaction_id == transaction.id).order_by(TransactionProducts.id.asc()).all()
                list_products = []
                for product in qry_products:
                    d_product = {
                        'name' : product.product.name,
                        'price' : str(product.product.price),
                        'amount' : product.amount
                    }
                    list_products.append(d_product)
                d_transact = {
                    'id': transaction.id,
                    'status': transaction.status.name,
                    'date_created': str(transaction.date_created),
                    'date_shipped': str(transaction.date_shipped),
                    'date_arrived': str(transaction.date_arrived),
                    'products': list_products,
                    'total': str(transaction.total)
                }
                list_transactions.append(d_transact)
                d_result.update({'data': list_transactions})
        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            return dumps(e), 400

        return d_result, {'Content-Type': 'application/json; character=utf-8'}
    def post(self):
        data = request.get_json();

        try:
            qry_transactions = session.query(TransactionsTbl).join(TransactionsTbl.status).order_by(TransactionsTbl.id.asc()).all()

            list_transactions = []
            for transaction in qry_transactions:
                new_transaction = TransactionsTbl(status_id=1, date_created=now)
                session.add(new_transaction)
                session.flush()

                session.refresh(new_transaction)

                products = [];
                total = 0;
                for product in data['products']:
                    qry_products = session.query(ProductsTbl).filter(ProductsTbl.id == product['id']).first()
                    total += product['amount']*qry_products.price
                    products.append(TransactionProducts(transaction_id=new_transaction.id, product_id=product['id'], amount=product['amount']))
                    new_stock = qry_products.stock - product['amount'];
                    session.query(ProductsTbl).filter(ProductsTbl.id == product['id']).update({'stock': new_stock})

                session.bulk_save_objects(products)
                session.query(TransactionsTbl).filter(TransactionsTbl.id == new_transaction.id).update({'total': float(total)})
                session.commit()

        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            return dumps(e), 400

        return dumps({}), 201
class Transaction(Resource):
    def put(self, id):
        data = request.get_json();

        try:
            d_trasaction = {
                'status_id': data['status']
            }
            if data['status'] == 2:
                d_trasaction['date_shipped'] = now
            elif data['status'] == 3:
                d_trasaction['date_arrived'] = now
            session.query(TransactionsTbl).filter(TransactionsTbl.id == id).update(d_trasaction)
            session.commit()

        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            return dumps(e), 400

        return dumps({}), 201
    def delete(self, id):

        try:
            session.query(ProductsTbl).filter(ProductsTbl.id == id).delete()
            session.commit()

        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            return dumps(e), 400
        return dumps({}), 201
