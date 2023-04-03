import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.profile import Profile
from werkzeug.security import generate_password_hash

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()
        
        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None

    def test_user_profile(self):
        data = {
            "id" :1,            
            "lastname" :"Adeyemo",
            "firstname" :"Musodiq",
            "othername":"Olamilekan",
            "bio":"Backend Developer",
            "gender":"Male",
            "user": 1
        }

        response = self.client.post('/profile/settings',json=data)

        #profile = Profile.query.filter_by(user=1).first()

        #assert profile.firstname == "Musodiq"

        assert response.status_code == 201

    """
def test_user_login(self):
    data = {
        "email":"sirmuso@gmail.com",
        "password":"musawdeeq"
    }

    response = self.client.post('/auth/login',json=data)

    assert response.status_code == 200
    """