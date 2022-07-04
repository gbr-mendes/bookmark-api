"""This module is responsible for encopassing all the models for the bookmarks system"""
from datetime import datetime
from ..database.db import db
from ..utils.utils import generate_short_characters


class Bookmark(db.Model):
    """Model of the bookmar table on the database"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    vistis = db.Column(db.Integer, default=0)
    user_id = db.Colum(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_url()

    def __repr__(self) -> str:
        """This method is resposible for the string respresentation of a bookmark"""
        return f"Bookmark>>>{self.url}"
    
    def generate_short_url(self):
        """This method generates a unique short url"""
        chars = generate_short_characters()
        link = self.query.filter_by(short_url=chars).first()
        if link is not None:
            return self.generate_short_url()
        return chars
