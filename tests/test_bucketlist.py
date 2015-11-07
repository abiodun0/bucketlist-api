import unittest
import json
import base64
from flask import current_app, url_for, jsonify, g
from app import create_app, db
from app.models import User, Bucketlist

class BucketlistTestCase(unittest.TestCase):
    """Test for bucket list route"""
	
    def setUp(self):

        # setup the app and push app context:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    
        # setup the db:
        db.drop_all()
        db.create_all()

        # create test datas:
        user = User(
            username='Anonymous', 
            email='anonymous@yahoo.com',
            password='anything'
        )
        user.save()

        self.user = User(email="abiodun12@golden0.com",password="passes",username="abiodun")
        self.user.save()
        self.bucket_item = Bucketlist(name="Bucket List 1", user_id=self.user.id)
        self.bucket_item.save() 

        self.user2 = User(email="abiodun2@golden0.com",password="passes",username="bimps")
        self.user2.save()
        self.bucket_item2 = Bucketlist(name="Bucket List 2", user_id=self.user2.id)
        self.bucket_item2.save() 


        bucket_item = Bucketlist(name="Bucket List", user_id=user.id)
        bucket_item.save() 

        self.client = self.app.test_client()


        #default login details
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

    def get_api_headers(self, email='',password=''):
        """Set default authorization headers for token"""
    	return {
            'Authorization':
                'Basic ' + base64.b64encode(
                    (email + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }


    def test_for_bad_request(self):
        """Test for bad request """
    	new_bucket_item = {
    	"bucketlist_name": "New Bucketlist"
    	}
    	response = self.client.post(url_for('api.bucketlists'),headers=self.get_api_headers(self.token),
    		data=new_bucket_item
    		)

    	self.assertEqual(response.status_code,400)

    def test_for_new_bucketlist_item(self):
        """Test for addition of new bucketlist collection"""
    	new_bucket_item = {
    	"bucketlist_name": "New Bucketlist"
    	}
    	response = self.client.post(url_for('api.bucketlists'),headers=self.get_api_headers(self.token),
    		data=json.dumps(new_bucket_item)
    		)

    	self.assertEqual(response.status_code,201)

    def test_for_method_not_allowed(self):
        """Test for method not allowed exception"""
    	response = self.client.put(url_for('api.bucketlists'),headers=self.get_api_headers())

    	self.assertEqual(response.status_code,405)


    def test_for_protected_url(self):
        """Test guest cant access protected url"""
    	response = self.client.get(url_for('api.bucketlists'),headers=self.get_api_headers())

    	self.assertEqual(response.status_code,401)

    def test_for_not_authorized(self):
        """Test for bucketlist can only be accessed by the owner"""

    	#for /api/v1/:id/
        response = self.client.get(url_for('api.manage_bucketlist',id=1),headers=self.get_api_headers(self.token))
        #for /api/v1/:id/items
    	response2 = self.client.get(url_for('api.bucketlist_items',id=1),headers=self.get_api_headers(self.token))

    	self.assertEqual(response.status_code,401)
    	self.assertEqual(response2.status_code,401)

    def test_get_bucketlist_authorized(self):
        """Test for authorized users can access bucket list"""
    	response = self.client.get(url_for('api.manage_bucketlist',id=3),headers=self.get_api_headers(self.token))

    	self.assertEqual(response.status_code,200)

    def test_get_bucketlist_item_authorized(self):
        """Test for authorized users can access bucket list"""
    	response = self.client.get(url_for('api.bucketlist_items',id=3),headers=self.get_api_headers(self.token))

    	self.assertEqual(response.status_code,200)

    def test_get_bucketlist_add_new_item_authorized(self):
        """Test for can add new item in the bucketlist """
    	new_item = {
    	    	"item name": "New Item Bucketlist"
    	}
    	response = self.client.post(url_for('api.bucketlist_items',id=3),headers=self.get_api_headers(self.token),
    		data=json.dumps(new_item))

    	self.assertEqual(response.status_code,201)
    def test_get_bucketlist_no_bucket_list(self):
        """Test for bucketlist collection doesn't exist"""
    	response = self.client.get(url_for('api.bucketlist_items',id=5),headers=self.get_api_headers(self.token))

    	self.assertEqual(response.status_code,404)

    def test_get_edit_bucketlist(self):
        """ Test for edit bucketlist collection"""
    	edit_bucket_item = {
    	"bucketlist_name": "Edited Bucketlist"
    	}
    	response = self.client.put(url_for('api.manage_bucketlist',id=3),headers=self.get_api_headers(self.token),
    		data=json.dumps(edit_bucket_item)
    		)

    	response_data = json.loads(response.data)

    	self.assertEqual(response.status_code,201)

    def test_delete_bucketlist(self):
        """ Test for delete bucket list"""
    	response = self.client.delete(url_for('api.manage_bucketlist',id=3),headers=self.get_api_headers(self.token)
    		)

    	self.assertEqual(response.status_code,204)

    def test_for_bucket_list_item_not_found(self):
        """ test for get bucketlist item route /api/v1/:id/items not found """
    	response = self.client.get(url_for('api.manage_bucketlist',id=5),headers=self.get_api_headers(self.token))

    	self.assertEqual(response.status_code,404)

    def test_for_url_not_found(self):
        """ test for none existing url within the api applicaito """
    	response = self.client.get(url_for('api.bucketlists') + '/custompage',headers=self.get_api_headers(self.token))

    	self.assertEqual(response.status_code,404)

if __name__ == "__main__":
    unittest.main()