from flask import Blueprint, render_template, flash, request
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from .models import Configuration

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


@main.route('/configuration', methods=['GET', 'POST'])  # Modify configuration variables
@login_required
def configuration():
    if request.method == 'POST':
        grow_cpu_threshold = request.form.get('grow_cpu_threshold')
        shrink_cpu_threshold = request.form.get('shrink_cpu_threshold')
        grow_ratio = request.form.get('grow_ratio')
        shrink_ratio = request.form.get('shrink_ratio')
        config = Configuration.query.all()[0]

        if (grow_cpu_threshold == "") or (shrink_cpu_threshold == "") or (grow_ratio == "") or (shrink_ratio == ""):
            flash("Please enter all 4 values.")
            return render_template('configuration.html', configuration=config)

        if (float(grow_cpu_threshold) <= 0) or (float(shrink_cpu_threshold) <= 0) or (float(grow_ratio) <= 0) or (float(shrink_ratio) <= 0):
            flash("Values have to be positive.")
            return render_template('configuration.html', configuration=config)

        config.grow_cpu_threshold = float(grow_cpu_threshold)
        config.shrink_cpu_threshold = float(shrink_cpu_threshold)
        config.grow_ratio = float(grow_ratio)
        config.shrink_ratio = float(shrink_ratio)
        db.session.commit()

        flash("Configuration of Autoscaler changed successfully.")
        return render_template('configuration.html', configuration=config)

    current_configuration = Configuration.query.all()[0]
    return render_template('configuration.html', configuration=current_configuration)

