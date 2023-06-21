from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from app.models import db
from .models import User

# Crea una instancia de Blueprint
routes = Blueprint('routes', __name__)

# Define las rutas dentro del Blueprint

@routes.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        role = session.get('role')
        if role == 'administrador':
            return redirect(url_for('routes.admin_dashboard'))
        elif role == 'vendedor':
            return redirect(url_for('routes.vendedor_dashboard'))
        else:
            abort(403)  # Acceso no autorizado

    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form.get('username')
        password = request.form.get('password')

        # Verificar las credenciales del usuario en la base de datos
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # Guardar el usuario en la sesión
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role

            # Redireccionar según el rol del usuario
            if user.role == 'administrador':
                return redirect(url_for('routes.admin_dashboard'))
            elif user.role == 'vendedor':
                return redirect(url_for('routes.vendedor_dashboard'))
            else:
                abort(403)  # Acceso no autorizado

        error_message = 'Credenciales inválidas. Inténtalo nuevamente.'
        return render_template('index.html', error_message=error_message)

    return render_template('index.html')


# Ruta de logout
@routes.route('/logout')
def logout():
    # Limpiar la sesión
    session.clear()
    return redirect(url_for('routes.index'))

# Ruta del panel de control del administrador
@routes.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' in session and session['role'] == 'administrador':
        # Lógica del panel de control del administrador...
        return render_template('admin/dashboard.html')
    else:
        abort(403)  # Acceso no autorizado

# Ruta del panel de control del vendedor
@routes.route('/vendedor/dashboard')
def vendedor_dashboard():
    if 'user_id' in session and session['role'] == 'vendedor':
        # Lógica del panel de control del vendedor...
        return render_template('admin/vendedor-dashboard.html')
    else:
        abort(403)  # Acceso no autorizado

# Ruta para crear un usuario
@routes.route('/admin/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if 'user_id' in session and session['role'] == 'administrador':
        if request.method == 'POST':
            # Obtener los datos del formulario
            username = request.form.get('username')
            password = request.form.get('password')
            perfil = request.form.get('perfil')
            max_money = request.form.get('maxMoney')
            max_sale = request.form.get('maxSale')
            max_cash = request.form.get('maxCash')
            max_pays = request.form.get('maxPays')
            max_loan = request.form.get('maxLoan')
            borrar_ventas = request.form.get('borrarVentas')
            modificar_pagos = request.form.get('modificarPagos')
            comition = request.form.get('comition')
            def_value = request.form.get('defValue')

            # Verificar que el perfil sea uno de los valores permitidos
            if perfil not in ['administrador', 'vendedor', 'cliente']:
                return "Perfil inválido"

            # Corregir el valor de modificar_pagos
            modificar_pagos = modificar_pagos == 'True'

            # Crear un nuevo usuario en la base de datos
            usuario = User(username=username, password=password, role=perfil)

            # Establecer los demás atributos del usuario
            usuario.max_money = max_money
            usuario.max_sale = max_sale
            usuario.max_cash = max_cash
            usuario.max_pays = max_pays
            usuario.max_loan = max_loan
            usuario.borrar_ventas = borrar_ventas
            usuario.modificar_pagos = modificar_pagos
            usuario.comition = comition
            usuario.def_value = def_value

            # Guardar el usuario en la base de datos
            db.session.add(usuario)
            db.session.commit()

            return redirect(url_for('routes.admin_dashboard'))

        return render_template('admin/crear_usuario.html')
    else:
        abort(403)  # Acceso no autorizado
        
# Ruta para editar un usuario
@routes.route('/admin/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):
    if 'user_id' in session and session['role'] == 'administrador':
        usuario = User.query.get(user_id)
        
        if request.method == 'POST':
            # Obtener los datos del formulario
            username = request.form.get('username')
            perfil = request.form.get('perfil')
            
            # Actualizar los atributos del usuario
            usuario.username = username
            usuario.role = perfil
            
            # Guardar los cambios en la base de datos
            db.session.commit()
            
            return redirect(url_for('routes.admin_usuarios'))
        
        return render_template('admin/editar_usuario.html', usuario=usuario)
    else:
        abort(403)  # Acceso no autorizado

# Ruta para eliminar un usuario
@routes.route('/admin/eliminar_usuario/<int:user_id>', methods=['POST'])
def eliminar_usuario(user_id):
    if 'user_id' in session and session['role'] == 'administrador':
        usuario = User.query.get(user_id)
        
        # Eliminar el usuario de la base de datos
        db.session.delete(usuario)
        db.session.commit()
        
        return redirect(url_for('routes.admin_usuarios'))
    else:
        abort(403)  # Acceso no autorizado
        
# Ruta para mostrar la lista de usuarios
@routes.route('/admin/usuarios', methods=['GET'])
def admin_usuarios():
    if 'user_id' in session and session['role'] == 'administrador':
        # Obtener la lista de usuarios desde la base de datos
        users = User.query.all()
        
        return render_template('admin/admin_usuarios.html', users=users)
    else:
        abort(403)  # Acceso no autorizado
