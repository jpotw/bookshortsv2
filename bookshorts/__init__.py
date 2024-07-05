from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize ORM
    db.init_app(app)
    migrate.init_app(app, db)  # Migrate handles database migrations

    from bookshorts import models  # Ensure your models are imported so they are registered with SQLAlchemy
    from .views import main_views, history_views, login_views, summarize_views

    app.register_blueprint(login_views.bp)
    app.register_blueprint(main_views.bp)
    app.register_blueprint(history_views.bp)
    app.register_blueprint(summarize_views.bp)

    with app.app_context():
        db.create_all()  # Create tables for all models (useful for initial setup, but usually handled by migrations)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
