from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

from project.models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # Chequear datos de login
        if not user or not check_password_hash(user.password, password):
            flash('Por favor verifique sus datos de login')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    else:
        return render_template('login.html')

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # Busca user en db 
        
        if user: # Usuario existe, vuelve a signup
            flash('Ya existe un usuario registrado con ese nombre')
            return redirect(url_for('auth.login'))

        # Creacion usuario
        new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'))

        # Agrego user a la db
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    
    else:
        return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))