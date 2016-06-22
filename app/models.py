from app import db, bcrypt
from flask.ext.login import UserMixin
import re

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    title = db.Column(db.String(128))
    slug = db.Column(db.String(128),unique = True)
    published = db.Column(db.Boolean)

    # USES REGEX import re to make slug
    def create_slug(self, *args, **kwargs):
        t = re.sub('[^\w\s\d]', "", self.title)
        self.slug = re.sub('[^\w]', "-", t).lower()

    # toString method
    def __repr__(self):
        return '<Title %r, Body %r, Time %r, Published %r, Slug %r, ID %r>' % (self.title, self.body, self.timestamp,
                                                               self.published, self.slug, self.id)

class User(db.Model):
    email = db.Column(db.String(128), primary_key = True)
    password = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean)

    def is_active(self):
       return True

    def is_authenticated(self):
       return self.authenticated

    def get_id(self):
       return self.email
    
    def is_anonymous(self):
       return False
    
    def __repr__(self):
        return '<Email %r, Password %r, Authenticated %r>' % (self.email, self.password,
                                                              self.authenticated)

