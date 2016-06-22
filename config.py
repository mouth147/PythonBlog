import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SECRET_KEY = 'PASSWORD'
UPLOADED_PHOTOS_DEST = 'app/static/images'
