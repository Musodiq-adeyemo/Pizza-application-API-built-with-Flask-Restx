from flask import Flask
from flask_restx import Api
from .orders.views import order_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .profile.views import profile_namespace
from .utils import db
from flask_migrate import Migrate
from .models.order import Order
from .models.user import User
from .models.profile import Profile,ProfileImage
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound,MethodNotAllowed

def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    jwt = JWTManager(app)

    db.init_app(app)

    migrate = Migrate(app,db)

    api = Api(app)

    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace,path='/auth')
    api.add_namespace(profile_namespace,path='/profile')

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error":"Method Not Allowed"}, 404

    @api.errorhandler(NotFound)
    def method_not_allowed(error):
        return {"error":"Not Found"}, 404

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "User":User,
            "Order":Order,
            "Profile":Profile,
            "ProfileImage":ProfileImage
        }

    return app