from flask import Flask, render_template, request, jsonify, session, redirect, flash
from models import User, Goal

app = Flask(__name__)


@app.route('/')
def index():
	"""Home page"""

	return render_template('index.html')


@app.route('/register')
def register_user():
	"""User registration page"""

	return render_template('register.html')


@app.route('/login')
def login_form():
	"""User login page"""

	return render_template('login.html')


# ------- Auth Routes -------


@app.route('/api/auth', methods=['POST'])
def login():
	user = User.query.filter_by(username=request.form.get('username')).first()

	if user.login(request.form.get('password')):
		app.logger.info('...Login successful.')
		session['user_id'] = user.id
	else:
		app.logger.info('-  Login failure  -')
		flash('Invalid username or password.')
		return render_template('login.html')

	return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
	del session['user_id']

	return redirect('/')


@app.route('/api/register', methods=['POST'])
def register_auth():
	"""Handles user registration data"""

	app.logger.info('Registering new user...')

	user_data = dict(request.form)

	if user_data.get('password') == user_data.get('passwordConfirm'):
		del user_data['passwordConfirm']

		user = User(**user_data)
		user.create_password(user_data.get('password'))
		user.save()
		app.logger.info(f'New user {user.id} created. Logging in...')
		session['user_id'] = user.id

		return redirect(f'/users/{user.id}')


# ------- User Routes -------


# To Do:
#	- Create new goal
#	- Edit goal
#	- Delete goal