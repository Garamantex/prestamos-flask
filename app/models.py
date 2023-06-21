from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum('administrador', 'vendedor', 'cliente'), nullable=False)
    max_money = db.Column(db.Float)
    max_sale = db.Column(db.Float)
    max_cash = db.Column(db.Float)
    max_pays = db.Column(db.Integer)
    max_loan = db.Column(db.Float)
    borrar_ventas = db.Column(db.Boolean)
    modificar_pagos = db.Column(db.Boolean)
    comition = db.Column(db.Float)
    def_value = db.Column(db.Float)
    