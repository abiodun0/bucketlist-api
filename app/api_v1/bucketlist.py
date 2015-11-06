from flask import jsonify, request, current_app, g, url_for

from ..models import Bucketlist, Item
from .authentication import auth
from .. import db
from . import api
from .pagination import paginate
from .response import unauthorized, forbidden, custom_response, not_found




@api.route('/bucketlist/', methods=['POST','GET'])
@auth.login_required
def bucketlists():
	if request.method ==  'POST':
		name = request.json.get('bucketlist_name')
		bucketlist = Bucketlist(name=name)
		bucketlist.create()
		bucketlist.save()
		return created("successfully created {}".format(name))
	if request.method == 'GET':
		user = g.current_user
		options = request.args.copy()

		bucket_lists = paginate(user.bucketlists,'api.bucketlists',options,Bucketlist)
		bucket_lists['created_by'] = user.email
		response = jsonify(bucket_lists)

        response.status_code = 200
        return response


@api.route('/bucketlist/<int:id>/',methods=['GET','PUT','DELETE'])
@auth.login_required
def manage_bucketlist(id):
	bucketlist = Bucketlist.query.filter_by(id=id).first()
	if bucketlist is None:
		return not_found("Bucketlist not found")
	if g.current_user.id != bucketlist.user_id:
		return unauthorized("You Dont Have Access to this resouce")
	if request.method == 'GET':
		bucketlist = bucketlist.to_json()
		response = jsonify(bucketlist)
		response.status_code = 200
		return response
	if request.method == 'PUT':
		name = request.json.get("bucketlist_name")
		bucketlist.edit(name)
		bucketlist.save()
		return custom_response("successfull updated {}".format(name),201)

	if request.method == 'DELETE':
		bucketlist.delete()
		return custom_response("sucessfully deleted {}".format(bucketlist.name),204)


@api.route('/bucketlist/<int:id>/items',methods=['GET','POST'])
@auth.login_required
def bucketlist_items(id):
	bucketlist = Bucketlist.query.filter_by(id=id).first()
	if bucketlist is None:
		return not_found("This bucket list is not available")
	if g.current_user.id != bucketlist.user_id:
		return unauthorized("You dont have Access to this resouce")

	if request.method == 'POST':
		name = request.json.get("item_name")
		item = Item(name=name)
		item.bucketlist_id = bucketlist.id
		item.save()

		return custom_response("Successfully created item", 201)

	if request.method == 'GET':
		options = request.args.copy()

		bucket_items = paginate(bucketlist.items,'api.bucketlist_items',options,Item,id)

		response = jsonify(bucket_items)
		response.status_code = 200
        return response



