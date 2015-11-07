from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, g, url_for


from . import db


class BaseModel(db.Model):
	""" Base model for the database """
	__abstract__ = True

	#This automatically create id, date_created, and date_modified
	id = db.Column(db.Integer, primary_key=True,unique=True)
	date_created = db.Column(db.DateTime, index=True, default=datetime.now())
	date_modified = db.Column(db.DateTime, index=True, default=datetime.now(), onupdate=datetime.now())


	#utility function for saving to db
	def save(self):
		db.session.add(self)
		db.session.commit()

	#utility function to delete from database
	def delete(self):
		db.session.delete(self)
		db.session.commit()


class Item(BaseModel):
	""" Database model for the item"""
	__tablename__ = "items"
	name = db.Column(db.String(100))
	done = db.Column(db.Boolean, default=False)
	bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'), nullable=False)

	#utility function for the edit functionality
	def edit(self, name,done=False):
		self.name = name
		self.done = done
		self.date_modified = datetime.now()

	#utility function to covert the item to json
	def to_json(self):
		json_items = {
		'id': self.id,
		'name': self.name,
		'date_created': self.date_created,
		'last_modified': self.date_modified,
		'done': self.done
		}

		return json_items

class User(BaseModel):
	""" Database model for the user"""

	__tablename__ = "users"
	username = db.Column(db.String(64), nullable=True)
	email = db.Column(db.Text, nullable=False, unique=True)
	password_hash = db.Column(db.Text, nullable=False)
	bucketlists = db.relationship('Bucketlist', lazy='dynamic', backref=db.backref('owned_by', lazy='select'),cascade='all, delete-orphan')

	#string representation of the model
	def __str__(self):
		return self.email if self.email else self.username

	#utility funciton for the verification of password return bool
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	#utility function return the json format of the user information
	def to_json(self):
		json_items = {
		'username': self.username,
		'email': self.email,
		'date_registered': self.date_created,
		'no_of_bucket_list': self.bucketlists.count()
		}
		return json_items

	#utility function to get bucketlists created by the user
	def get_bucketlists(self):
		bucketlists = Bucketlist.query.filter_by(
                user_id=self.id)
		return bucketlists

	@property
	def password(self):
	    raise AttributeError("This attribute is not readbale")
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	#utility function to generate token for logged in users
	def generate_auth_token(self, expiration=None):
		s = Serializer(current_app.config['SECRET_KEY'], expiration or current_app.config['TOKEN_EXPIRE'])
		return s.dumps({'id': self.id})

	#utility function to verify token of logged in users and return the user instance
	@staticmethod
	def verify_auth_token(token):
		s = Serializer(current_app.config['SECRET_KEY']) 
		try:
			data = s.loads(token)
		except:
			return None
		return User.query.get(data['id'])

class Bucketlist(BaseModel):
	"""Model that handles the database for the bucketlist"""
	__tablename__ = "bucketlists"
	name = db.Column(db.String(100))
	items = db.relationship('Item', lazy='dynamic', backref=db.backref('bucketlist', lazy='select'),cascade='all, delete-orphan')
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	#utility function that creates a new bucketlist and sets it parent to the current user
	def create(self):
		self.user_id = g.current_user.id

	#utility function that allows for the edition of a bucketlist name
	def edit(self, name):
		self.name = name
		self.date_modified = datetime.now()

	#utility function that coverts the bucketlist item to a json serializable dictionary
	def to_json(self):
		items = [item.to_json() for item in self.items]
		json_bucketlist = {
			'id': self.id,
			'name': self.name,
			'no_of_items': self.items.count(),
			'items': items,
			'date_created': self.date_created,
			'last_modified': self.date_modified,
			'created_by': User.query.get(self.user_id).email}

		return json_bucketlist

	pass