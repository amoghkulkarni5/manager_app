from flask import Blueprint, render_template, flash, request
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


@main.route('/actions')
@login_required
def actions():
    return render_template('actions.html')


@main.route('/stop-manager')  # A button that terminates all the workers and then stops the manager itself
@login_required
def stop_manager():
    flash("Terminate all workers and stop manager then redirect here")
    return render_template('actions.html')


@main.route('/destroy-app-data')  # A button to delete application data stored on the database as well as all images stored on S3
@login_required
def destroy_app_data():
    flash("Delete application data on RDS and S3 then redirect here")
    return render_template('actions.html')


@main.route('/add-worker')  # A button that adds EC2 instance
@login_required
def add_worker():
    flash("Create worker then redirect here")
    return render_template('load_balancer.html')


@main.route('/remove-worker', methods=['POST'])  # A button that adds EC2 instance
@login_required
def remove_worker():
    instance_id = request.form['instance_id']
    flash(f"Remove worker {instance_id} then redirect here")
    return render_template('load_balancer.html')

