from flask import Flask 
from controllers import routes
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  
jwt = JWTManager(app)

app.register_blueprint(routes)
app.run(debug = True) # to allow for debugging and auto-reload
