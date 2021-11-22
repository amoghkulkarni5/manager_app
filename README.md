# flask-images-webapp
This repo is for a webapp 'manager' to manage the AWS resources of the other app 'flask-images-webapp'

### Commands -
Start terminal from one level above project directory <br>
`source manager_app/manager_app_venv/bin/activate` <br>
`export FLASK_APP=manager_app` <br>
`export FLASK_DEBUG=1` <br>
`export FLASK_ENV=development` <br>
`flask crontab add` <br>
`flask run` <br>

### Libraries-
pip install flask flask-sqlalchemy flask-login flask-crontab

### Running UP DB interactions -
Log onto python interpreter one level above project directory <br>
`from manager_app import db, create_app, models` <br>
`from manager_app.models import User, Configuration, Instance` <br>
`db.create_all(app=create_app())` <br>
`manager = User(name='Amogh', email='amoghkulkarni5@gmail.com', password='amogh')` <br>
`configuration= Configuration(grow_cpu_threshold=1.0, shrink_cpu_threshold=1.0, grow_ratio=1.0, shrink_ratio=1.0)` <br>
(Add instances to Instance database) <br>
`instance1 = Instance(status=True, aws_id='i-019c3d4829ed787b7')` <br>
`instance2 = Instance(status=False, aws_id='i-00d3569f8b698ed61')` <br>
`instance3 = Instance(status=False, aws_id='i-05cf818c060593edd')` <br>
`instance4 = Instance(status=False, aws_id='i-022d5c2dab67c9ea3')` <br>
`instance5 = Instance(status=False, aws_id='i-0c317f8638221aa09')` <br>
`instance6 = Instance(status=False, aws_id='i-039771dde920025fd')` <br>
`db.app = create_app()` <br>
`db.session.add(manager)` <br>
`db.session.add(configuration)` <br>
`db.session.add(instance1)` <br>
`db.session.add(instance2)` <br>
`db.session.add(instance3)` <br>
`db.session.add(instance4)` <br>
`db.session.add(instance5)` <br>
`db.session.add(instance6)` <br>
`db.session.commit()` <br>
####To check if data is added properly: <br>
`user = User.query.all()[0]` <br>
`ac = Configuration.query.all()[0]` <br>
`instance = Instance.query.all()[0]` <br>
`print (user.id, user.email, user.password, user.name)` <br>
`print (instance.id, instance.aws_id, instance.status)` <br>
`print (ac.grow_cpu_threshold, ac.shrink_cpu_threshold, ac.grow_ratio, ac.shrink_ratio)` <br>
####To delete : <br>
`db.drop_all(app=create_app())` <br>