from flask import jsonify, request, current_app, g

from ..models import Bucketlist, Item
from .authentication import auth
from .. import db
from . import api
from .response import unauthorized, forbidden, created, updated, deleted, not_found



@api.route('/bucketlist/', methods=['POST','GET'])
@auth.login_required
def create_bucketlist():
	if request.method ==  'POST':
		name = request.json.get('bucketlist_name')
		bucketlist = Bucketlist(name=name)
		bucketlist.create()
		bucketlist.save()
		return created("successfully created {}".format(name))
	if request.method == 'GET':
		user = g.current_user
		bucketlists = [bucketlist.name for bucketlist in user.bucketlists]
		print bucketlists
		response = jsonify({'bucketlists': bucketlists})
		response.status_code = 200
		return response


@api.route('/bucketlist/<int:id>/',methods=['GET','PUT','DELETE'])
@auth.login_required
def bucketlist(id):
	bucketlist = Bucketlist.query.filter_by(id=id).first()
	if bucketlist is None:
		return not_found("Bucketlist Not found")
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
		return updated("successfull updated {}".format(name))

	if request.method == 'DELETE':
		bucketlist.delete()
		return deleted("sucessfully deleted {}".format(bucketlist.name))


@api.route('/bucketlist/<int:id>/items',methods=['GET','POST'])
@auth.login_required
def bucketlist_items(id):
	bucketlist = Bucketlist.query.filter_by(id=id).first()
	if bucketlist is None:
		return not_found("Bucketlist is not found")
	if g.current_user.id != bucketlist.user_id:
		return unauthorized("You Dont Have Access to this resouce")

	if request.method == 'GET':

		items = [item.to_json() for item in bucketlist.items]

		response = jsonify({'items': items })
		response.status_code = 200
		return response
	if request.method == 'POST':
		name = request.json.get("item_name")
		item = Item(name=name)
		item.bucketlist_id = bucketlist.id
		item.save()

		return created("successfully created {}".format(item.name))


