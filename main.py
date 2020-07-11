from flask import Flask 
app = Flask(__name__)

from controllers import *
app.register_blueprint(routes)
app.run(debug = True) # to allow for debugging and auto-reload
