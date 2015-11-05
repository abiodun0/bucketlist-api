from flask import jsonify, request, current_app, url_for
from .authentication import auth
from ..models import User
from . import api
from .. import db
from .errors import notacceptable, forbidden, unauthorized

@api.route('/login',methods=['GET'])
def index():
	return jsonify({
		'name': "Abiodun",
		'post': "Software Developer"
		})

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
	db.session.add(user)
	db.session.commit()


	return jsonify({
		'msg': "Successfully created user"
		})



# logout endpoint
@api.route('/auth/logout/', methods=['POST'])
@auth.login_required
def logout():
    #session.clear()
    return jsonify({'status': 'Logged Out'})


@api.route('/user/<int:id>',methods=['GET'])
@auth.login_required
def user(id):
	user = User.query.filter_by(id=id).first()
	return jsonify(user.to_json())

