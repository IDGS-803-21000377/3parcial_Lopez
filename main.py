from datetime import date
from hashlib import scrypt
import os
from flask import Flask, flash, json, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_manager, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import func
from wtforms.fields import datetime
from models import Pedidos, User, Venta, db, Cliente
from config import DevelomentConfig
import forms
from flask import redirect, url_for, flash

app = Flask(__name__)
app.config.from_object(DevelomentConfig)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.login_view = 'login'  
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    

@app.route('/index')
@login_required  
def index():
    ventas = Venta.query.all()
    return render_template("index.html", ventas=ventas)

@app.route('/')
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = forms.LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=form.username.data).first()
        if user:
          login_user(user)
        else:
         print("Usuario no encontrado")   

        if user and user.password == password:  
            login_user(user)  
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('index'))  

        else:
            flash("Usuario o contraseña incorrectos", "danger")
            print(user)

    return render_template('login.html', form=form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('login'))
@app.route('/ventas')
def detalles_venta():
    ventas = Venta.query.all()
    return render_template("index.html", ventas=ventas)



@app.route('/pedido', methods=['GET', 'POST'])
def pedido():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        size = request.form['size']
        ingredientes = request.form.getlist('ingredientes')
        num_pizzas = int(request.form['num_pizzas'])

        cliente = Cliente.query.filter_by(nombre=nombre, telefono=telefono).first()
        if not cliente:
            cliente = Cliente(nombre=nombre, direccion=direccion, telefono=telefono)
            db.session.add(cliente)
            db.session.commit()

        nuevo_pedido = Pedidos(idCliente=cliente.idCliente, estado="Pendiente")
        db.session.add(nuevo_pedido)
        db.session.commit()

        precios = {"chica": 40, "mediana": 80, "grande": 120}
        precio_unitario = precios.get(size, 40)
        precio_ingrediente = 10
        subtotal = (precio_unitario + (precio_ingrediente * len(ingredientes))) * num_pizzas

        nueva_venta = Venta(
            idPedido=nuevo_pedido.idPedido,
            montoTotal=subtotal,
            size=size,
            ingredientes=", ".join(ingredientes),
            num_pizzas=num_pizzas,
            subtotal=subtotal
        )
        db.session.add(nueva_venta)
        db.session.commit()

        flash(f"Pedido agregado correctamente. Total: ${subtotal:.2f}", "success")
        return redirect(url_for('detalles_venta'))

    return render_template('index.html')



@app.route('/quitar_pedido/<int:id_venta>', methods=['POST'])
def quitar_pedido(id_venta):
    venta = Venta.query.get(id_venta)
    if venta:
        with open('pizzas_eliminadas.txt', 'a') as file:
            file.write(json.dumps({
                "idVenta": venta.idVenta,
                "size": venta.size,
                "ingredientes": venta.ingredientes,
                "num_pizzas": venta.num_pizzas,
                "subtotal": venta.subtotal
            }) + '\n')
        
        db.session.delete(venta)
        db.session.commit()
        
        flash("Producto eliminado correctamente", "success")
    else:
        flash("Producto no encontrado", "danger")

    return redirect(url_for('detalles_venta'))

@app.route('/terminar_pedido', methods=['POST'])
def terminar_pedido():
    if not os.path.exists('pizzas_eliminadas.txt'):
        flash("No hay pedidos eliminados.", "danger")
        return redirect(url_for('detalles_venta'))

    total = 0
    with open('pizzas_eliminadas.txt', 'r') as file:
        for line in file:
            pizza_data = json.loads(line)  
            total += pizza_data['subtotal']  

    flash(f"El costo total de los pedidos eliminados es: ${total:.2f}", "success")
    return redirect(url_for('detalles_venta'))

@app.route("/ventas_totales", methods=["POST"])
def ventas_totales():
    create_form = forms.UserForm(request.form)

    try:
        hoy = date.today()  
        pedidos = Pedidos.query.filter(db.func.date(Pedidos.fechaPedido) == hoy).all()

        total = 0
        ventas_por_cliente = []

        for pedido in pedidos:
            if pedido.ventas:
                subtotal = sum(venta.montoTotal for venta in pedido.ventas)
                total += subtotal
                ventas_por_cliente.append({
                    'cliente': pedido.cliente.nombre,
                    'subtotal': subtotal
                })

        mensaje_ventas = f"${total:.2f}" if total > 0 else "$0.00"

        flash({'ventas_totales': mensaje_ventas, 'ventas_por_cliente': ventas_por_cliente}, 'success')

        return redirect(url_for('index'))  

    except Exception as e:
        flash({'mensaje_error': f"Error al obtener ventas totales: {str(e)}"}, 'error')
        return redirect(url_for('index'))



if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()  
    app.run(debug=True)
