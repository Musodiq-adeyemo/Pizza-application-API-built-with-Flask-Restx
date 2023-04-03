from flask_restx import Namespace,Resource,fields
from flask import request
from ..utils import db
from ..models.user import User
from werkzeug.security import generate_password_hash,check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token,create_refresh_token
from flask_jwt_extended import jwt_required,get_jwt_identity,unset_jwt_cookies

auth_namespace = Namespace("Auth",description="Namespace for authentication")

signup_model= auth_namespace.model(
    "signup", {
        'username':fields.String(required=True,description='A username'),
        'email':fields.String(required=True,description='An email'),
        'password':fields.String(required=True,description='A password')
    }
)

login_model= auth_namespace.model(
    "Login", {
        'email':fields.String(required=True,description='An email'),
        'password':fields.String(required=True,description='A password')
    }
)

user_model= auth_namespace.model(
    "User", {
        'id':fields.Integer(),
        'username':fields.String(required=True,description='A username'),
        'email':fields.String(required=True,description='An email'),
        'password':fields.String(required=True,description='A password'),
        'is_active':fields.Boolean(description="This shows if a User is active or not"),
        'is_staff':fields.Boolean(description="This shows if User is a staff or not")
    }
)

@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
        Users Registration
        """
        data = request.get_json()
        new_user = User(
            username=data.get('username'),
            email = data.get('email'),
            password = generate_password_hash(data.get('password'))
        )
        new_user.save()
        return new_user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
        Login Authentication 
        """
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if (user is not None) and check_password_hash(user.password,password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response = {
                "access_token":access_token,
                "refresh_token":refresh_token,
            }

            return response, HTTPStatus.CREATED

@auth_namespace.route('/refresh')
class Login_refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Generate Refresh Token 
        """
        username = get_jwt_identity()
        
        access_token = create_access_token(identity=username)

        return { "access_token":access_token}, HTTPStatus.OK

@auth_namespace.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        """
        Log the User Out 
        """
        unset_jwt_cookies
        db.session.commit()

        return {"message":"Successfully Logged Out"}, HTTPStatus.OK