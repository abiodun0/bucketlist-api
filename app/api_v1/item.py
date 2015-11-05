from flask import jsonify, request, current_app, g

from ..models import Item, Bucketlist
from .authentication import auth
from .. import db
from . import api
from .response import unauthorized, forbidden, not_found, created, updated, deleted


@api.route('/bucketlist/<int:id>/items/<int:item_id>',methods=['GET','PUT','DELETE'])
@auth.login_required
def bucketlist_item(id,item_id):
	bucketlist = Bucketlist.query.filter_by(id=id).first()
	item = Item.query.filter_by(id=item_id).first()

	if bucketlist is None or item is None:
		return not_found("Bucketlist is not found")

	if item not in bucketlist.items:
		return forbidden("Wrong access information")
	
	if g.current_user.id != bucketlist.user_id:
		return unauthorized("You Dont Have Access to this resouce")

	if request.method == 'GET':
		response = jsonify({'item': item.to_json()})
		response.status_code = 200
		return response

	if request.method == 'PUT':
		name = request.json.get("item_name")
		item.edit(name)
		item.save()

		return updated("Successfully updated {}".format(name))

	if request.method == 'DELETE':
		item.delete()
		return deleted("sucessfully deleted {}".format(bucketlist.name))