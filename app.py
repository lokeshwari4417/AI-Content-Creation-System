# ============================================================
# app.py - Main Flask Application Entry Point
# AI Content Creation System
# ============================================================

import os
from flask import Flask
from dotenv import load_dotenv
from models.content_model import db
from routes.content_routes import content_bp

# Load environment variables from .env file
load_dotenv()

def create_app():
    """
    Application factory function.
    Creates and configures the Flask app instance.
    """
    app = Flask(__name__)

    # ── Database Configuration ──────────────────────────────
    # SQLite database stored in the project root
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Secret key for session management
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ai-content-secret-2024')

    # ── Initialize Extensions ───────────────────────────────
    db.init_app(app)

    # ── Register Blueprints ─────────────────────────────────
    # All content-related routes are in the content Blueprint
    app.register_blueprint(content_bp)

    # ── Create Database Tables ──────────────────────────────
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully.")

    return app


# ── Run the Application ─────────────────────────────────────

app = create_app() 

if __name__ == '__main__':
    app = create_app()
    print("🚀 AI Content Creation System is running...")
    print("📍 Visit: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
