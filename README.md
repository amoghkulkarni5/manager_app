# flask-images-webapp
This repo is for a webapp 'manager' to manage the AWS resources of the other app 'flask-images-webapp'

### Commands -
Start terminal from one level above project directory <br>
`source images_webapp/flask_env/bin/activate` <br>
`export FLASK_APP=manager_app` <br>
`export FLASK_DEBUG=1` <br>
`export FLASK_ENV=development` <br>
`flask run` <br>

### Libraries-
pip install flask flask-sqlalchemy flask-login

### Running UP DB interactions -
Log onto python interpreter one level above project directory
`from manager_app import db, create_app, models, models.User` <br>
`from manager_app.models import User` <br>
`db.create_all(app=create_app())` <br>
`manager = User(name='Amogh', email='amoghkulkarni5@gmail.com', password='amogh')` <br>
`db.app = create_app()` <br>
`db.session.add(manager)` <br>
`db.session.commit()` <br>
To check if manager is added properly:
`user= User.query.all()[0]` <br>
`print (user.id, user.email, user.password, user.name)` <br>
To delete : <br>
`db.drop_all(app=create_app())` <br>