from flask import Flask 
from controllers import routes
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(routes)
app.run(debug = True) # to allow for debugging and auto-reload
