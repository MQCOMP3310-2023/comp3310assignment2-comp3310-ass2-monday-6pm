import unittest
from flask import current_app
from project import create_app, db
from project.models import UserAccount

registerPage = '/register'
loginPage ='/login'

testUsername = 'test2'
testPassword ='testP2'

#   DO NOT RUN 

#   Pytest script is functionally broken. One of the below tests (I believe test_registration_form) is breaking the website or DB, and causing Internal Server Errors until stopped and initialise_db.py is run. 

class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = True  # no CSRF during tests
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.client = self.app.test_client()  

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app


    def test_homepage_redirect(self):
        response = self.client.get('/', follow_redirects = True)
        assert response.status_code == 200

    def test_registration_form(self):
        response = self.client.get(registerPage)
        assert response.status_code == 200

    def test_login_form(self):
        response = self.client.get(loginPage)
        assert response.status_code == 200