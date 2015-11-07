import base64
import unittest
import json
from flask import current_app, url_for, jsonify, g
from app import create_app, db
from app.models import User



class AuthenticationTestCase(unittest.TestCase):
    """ Testcase for the Authentication related API endpoints 
    """

    def setUp(self):

        # setup the app and push app context:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # setup the db:
        db.drop_all()
        db.create_all()

        # create test user:
        user = User(
            username='Anonymous', 
            email='anonymous@yahoo.com',
            password='anything'
        )
        user.save()

        self.client = self.app.test_client()

        #response = self.client.post()

        login_details = {
    	'email': 'anonymous@yahoo.com',
    	'password': 'anything'}
    	response = self.client.post(
    		url_for('api.login'),
            headers=self.get_api_headers(),
            data=json.dumps(login_details)
            )
    	self.token = json.loads(response.data)['token']


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, email='', password=''): 
        """Utility method that returns the api headers with token if set"""
    	return {
            'Authorization':
                'Basic ' + base64.b64encode(
                    (email + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }

    def test_user_can_register_with_username(self):
        """ Test for user registration form your specifying the username and thestatus code
        """
        register_details = {
                'username': 'someone', 
                'email':'nobody@yahoo.com',
                'password': 'nothing',
            }
        response = self.client.post(
            url_for('api.register'),
            headers=self.get_api_headers(),
            data=json.dumps(register_details)
        )
        response_data = json.loads(response.data)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get('email'), "nobody@yahoo.com")

    def test_user_can_not_register_with_exsiting_email(self):
        """ Test for user cant register with an existing email"""
        register_details = {
                'username': 'so2meone', 
                'email':'anonymous@yahoo.com',
                'password': 'nothing',
            }
        response = self.client.post(
            url_for('api.register'),
            headers=self.get_api_headers(),
            data=json.dumps(register_details)
        )
        response_data = json.loads(response.data)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 406)
        self.assertIsNone(response_data.get('email'))

    def test_if_user_can_login_with_email(self):
        """ Test for user loggin in with email """
    	login_details = {
    	'email': 'anonymous@yahoo.com',
    	'password': 'anything'}
    	response = self.client.post(
    		url_for('api.login'),
            headers=self.get_api_headers(),
            data=json.dumps(login_details)
            )
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 200)
    def test_protected_url(self):

    	response = self.client.get(url_for('api.bucketlists'),
     		headers=self.get_api_headers(self.token)
     		)
     	#import pdb; pdb.set_trace()
     	self.assertEqual(response.status_code, 200)
    def test_logout_page(self):
        """ Test for logout page"""
    	response = self.client.post(url_for('api.logout'),headers=self.get_api_headers(self.token))

     	self.assertEqual(response.status_code, 201)

    def test_unregistered_user_cant_login(self):
        """Test for unregistered user cant login """
        
    	login_details = {
                'email': 'anonymous1@yahoo.com',
                'password': 'anything'}
    	response = self.client.post(
    		url_for('api.login'),
            headers=self.get_api_headers(),
            data=json.dumps(login_details)
            )

    	response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)



if __name__ == "__main__":
	unittest.main()