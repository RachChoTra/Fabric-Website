# pinkbuttons/__init__.py

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    app.debug = True

    # Set the app configuration data
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///pinkbuttons.sqlite'
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Set a secret key for session and form security
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    bootstrap = Bootstrap(app)
    db.init_app(app)

    # Register blueprints
    from .views import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')
    from .admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500