from sqlite3.dbapi2 import Cursor
from flask import Blueprint, render_template
from flask.helpers import url_for
from flask_login import login_required, current_user
from . import db
from .models import Movie
import sqlite3
from . import DB_NAME
import os.path
from .models import User

#making a blueprint for flask application called views
views = Blueprint('views',__name__)

@views.route('/')
def home():

    db.session.commit()

    
    

    r = db.session.execute("SELECT id from Movie")
    s = db.session.execute("SELECT * from Movie")
    
    idrows = r.fetchall()
    rows = s.fetchall()

    mid = db.session.execute("SELECT id from Upcoming").fetchall()
    ur = db.session.execute("SELECT * from Upcoming").fetchall()


    return render_template("home.html",user=current_user,movid=len(idrows),mov=rows,mid=len(mid),mv=ur)