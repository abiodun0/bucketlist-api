from flask import jsonify, request, current_app, url_for
from .authentication import auth
from ..models import User
from . import api
from .. import db
from .response import notacceptable, forbidden, unauthorized



@api.route('/auth/register',methods=['POST'])
def register():
	email = request.json.get('email')
	password = request.json.get('password')
	username = request.json.get('username')
	if email is None or password is None:
		return notacceptable("email and password field can't be left empty")
	if User.query.filter_by(email=email).first() is not None:
		return notacceptable("already exists", email)

	user = User(email=email, password=password, username=username)
	user.save()


	response = jsonify({
		'username': username,
		'email': email,
		'msg': "Successfully created user"
		})
	response.status_code = 201
	return response


@api.route('/user/<int:id>',methods=['GET'])
@auth.login_required
def user(id):
	user = User.query.filter_by(id=id).first()
	return jsonify(user.to_json())

