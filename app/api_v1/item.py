from flask import jsonify, request, current_app, g

from ..models import Item, Bucketlist
from .authentication import auth
from .. import db
from . import api
from .response import unauthorized, forbidden, not_found, custom_response


@api.route('/bucketlist/<int:id>/items/<int:item_id>',methods=['GET','PUT','DELETE'])
@auth.login_required
def bucketlist_item(id,item_id):
	bucketlist = Bucketlist.query.filter_by(id=id).first()
	item = Item.query.filter_by(id=item_id).first()

	if bucketlist is None or item is None:
		return not_found("This resource or bucket list doesnt exist")

	if item not in bucketlist.items:
		return forbidden("You dont have access to this resource")
	
	if g.current_user.id != bucketlist.user_id:
		return unauthorized("You Dont Have Access to this resource")

	if request.method == 'GET':
		response = jsonify({'item': item.to_json()})
		response.status_code = 200
		return response

	if request.method == 'PUT':
		name = request.json.get("item_name")
		item.edit(name)
		item.save()

		return custom_response("Successfully updated {}".format(name),201)

	if request.method == 'DELETE':
		item.delete()
		return custom_response("sucessfully deleted {}".format(bucketlist.name),204)