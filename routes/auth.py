from flask import Blueprint, request, session, redirect, url_for, render_template
from models.user import User
import sqlite3

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth')
def auth():
    return render_template('autorize.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    if not password or password != confirm:
        return "Пароли не совпадают", 400

    try:
        user = User.create(name, email, password)
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return redirect(url_for('tasks.index'))  # Изменили на tasks.index
    except sqlite3.IntegrityError:
        return "Пользователь с таким email уже существует", 400

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.get_by_email(email)
    
    if user and User.verify_password(user, password):
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return redirect(url_for('tasks.index'))  # Изменили на tasks.index
    return "Неверный email или пароль", 401

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.auth'))