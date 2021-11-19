from flask import Blueprint, render_template
from . import db
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/load-balancer')
@login_required
def load_balancer():
    return render_template('load_balancer.html')