from wtforms import FloatField, Form, RadioField, SelectMultipleField, SubmitField
from flask_wtf import FlaskForm
 
from wtforms import StringField,IntegerField
from wtforms import EmailField
from wtforms import validators
from wtforms.fields import PasswordField
 
class UserForm(Form):
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un nombre válido')
    ])

    direccion = StringField('Dirección', [
        validators.DataRequired(message='El campo es requerido')
    ])

    telefono = StringField('Teléfono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=10, max=15, message='Número de teléfono inválido')
    ])

    submit = SubmitField('Registrar Cliente')

class PedidoForm(Form):
    tamaño = StringField('Tamaño', choices=[
        ('Chica', 'Chica'),
        ('Mediana', 'Mediana'),
        ('Grande', 'Grande')
    ], validators=[validators.DataRequired(message='Selecciona un tamaño')])

    ingredientes = StringField('Ingredientes', [
        validators.DataRequired(message='El campo es requerido')
    ])

    cantidad = IntegerField('Número de Pizzas', [
        validators.DataRequired(message='Ingresa una cantidad'),
        validators.NumberRange(min=1, message='Debe ser al menos 1')
    ])

    submit = SubmitField('Agregar Pizza')
    

class VentaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[validators.DataRequired()])
    direccion = StringField('Dirección', validators=[validators.DataRequired()])
    telefono = StringField('Teléfono', validators=[validators.DataRequired()])
    size = RadioField('Tamaño', choices=[('chica', 'Chica $40'), ('mediana', 'Mediana $80'), ('grande', 'Grande $120')], validators=[validators.DataRequired()])
    ingredientes = SelectMultipleField('Ingredientes', choices=[('jamon', 'Jamón $10'), ('piña', 'Piña $10'), ('champiñones', 'Champiñones $10')])
    num_pizzas = IntegerField('Número de Pizzas', validators=[validators.DataRequired()])
    submit = SubmitField('Realizar Pedido')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=4, max=20)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=4, max=20)])