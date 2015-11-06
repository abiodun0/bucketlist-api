from flask import jsonify, request, current_app, g, url_for

from ..models import Bucketlist, Item
from .authentication import auth
from .. import db
from . import api
from .response import unauthorized, forbidden, created, updated, deleted, not_found
from .pagination import paginate



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

		response = jsonify({
			'bucketlists': [bucketlist.to_json() for bucketlist in bucket_lists['items']],
			'prev_page': bucket_lists['prev_page'],
			'next_page': bucket_lists['next_page'],
			'total_items': bucket_lists['total_item'],
			'current_page': bucket_lists['current_page']

			})

        response.status_code = 200
        return response


@api.route('/bucketlist/<int:id>/',methods=['GET','PUT','DELETE'])
@auth.login_required
def manage_bucketlist(id):
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
		options = request.args.copy()

		bucket_lists = paginate(bucketlist.items,'api.bucketlist_items',options,Item,id)

		response = jsonify({
			'bucketlist_items': [bucketlist.to_json() for bucketlist in bucket_lists['items']],
			'prev_page': bucket_lists['prev_page'],
			'next_page': bucket_lists['next_page'],
			'total_items': bucket_lists['total_item'],
			'current_page': bucket_lists['current_page']

			})

        response.status_code = 200
        return response
	if request.method == 'POST':
		name = request.json.get("item_name")
		item = Item(name=name)
		item.bucketlist_id = bucketlist.id
		item.save()

		return created("successfully created {}".format(item.name))


