import sys
import os
# Add the parent directory to sys.path so that "src" is found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import pytest
from src.app import create_app  # Removed "db" import
from src import models

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        models.db.create_all()  # Use models.db instance
        yield app
        models.db.drop_all()    # Use models.db instance

@pytest.fixture
def client(app):
    return app.test_client()

# Helper to post a user; required for endpoints with foreign keys.
def create_test_user(client):
    data = {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone": "123456789",
        "credentials": 0,
        "password": "secret"
    }
    resp = client.post('/users', data=json.dumps(data), content_type='application/json')
    return json.loads(resp.data)

def test_users_endpoints(client):
    # GET users (should be empty)
    resp = client.get('/users')
    assert resp.status_code == 200
    assert json.loads(resp.data) == []
    
    # POST user
    user_data = {
        "username": "testuser2",
        "first_name": "Test",
        "last_name": "User2",
        "email": "test2@example.com",
        "phone": "987654321",
        "credentials": 0,
        "password": "secret"
    }
    resp = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    assert resp.status_code == 201
    created = json.loads(resp.data)
    user_id = created["user_id"]
    
    # GET single user
    resp = client.get(f'/users/{user_id}')
    assert resp.status_code == 200

    # PUT update user
    update_data = {"first_name": "Updated"}
    resp = client.put(f'/users/{user_id}', data=json.dumps(update_data), content_type='application/json')
    assert resp.status_code == 200
    updated = json.loads(resp.data)
    assert updated["first_name"] == "Updated"
    
    # DELETE user
    resp = client.delete(f'/users/{user_id}')
    assert resp.status_code == 200

def test_beers_endpoints(client):
    # GET beers (empty)
    resp = client.get('/beers')
    assert resp.status_code == 200
    assert json.loads(resp.data) == []

    # POST beer
    beer_data = {
        "nr": "001",
        "articleid": "A1",
        "articletype": "lager",
        "name": "Cool Beer",
        "priceinclvat": 59.99,
        "volumeml": 500
    }
    resp = client.post('/beers', data=json.dumps(beer_data), content_type='application/json')
    assert resp.status_code == 201
    created = json.loads(resp.data)
    beer_id = created["beer_id"]

    # GET beer detail
    resp = client.get(f'/beers/{beer_id}')
    assert resp.status_code == 200

def test_orders_endpoints(client):
    # Orders depend on a user.
    user = create_test_user(client)
    user_id = user["user_id"]
    
    # GET orders (empty)
    resp = client.get('/orders')
    assert resp.status_code == 200
    assert json.loads(resp.data) == []

    # POST order
    order_data = {"user_id": user_id, "status": "pending"}
    resp = client.post('/orders', data=json.dumps(order_data), content_type='application/json')
    assert resp.status_code == 201
    order = json.loads(resp.data)
    order_id = order["order_id"]

    # GET order detail
    resp = client.get(f'/orders/{order_id}')
    assert resp.status_code == 200

    # PUT update order
    update_order = {"status": "completed"}
    resp = client.put(f'/orders/{order_id}', data=json.dumps(update_order), content_type='application/json')
    assert resp.status_code == 200

    # DELETE order
    resp = client.delete(f'/orders/{order_id}')
    assert resp.status_code == 200

def test_order_items_endpoints(client):
    # Create user and order
    user = create_test_user(client)
    order_resp = client.post('/orders', data=json.dumps({"user_id": user["user_id"]}), content_type='application/json')
    order = json.loads(order_resp.data)
    order_id = order["order_id"]
    
    # GET order items (empty)
    resp = client.get(f'/orders/{order_id}/items')
    assert resp.status_code == 200
    assert json.loads(resp.data) == []

    # Ensure a beer exists.
    beer_data = {"nr": "002", "articleid": "A2", "articletype": "ale", "name": "Test Ale", "priceinclvat": 45.50}
    beer_resp = client.post('/beers', data=json.dumps(beer_data), content_type='application/json')
    beer = json.loads(beer_resp.data)
    
    # POST an order item
    item_data = {
        "beer_id": beer["beer_id"],
        "quantity": 2,
        "price": 45.50
    }
    resp = client.post(f'/orders/{order_id}/items', data=json.dumps(item_data), content_type='application/json')
    assert resp.status_code == 201
    item = json.loads(resp.data)
    assert item["quantity"] == 2

def test_payments_endpoints(client):
    # Create a user for payment and an admin (using same created user for simplicity)
    user = create_test_user(client)
    
    # GET payments (empty)
    resp = client.get('/payments')
    assert resp.status_code == 200
    assert json.loads(resp.data) == []

    # POST payment
    payment_data = {
        "user_id": user["user_id"],
        "admin_id": user["user_id"],
        "amount": 100.00
    }
    resp = client.post('/payments', data=json.dumps(payment_data), content_type='application/json')
    assert resp.status_code == 201
    payment = json.loads(resp.data)
    transaction_id = payment["transaction_id"]

    # GET payment detail
    resp = client.get(f'/payments/{transaction_id}')
    assert resp.status_code == 200

def test_beers_sold_endpoints(client):
    # Create user and beer for beers_sold
    user = create_test_user(client)
    beer_data = {"nr": "003", "articleid": "A3", "articletype": "stout", "name": "Dark Stout", "priceinclvat": 65.00}
    beer_resp = client.post('/beers', data=json.dumps(beer_data), content_type='application/json')
    beer = json.loads(beer_resp.data)
    
    # Simulate a beer sold record directly via DB insertion
    with client.application.app_context():
        bs = models.BeerSold(user_id=user["user_id"], beer_id=beer["beer_id"])
        models.db.session.add(bs)
        models.db.session.commit()
        transaction_id = bs.transaction_id

    # GET beers_sold
    resp = client.get('/beers_sold')
    assert resp.status_code == 200

    # GET beer sold detail
    resp = client.get(f'/beers_sold/{transaction_id}')
    assert resp.status_code == 200

def test_vip_customers_endpoints(client):
    # Create user for VIP record
    user = create_test_user(client)
    
    # GET vip_customers (empty)
    resp = client.get('/vip_customers')
    assert resp.status_code == 200
    assert json.loads(resp.data) == []

    # POST vip customer
    vip_data = {"user_id": user["user_id"], "credit_limit": 1000.00}
    resp = client.post('/vip_customers', data=json.dumps(vip_data), content_type='application/json')
    assert resp.status_code == 201

    # GET vip customer detail
    resp = client.get(f'/vip_customers/{user["user_id"]}')
    assert resp.status_code == 200
