from flask_restx import Namespace,Resource,fields
from flask import request
from http import HTTPStatus
from ..utils import db
from ..models.profile import Profile,ProfileImage
from ..models.user import User
from flask_jwt_extended import get_jwt_identity,jwt_required
from werkzeug.utils import secure_filename

profile_namespace = Namespace('Profile',description='Namespace for Profile')

profile_model= profile_namespace.model(
    "Settings", {
        'lastname':fields.String(description='A lastname'),
        'firstname':fields.String(description='A firstname'),
        'othername':fields.String(description='An othername'),
        'bio':fields.String(description='A Bio'),
        'gender':fields.String(description='A Gender'),
        'user':fields.Integer(description='An user id')
    }
)

show_profile_model= profile_namespace.model(
    "Profile", {
        'id':fields.Integer(),
        'lastname':fields.String(description='A lastname'),
        'firstname':fields.String(description='A firstname'),
        'gender':fields.String(description='A Gender'),
        'user':fields.Integer(description='An user id')
    }
)

profile_image_model= profile_namespace.model(
    "Image", {
        'pic':fields.String(description='A name'),
        'profile':fields.Integer(description='A profile id')
    }
)

@profile_namespace.route('/settings')
class ProfileSettings(Resource):
    @profile_namespace.expect(profile_model)
    @profile_namespace.marshal_with(show_profile_model)
    @jwt_required()
    def post(self):
        """
        Create Profile
        """
        data = request.get_json()
        new_profile = Profile(
            lastname=data.get('lastname'),
            firstname=data.get('firstname'),
            othername=data.get('othername'),
            bio=data.get('bio'),
            gender=data.get('gender'),
            user=data.get('user')
        )
        
        new_profile.save()
        return new_profile, HTTPStatus.CREATED

    @profile_namespace.marshal_with(show_profile_model)
    @jwt_required()
    def get(self):
        """
        Get all Profile
        
        """
        profiles = Profile.query.all()
        return profiles, HTTPStatus.OK

@profile_namespace.route('/settings/<int:profile_id>')
class GetUpdateDeleteProfile(Resource):
    @profile_namespace.expect(profile_model)
    @profile_namespace.marshal_with(show_profile_model)
    @jwt_required()
    def put(self,profile_id):
        """
        Update Profile
        
        """
        data = profile_namespace.payload
        profile_update = Profile.get_by_id(profile_id)

        profile_update.lastname=data['lastname'],
        profile_update.firstname=data['firstname'],
        profile_update.othername=data['othername'],
        profile_update.bio=data['bio'],
        profile_update.gender=data['gender']

        db.session.commit()

        return profile_update, HTTPStatus.OK
    
    @profile_namespace.marshal_with(show_profile_model)
    @jwt_required()
    def get(self,profile_id):
        """
        Get Profile by ID
        
        """
        profile = Profile.get_by_id(profile_id)

        return profile, HTTPStatus.OK
    
    @jwt_required()
    def delete(self,profile_id):
        """
        Delete Profile
        
        """
        delete_profile = Profile.get_by_id(profile_id)

        db.session.delete(delete_profile)
        db.session.commit()

        return {"Deleted Successfully!"}

@profile_namespace.route('/upload')
class ProfilePicture(Resource):
    @profile_namespace.expect(profile_image_model)
    @jwt_required()
    def post(self):
        """
        Create Profile Picture
        """
        data = request.get_json()

        pic = request.files('pic')
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype

        image_upload = ProfileImage(img = pic.read(),mimetype=mimetype, name=filename,profile = data.get('profile'))
        db.session.add(image_upload)
        db.session.commit()