import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src import models  # import models (e.g., User, Beer) for later use if needed

db = SQLAlchemy()

def serialize(instance):
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config')

    models.db.init_app(app)
    Migrate(app, models.db)

    # Users endpoints
    @app.route('/users', methods=['GET', 'POST'])
    def users():
        if request.method == 'GET':
            users = models.User.query.all()
            return jsonify([serialize(u) for u in users]), 200
        else:  # POST
            data = request.get_json()
            user = models.User(**data)
            models.db.session.add(user)
            models.db.session.commit()
            return jsonify(serialize(user)), 201

    @app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
    def user_detail(user_id):
        user = models.User.query.get_or_404(user_id)
        if request.method == 'GET':
            return jsonify(serialize(user)), 200
        elif request.method == 'PUT':
            data = request.get_json()
            for key, value in data.items():
                setattr(user, key, value)
            models.db.session.commit()
            return jsonify(serialize(user)), 200
        else:  # DELETE
            models.db.session.delete(user)
            models.db.session.commit()
            return jsonify({'message': 'User deleted'}), 200

    # Beers endpoints
    @app.route('/beers', methods=['GET', 'POST'])
    def beers():
        if request.method == 'GET':
            beers = models.Beer.query.all()
            return jsonify([serialize(b) for b in beers]), 200
        else:  # POST
            data = request.get_json()
            beer = models.Beer(**data)
            models.db.session.add(beer)
            models.db.session.commit()
            return jsonify(serialize(beer)), 201

    @app.route('/beers/<int:beer_id>', methods=['GET'])
    def beer_detail(beer_id):
        beer = models.Beer.query.get_or_404(beer_id)
        return jsonify(serialize(beer)), 200

    # Orders endpoints
    @app.route('/orders', methods=['GET', 'POST'])
    def orders():
        if request.method == 'GET':
            orders = models.Order.query.all()
            return jsonify([serialize(o) for o in orders]), 200
        else:  # POST
            data = request.get_json()
            order = models.Order(
                user_id=data.get('user_id'),
                status=data.get('status', 'pending')
            )
            models.db.session.add(order)
            models.db.session.commit()
            return jsonify(serialize(order)), 201

    @app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
    def order_detail(order_id):
        order = models.Order.query.get_or_404(order_id)
        if request.method == 'GET':
            return jsonify(serialize(order)), 200
        elif request.method == 'PUT':
            data = request.get_json()
            for key, value in data.items():
                setattr(order, key, value)
            models.db.session.commit()
            return jsonify(serialize(order)), 200
        else:  # DELETE
            models.db.session.delete(order)
            models.db.session.commit()
            return jsonify({'message': 'Order deleted'}), 200

    # Order Items endpoints
    @app.route('/orders/<int:order_id>/items', methods=['GET', 'POST'])
    def order_items(order_id):
        # Ensure order exists
        models.Order.query.get_or_404(order_id)
        if request.method == 'GET':
            items = models.OrderItem.query.filter_by(order_id=order_id).all()
            return jsonify([serialize(item) for item in items]), 200
        else:  # POST
            data = request.get_json()
            item = models.OrderItem(order_id=order_id, **data)
            models.db.session.add(item)
            models.db.session.commit()
            return jsonify(serialize(item)), 201

    # Payments endpoints
    @app.route('/payments', methods=['GET', 'POST'])
    def payments():
        if request.method == 'GET':
            payments = models.Payment.query.all()
            return jsonify([serialize(p) for p in payments]), 200
        else:  # POST
            data = request.get_json()
            payment = models.Payment(**data)
            models.db.session.add(payment)
            models.db.session.commit()
            return jsonify(serialize(payment)), 201

    @app.route('/payments/<int:transaction_id>', methods=['GET'])
    def payment_detail(transaction_id):
        payment = models.Payment.query.get_or_404(transaction_id)
        return jsonify(serialize(payment)), 200

    # Beer Sold endpoints
    @app.route('/beers_sold', methods=['GET'])
    def beers_sold():
        beers_sold = models.BeerSold.query.all()
        return jsonify([serialize(bs) for bs in beers_sold]), 200

    @app.route('/beers_sold/<int:transaction_id>', methods=['GET'])
    def beer_sold_detail(transaction_id):
        beer_sold = models.BeerSold.query.get_or_404(transaction_id)
        return jsonify(serialize(beer_sold)), 200

    # VIP Customers endpoints
    @app.route('/vip_customers', methods=['GET', 'POST'])
    def vip_customers():
        if request.method == 'GET':
            vip_list = models.VipCustomer.query.all()
            return jsonify([serialize(v) for v in vip_list]), 200
        else:  # POST
            data = request.get_json()
            vip = models.VipCustomer(**data)
            models.db.session.add(vip)
            models.db.session.commit()
            return jsonify(serialize(vip)), 201

    @app.route('/vip_customers/<int:user_id>', methods=['GET'])
    def vip_customer_detail(user_id):
        vip = models.VipCustomer.query.get_or_404(user_id)
        return jsonify(serialize(vip)), 200

    return app