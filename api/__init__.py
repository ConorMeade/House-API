from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init our database object
db = SQLAlchemy()

class InterceptRequestMiddlewate:
    # change 'Accepts' request header
    def __init__(self, wgsi_app):
        self.wgsi_app = wgsi_app
    
    def __call__(self,environ, start_repsonse):
        environ['Accepts'] = 'application/json'
        return self.wgsi_app(environ, start_repsonse)


def create_app():
    # define our Blueprint (template) for our application
    # create an instance of Flask class
    app = Flask(__name__)
    app.wsgi_app = InterceptRequestMiddlewate(app.wsgi_app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///houseapi.db'
    # depreceated feature
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # used in order to keep same ordering as in diirections
    app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)

    # avoiding circular imports
    from .models import House
    # create all our database tables we defined in models.py
    with app.app_context():
        db.create_all()

    # avoiding circular imports
    from .views import houses
    app.register_blueprint(houses)

    return app