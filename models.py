from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields import datetime
from config import DevelomentConfig
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import datetime

 
db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'cliente'
    idCliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    
    pedidos = db.relationship('Pedidos', backref='cliente', lazy=True)

class Pedidos(db.Model):
    __tablename__ = 'pedidos'
    idPedido = db.Column(db.Integer, primary_key=True)
    idCliente = db.Column(db.Integer, db.ForeignKey('cliente.idCliente'), nullable=False)
    fechaPedido = db.Column(db.DateTime, default=datetime.datetime.now)
    estado = db.Column(db.String(50), default="Pendiente")

    ventas = db.relationship('Venta', backref='pedido', lazy=True)

class Venta(db.Model):
    __tablename__ = 'ventas'
    idVenta = db.Column(db.Integer, primary_key=True)
    idPedido = db.Column(db.Integer, db.ForeignKey('pedidos.idPedido'), nullable=False)
    fechaVenta = db.Column(db.DateTime, default=datetime.datetime.now)
    montoTotal = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(20), nullable=False)
    ingredientes = db.Column(db.String(200), nullable=False)
    num_pizzas = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)  

class User(UserMixin, db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        """Método para establecer la contraseña"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Método para verificar la contraseña"""
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return str(self.id_user)