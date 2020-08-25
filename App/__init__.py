import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = "s3cr37_k3y"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/recipe_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.permanent_session_lifetime = timedelta(days=7)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', 'kibwalid@gmail.com') #email
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS', '') #pass
mail = Mail(app)

from App import routes
