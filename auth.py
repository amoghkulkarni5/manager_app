from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from flask_login import login_user
from flask_login import login_user, logout_user, login_required, current_user
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        if not user or not user.password == password:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        flash("Login successful")
        return redirect(url_for('main.dashboard'))

    if current_user.is_authenticated:
        flash(f"You are already logged in as {current_user.name}!")
        return render_template('dashboard.html')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))