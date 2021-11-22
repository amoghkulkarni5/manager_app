from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_crontab import Crontab
import math

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
crontab = Crontab()


def add_instances_to_worker_pool(active_instances, inactive_instances, no_of_instances):
    active_instance_count = active_instances.count()
    inactive_instance_count = inactive_instances.count()
    if no_of_instances > 6:
        no_of_instances = 6
    if active_instances == 1 and no_of_instances == 6:
        print("\nAlready at maximum capacity")
        return
    print(f"\nTotal Worker pool now has {no_of_instances} instances")
    print(f"\nAdding { no_of_instances - active_instance_count} instances")


def remove_instances_from_worker_pool(active_instances, inactive_instances, no_of_instances):
    active_instance_count = active_instances.count()
    if no_of_instances < 1:
        no_of_instances = 1
    if active_instances == 1 and no_of_instances == 1:
        print("\nAlready at minimum capacity")
        return
    print(f"\nTotal Worker pool now has {no_of_instances} instances")
    print(f"Removing {active_instance_count - no_of_instances} instances")


def run_autoscaler(configuration, active_instances, active_count, inactive_instances):
    total_cpu_utilization = 0
    for instance in active_instances:
        # GET VALUE OF CPU THRESHOLD AND STORE IN instance_cpu_threshold
        instance_cpu_threshold = 1
        total_cpu_utilization += instance_cpu_threshold

    avg_utilization = total_cpu_utilization / active_count
    if avg_utilization >= configuration.grow_cpu_threshold:
        new_worker_pool_instance_count = int(math.floor(active_count * configuration.grow_ratio))
        print (f"Average Utilization: {avg_utilization}, NEED TO GROW")
        add_instances_to_worker_pool(active_instances, inactive_instances, new_worker_pool_instance_count)

    elif avg_utilization <= configuration.shrink_cpu_threshold:
        new_worker_pool_instance_count = int(math.floor(active_count * configuration.shrink_ratio))
        print(f"Average Utilization: {avg_utilization}\nNEED TO SHRINK\n\n")
        remove_instances_from_worker_pool(active_instances, inactive_instances, new_worker_pool_instance_count)

    else:
        print(f"Average Utilization: {avg_utilization}\nNO NEED TO MODIFY\n\n")

    print("----------------------------------------------------------------")


def autoscaler():
    from .models import Configuration, Instance
    active_instances = Instance.query.filter(Instance.status == True)
    inactive_instances = Instance.query.filter(Instance.status == False)
    active_instance_count = active_instances.count()
    configuration = Configuration.query.all()[0]

    print("----------------------------------------------------------------")
    print(f"\nCONFIGURATION:\n  " +
          f"grow_cpu_threshold= {configuration.grow_cpu_threshold}\n  " +
          f"shrink_cpu_threshold= {configuration.shrink_cpu_threshold}\n  " +
          f"grow_ratio= {configuration.grow_ratio}\n  " +
          f"shrink_ratio= {configuration.shrink_ratio}\n")
    run_autoscaler(configuration, active_instances, active_instance_count, inactive_instances)


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'SECRETKEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    crontab.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # CRON task for autoscaler
    @crontab.job(minute="*", hour="*")
    def autoscaler_job():
        autoscaler()

    return app

