from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
# from flask_migrate import Migrate 
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = '11ce25b061258c37b3de06a3'
app.config['SESSION_COOKIE_SECURE'] = False
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
# migrate = Migrate(app, db, render_as_batch=True)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from vincemart import routes
from vincemart import models