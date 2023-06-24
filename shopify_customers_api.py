import os
import urllib.parse
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

password = "R@vig@rg1907"
encode_password =  urllib.parse.quote_plus("R@vig@rg1907")


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://ravigarg:R%40vig%40rg1907@103.174.54.87:3306/shopifycustomers"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://ravigarg:"+encode_password+"@103.174.54.87:3306/shopifycustomers"
db = SQLAlchemy(app)

class TblCustomer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    # Add other columns for customer details (e.g., name, email, etc.)

class TblEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('tbl_customer.id'), nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    event = db.Column(db.String(50), nullable=False)

@app.route('/check_phone_number', methods=['POST'])
def check_phone_number():
    phone_number = request.json.get('phone_number')
    customer = TblCustomer.query.filter_by(phone_number=phone_number).first()
    exists = bool(customer)
    return jsonify(exists=exists)

@app.route('/register_phone_number', methods=['POST'])
def register_phone_number():
    phone_number = request.json.get('phone_number')
    # Additional data for customer registration can be obtained from request.json

    customer = TblCustomer(phone_number=phone_number)
    db.session.add(customer)
    db.session.commit()

    return jsonify(message='Phone number registered successfully')

@app.route('/record_event', methods=['POST'])
def record_event():
    customer_id = request.json.get('customer_id')
    tag = request.json.get('tag')
    url = request.json.get('url')
    event = request.json.get('event')

    event_data = TblEvent(customer_id=customer_id, tag=tag, url=url, event=event)
    db.session.add(event_data)
    db.session.commit()

    return jsonify(message='Event recorded successfully')

if __name__ == '__main__':
    app.run()
