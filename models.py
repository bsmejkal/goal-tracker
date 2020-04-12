
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

app = Flask(__name__)
app.secret_key = 'SUNDERED'


class ModelMix:

	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()


class User(ModelMix, db.Model):
	"""Users"""

	__tablename__ = 'users'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String, nullable=False, unique=True)
	username = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(250), nullable=False)


	def __repr__(self):
		return f'<User ID = {self.id}, username = {self.username}>'

	def create_password(self, password):
		self.password = generate_password_hash(password)

	def login(self, password):
		return check_password_hash(self.password, password)


class Goal(ModelMix, db.Model):
	"""User Goals"""

	__tablename__ = "goals"

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	date = db.Column(db.Date, nullable=False)
	description = db.Column(db.String(250))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	goal_keeper = db.relationship('User', backref='events')

	def __repr__(self):

		return f'<Goal name = {self.name} id = {self.id}>'


def connect_to_db(app):

	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///goal_tracker'
	app.config['SQLALCHEMY_ECHO'] = True
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.app = app
	db.init_app(app)


if __name__ == "__main__":

	from server import app
	connect_to_db(app)
	print('Connected to database.')