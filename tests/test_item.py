import unittest
import json
import base64
from flask import current_app, url_for, jsonify, g
from app import create_app, db
from app.models import User, Bucketlist, Item

class BucketlistTestCase(unittest.TestCase):
    """" Test cases for the route /api/v1/:id/item/:item_id"""
	
    def setUp(self):

        # setup the app and push app context:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    
        # setup the db:
        db.drop_all()
        db.create_all()

        # create test datas for the users, bucketlists, and items:
        user = User(
            username='Anonymous', 
            email='anonymous@yahoo.com',
            password='anything'
        )
        user.save()


        self.user = User(email="abiodun1@golden0.com",password="passes",username="abiodun")
        self.user.save()
        self.bucket_item = Bucketlist(name="Bucket List 1", user_id=self.user.id)
        self.bucket_item.save()

        self.item = Item(name="Item 1", bucketlist_id=self.bucket_item.id)
        self.item.save()

        self.user2 = User(email="abiodun2@golden0.com",password="passes",username="bimps")
        self.user2.save()
        self.bucket_item2 = Bucketlist(name="Bucket List 2", user_id=self.user2.id)
        self.bucket_item2.save() 

        self.item2 = Item(name="Item 1", bucketlist_id=self.bucket_item2.id)
        self.item2.save()


        bucket_item = Bucketlist(name="Bucket List", user_id=user.id)
        bucket_item.save()


        item = Item(name="Item 1", bucketlist_id=bucket_item.id)
        item.save() 

        self.client = self.app.test_client()


        #create default login 
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

    def get_api_headers(self, token='',):
        """ get authorization header with login credentials or token"""
    	return {
            'Authorization':
                'Basic ' + base64.b64encode(
                    (token + ':' + '').encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }
    def test_for_error_bucketlist_or_item(self):
        """ test exception on the bucketlist item"""
        #response for not found bucketlists or item
        response = self.client.get(url_for('api.bucketlist_item',id=5,item_id=5),headers=self.get_api_headers(self.token))

        #response for item not belonging to a bucketlist
        response_two= self.client.get(url_for('api.bucketlist_item',id=3,item_id=1),headers=self.get_api_headers(self.token))

        #repsone for user not authorized for the bucketlist colleciton
        response_three = self.client.get(url_for('api.bucketlist_item',id=2,item_id=2),headers=self.get_api_headers(self.token))

        self.assertEqual(response.status_code,404)
        self.assertEqual(response_two.status_code,403)
        self.assertEqual(response_three.status_code,401)

    def test_for_each_authenticated_method(self):
        """Test for the http verbs for route /api/v1/:id/item/:item_id action"""
        item = {
        "item_name": "changed item"
        }

        #response for get request
        response = self.client.get(url_for('api.bucketlist_item',id=3,item_id=3),headers=self.get_api_headers(self.token))
        #response for the put request
        response_two = self.client.put(url_for('api.bucketlist_item',id=3,item_id=3),headers=self.get_api_headers(self.token),
            data=json.dumps(item))
        #response for delete request 
        response_three= self.client.delete(url_for('api.bucketlist_item',id=3,item_id=3),headers=self.get_api_headers(self.token))

        self.assertEqual(response.status_code,200)
        self.assertEqual(response_two.status_code,201)
        self.assertEqual(response_three.status_code,204)

if __name__ == "__main__":
    unittest.main()

