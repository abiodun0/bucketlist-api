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
        db.create_all()

        # create test user:
        user = User(
            username='Anonymous', 
            email='anonymous@yahoo.com',
            password='anything'
        )
        user.save()
        # init the test client:
        self.client = self.app.test_client()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()



    def get_api_headers(self, access_token=''):
        """ formats the headers to be used when accessing API endpoints.
        """
        return {
            'Authorization': "Basic {}".format(access_token),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    

    def test_user_can_register_with_username(self):
        """ 
        Test for user registration form your specifying the username and the
        status code
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

    def test_if_user_can_login_with_email(self):
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

    def test_for_login_page(self):

    def test_wrong_user_can_not_login(self):
    	login_details = {
                'email': 'anonymous1@yahoo.com',
                'password': 'anything'}
    	response = self.client.post(
    		url_for('api.login'),
            headers=self.get_api_headers(),
            data=json.dumps(login_details)
            )

    	response_data = json.loads(response.data)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 401)
        #self.assertEqual(response_data.get('email'), "nobody@yahoo.com.com")


if __name__ == "__main__":
	unittest.main()