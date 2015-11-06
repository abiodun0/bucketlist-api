import unittest
import json
from flask import current_app, url_for, jsonify, g
from app import create_app, db
from app.models import User

class BucketlistTestCase(unittest.TestCase):
	
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
   		return {
            'Authorization':
                'Basic ' + base64.b64encode(
                    (email + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }

    def test_for_forbidden_protected_url(self):
    	response = self.client.get(url_for('api.bucketlists'),headers=self.get_api_headers())

    	self.assertEqual(response.status_code,201)