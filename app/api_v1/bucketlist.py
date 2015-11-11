from flask import jsonify, request, current_app, g, url_for

from ..models import Bucketlist, Item
from .authentication import auth
from .. import db
from . import api
from .pagination import paginate
from .response import unauthorized, forbidden, custom_response, not_found



#Bucketlist Endpoint
@api.route('/bucketlist/', methods=['POST','GET'])
@auth.login_required
def bucketlists():
	""" This funciton takes care of the GET and the POST request for /v1/bucketlist endpoint"""

	if request.method ==  'POST':
		#returns status code of 201 and json success message for a newly created bucket list
		name = request.json.get('bucketlist_name')
		bucketlist = Bucketlist(name=name)
		bucketlist.create()
		bucketlist.save()
		return custom_response("Successfully created {}".format(name),201)
	if request.method == 'GET':

		#returns status code of 200 and a list of bucket list created by the user
		user = g.current_user
		options = request.args.copy()

		#Handles the pagination and quering of the bucketlists by name and limit
		bucket_lists = paginate(user.bucketlists,'api.bucketlists',options,Bucketlist)
		bucket_lists['created_by'] = user.email
		response = jsonify(bucket_lists)

        response.status_code = 200
        return response

#Single bucket list endpoint
@api.route('/bucketlist/<int:id>', methods=['GET','PUT','DELETE'])
@auth.login_required
def manage_bucketlist(id):
	""" This function manages a particular bucket list of id : id """

	#assing the bucketlist object to a variable
	bucketlist = Bucketlist.query.filter_by(id=id).first()
	if bucketlist is None:
		#checks for existence
		return not_found("Bucketlist not found")
	if g.current_user.id != bucketlist.user_id:
		#check if the user have access to the bucketlist
		return unauthorized("You Dont Have Access to this resouce")
	if request.method == 'GET':
		#returns the item of the bucketlist with its items in bracket with a status code of 200
		bucketlist = bucketlist.to_json()
		response = jsonify(bucketlist)
		response.status_code = 200
		return response
	if request.method == 'PUT':
		#handles the edition of a particular bucketlist name takes a json with the property of "bucketlist_name"
		name = request.json.get("bucketlist_name")
		bucketlist.edit(name)
		bucketlist.save()
		return custom_response("Successfully updated {}".format(name),201)

	if request.method == 'DELETE':
		#handles the deletion of a particular bucket list item
		bucketlist.delete()
		return custom_response("Sucessfully deleted {}".format(bucketlist.name),204)

#Bucketlist item editing endpoint
@api.route('/bucketlist/<int:id>/items', methods=['GET','POST'])
@auth.login_required
def bucketlist_items(id):
	"""This function handles the bucketlist item for a particular bucket list /v1/:id/items"""

	bucketlist = Bucketlist.query.filter_by(id=id).first()
	if bucketlist is None:
		#Checks if the bucketlist is available
		return not_found("This bucket list is not available")
	if g.current_user.id != bucketlist.user_id:
		#checks if the global user have access to the selected bucketlist item
		return unauthorized("You dont have Access to this resource")

	if request.method == 'POST':
		#creates a new item that is a member of the present bucket list
		name = request.json.get("item_name")
		item = Item(name=name)
		item.bucketlist_id = bucketlist.id
		item.save()

		return custom_response("Successfully created item {}".format(item.name), 201)

	if request.method == 'GET':
		#Get all the bucketlist items under this bucketlist
		options = request.args.copy()

		#gets all the paginated items under this bucket list
		bucket_items = paginate(bucketlist.items,'api.bucketlist_items',options,Item,id)
		bucket_items['name'] = bucketlist.name
		bucket_items['created_by'] = bucketlist.owned_by.email

		response = jsonify(bucket_items)
		response.status_code = 200
        return response



