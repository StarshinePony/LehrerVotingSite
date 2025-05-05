import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the Base class
db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure the database connection
# Verwende SQLite anstatt PostgreSQL für die Entwicklung/Demo
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///teacher_ratings.db'
# Initialize the app with the extension
db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

with app.app_context():
    # Import models here to ensure they're registered with SQLAlchemy
    import models  # noqa: F401
    
    # Create all tables in the database
    db.create_all()

    # Check if admin account exists, and create if it doesn't
    from models import Admin
    from werkzeug.security import generate_password_hash
    
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin', password_hash=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()
        logging.info("Admin account created")
