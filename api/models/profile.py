from ..utils import db
from datetime import datetime


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer(), primary_key=True)
    othername = db.Column(db.String(100))
    firstname = db.Column(db.String(100),nullable=False)
    lastname = db.Column(db.String(100),nullable=False)
    bio = db.Column(db.Text(),nullable=False)
    gender = db.Column(db.String(20),nullable=False)
    created_at = db.Column(db.DateTime(),default=datetime.utcnow)
    profile_picture = db.relationship('ProfileImage',backref='owner_picture',lazy=True)
    user = db.Column(db.Integer(),db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Profile : {self.lastname} {self.firstname}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
        
class ProfileImage(db.Model):
    __tablename__ = 'profileimages'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    img = db.Column(db.String(70))
    minetype = db.Column(db.String(100))
    profile = db.Column(db.Integer(),db.ForeignKey('profiles.id'))

    def __repr__(self):
        return f"UserImage {self.name}"