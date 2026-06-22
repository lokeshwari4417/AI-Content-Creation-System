# ============================================================
# models/content_model.py - Database Model using SQLAlchemy ORM
# Defines the ContentHistory table schema
# ============================================================

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create the SQLAlchemy database instance
# This is shared across the entire application
db = SQLAlchemy()


class ContentHistory(db.Model):
    """
    SQLAlchemy ORM model for storing generated content history.

    Each row represents one content generation request
    along with the AI-generated output.
    """

    # Table name in the SQLite database
    __tablename__ = 'content_history'

    # ── Columns ─────────────────────────────────────────────
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Type of content (e.g., "Blog Post", "Marketing Email")
    content_type = db.Column(db.String(100), nullable=False)

    # The topic the user entered
    topic = db.Column(db.String(500), nullable=False)

    # Target audience specified by the user
    audience = db.Column(db.String(200), nullable=False)

    # Writing tone (Professional, Friendly, Casual, etc.)
    tone = db.Column(db.String(100), nullable=False)

    # Requested length (Short, Medium, Long)
    length = db.Column(db.String(50), nullable=False)

    # The AI-generated content (can be very long, so use Text type)
    generated_content = db.Column(db.Text, nullable=False)

    # Timestamp of when the content was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """String representation of the model instance."""
        return f'<ContentHistory id={self.id} type={self.content_type} topic={self.topic[:30]}>'

    def to_dict(self):
        """
        Convert the model instance to a Python dictionary.
        Useful for returning JSON responses.
        """
        return {
            'id': self.id,
            'content_type': self.content_type,
            'topic': self.topic,
            'audience': self.audience,
            'tone': self.tone,
            'length': self.length,
            'generated_content': self.generated_content,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
