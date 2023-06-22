import datetime

from app import db


class User(db.Model):
    """ Modelo de Usuario

    Esta clase representa un modelo de Usuario en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum('administrador', 'vendedor', 'cliente'), nullable=False)
    first_name = db.Column(db.String(30), nullable=False, doc='Nombre')
    last_name = db.Column(db.String(30), nullable=False, doc='Apellido')
    email = db.Column(db.String(120), unique=True, nullable=False, doc='Correo electrónico')
    document = db.Column(db.String(20), unique=True, nullable=False, doc='Documento')
    address = db.Column(db.String(100), nullable=False, doc='Dirección')
    cellphone = db.Column(db.String(20), nullable=False, doc='Celular')
    status_id = db.Column(db.Integer, db.ForeignKey('user_status.id'), nullable=False)
    is_staff = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    modification_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow,
                                  onupdate=datetime.datetime.utcnow)

    user_status = db.relationship('UserStatus')

    def __str__(self):
        """ Representación en forma de cadena del modelo de Usuario."""
        return f"{self.first_name} {self.last_name}"


class UserStatus(db.Model):
    """ Modelo de Estado de Usuario """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        """ Representación en forma de cadena del modelo de Estado de Usuario."""
        return self.name


class Manager(db.Model):
    """ Modelo de Gerente """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True, doc='Usuario')
    maximum_cash = db.Column(db.Numeric(10, 2), nullable=False, doc='Máxima caja')
    maximum_sale = db.Column(db.Numeric(10, 2), nullable=False, doc='Máxima venta')
    maximum_expense = db.Column(db.Numeric(10, 2), nullable=False, doc='Límite gasto')
    maximum_payment = db.Column(db.Numeric(10, 2), nullable=False, doc='Máximo pago')
    minimum_interest = db.Column(db.Numeric(10, 2), nullable=False, doc='Mínimo interés')
    percentage_interest = db.Column(db.Numeric(10, 2), nullable=False, doc='Porcentaje interés')
    fix_value = db.Column(db.Numeric(10, 2), nullable=False, doc='Valor fijo')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    modification_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow,
                                  onupdate=datetime.datetime.utcnow)

    user = db.relationship('User', backref='manager')

    def __str__(self):
        """ Representación en forma de cadena del modelo de Gerente."""
        return f"{self.user.first_name} {self.user.last_name}"


class Salesman(db.Model):
    """ Modelo de Vendedor """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True, doc='Usuario')
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False, doc='Coordinador')
    maximum_cash = db.Column(db.Numeric(10, 2), nullable=False, doc='Monto máximo de caja')
    maximum_sale = db.Column(db.Numeric(10, 2), nullable=False, doc='Monto máximo del préstamo')
    maximum_expense = db.Column(db.Numeric(10, 2), nullable=False, doc='Monto máximo de gastos')
    maximum_payment = db.Column(db.Numeric(10, 2), nullable=False, doc='Monto máximo de pago')
    minimum_interest = db.Column(db.Numeric(10, 2), nullable=False, doc='Monto mínimo de interés')
    percentage_interest = db.Column(db.Numeric(10, 2), nullable=False, doc='Porcentaje de interés')
    fix_value = db.Column(db.Numeric(10, 2), nullable=False, doc='Valor fijo de interés')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    modification_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow,
                                  onupdate=datetime.datetime.utcnow)

    user = db.relationship('User', backref='salesman', uselist=False)
    manager = db.relationship('Manager')

    def __str__(self):
        """ Representación en forma de cadena del modelo de Vendedor."""
        return f"{self.user.first_name} {self.user.last_name}"


class Client(db.Model):
    """ Modelo de Cliente. """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # TODO: ajustar la relación en el modelo prestamo
    # salesman_id = db.Column(db.Integer, db.ForeignKey('salesman.id'), nullable=False)
    # loan = db.Column(db.Numeric(10, 2), nullable=False, doc='Préstamo')
    # interest = db.Column(db.Numeric(10, 2), nullable=False, doc='Interés')
    # number_of_payments = db.Column(db.Integer, nullable=False, doc='Número de pagos')
    # deadline_id = db.Column(db.Integer, db.ForeignKey('deadlines.id'), nullable=False, doc='Plazo')
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    modification_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow,
                                  onupdate=datetime.datetime.utcnow)

    user = db.relationship('User', backref='client')
    salesman = db.relationship('Salesman', backref='client')
    deadline = db.relationship('Deadlines', backref='client')

    def __str__(self):
        """ Representación en forma de cadena del modelo de Cliente. """
        return f"{self.user.first_name} {self.user.last_name} Atendido por {self.salesman.first_name} {self.salesman.last_name}"
