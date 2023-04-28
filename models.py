from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow().replace(microsecond=0))
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow().replace(microsecond=0))

    def __repr__(self):
        return f"Document(id={self.id}, name='{self.name}')"


class DocumentVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().replace(microsecond=0))

    def __repr__(self):
        return f"DocumentVersion(id={self.id}, document_id={self.document_id}, name='{self.name}', created_at='{self.created_at}')"


class DocumentDeletion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, unique=True, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().replace(microsecond=0))

    def __repr__(self):
        return f"DocumentDeletion(id={self.id}, document_id={self.document_id}, deleted_at='{self.deleted_at}')"
