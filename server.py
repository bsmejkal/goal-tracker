"""Server for web app"""

from routes import app
from models import connect_to_db



if __name__ == "__main__":

	app.secret_key = "SUNDERED"
	app.debug = False
	app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

	connect_to_db(app)

	from flask_debugtoolbar import DebugToolbarExtension
	DebugToolbarExtension(app)

	app.run(port=5000, host='0.0.0.0')