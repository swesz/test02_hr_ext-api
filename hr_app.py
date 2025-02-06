from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize Flask hr_app
hr_app = Flask(__name__)

# Database Configuration
hr_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company_hr.db'
hr_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
hr_app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Change for production

# Initialize Extensions
db = SQLAlchemy(hr_app)
ma = Marshmallow(hr_app)
bcrypt = Bcrypt(hr_app)
jwt = JWTManager(hr_app)

from routes import *

# Run the hr_app
if __name__ == '__main__':
    hr_app.run(debug=True)