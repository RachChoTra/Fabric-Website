'''
How to Create a new Database
----------------------------
Based on the information provided by: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

Also, this information is based on the Milton Tours Example provided by Dr. Jason Watson (2020).
I am re-writing this information in my own words for practice and study. 

In the terminal, in my case for windows I'll use cmd or powershell, navigate to the folder
just above pinkbuttons. Type 'python' to enter the python interpreter, and on the next 
line you should see the python version information, then you should see '>>>'. 
In the python interpreter type out the following (press enter after each line):

from pinkbuttons import db, create_app
    db.create_all(app=create_app())
The database should be created. Exit python interpreter by typing:
    quit()

You can use the DB Browser for SQLite to check that the structure of the database. 

'''
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin/')

@admin_bp.route('/')
def admin_home():
    return "Admin Home Page"
