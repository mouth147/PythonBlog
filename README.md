# Python Blog

This is a basic blog made using Python.

It uses
- Flask
- WTForms
- Bcrypt
- SQLAlchemy
- Misaka
- Markdown

# Installation

Set up your instance of this blog. 

1. Clone the link into your directory
2. Set up a python virtualenv
3. Install the python requirements by running ```pip install -r requirements.txt```
4. Start up your python interpreter and create a database
    ```
    from app import db; db.create_all()
    ```
5. Create a new user in python interpreter
    ```
from app import db, bcrypt; 
from app.models import User; em = "TEST@EMAIL.COM"; pw = "PASSWORD"; pw_hash = bcrypt.generate_password_hash(pw); 
u = User(email = em, password = pw_hash); 
db.session.add(u);db.session.commit()
```
6. Go to localhost:5000/login and enjoy!

# Screenshots

For screenshots visit [my website](www.mikebotti.com)!

