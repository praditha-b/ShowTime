from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager  
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView


db = SQLAlchemy()   #object of sqlalchemy
DB_NAME = "database.db" 

def create_app():

    #Created a flask application, initialised a secret key and returned the application
    
    app=Flask(__name__) 
     #__name__ is a convienent way to import name of the place where the app is defined
    
    #added on my own not fully sure what it does
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    #encrypts cookies and session data 
    app.config['SECRET_KEY'] = 'asjcfekjieahbkeopjfnv'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

   

    from .views import views
    from .auth import auth

    #registering blueprints with flask
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User

     
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)

    admin = Admin(app, template_mode='bootstrap3')

    from .models import Movie, Shows,Booking,Seats, Upcoming, BookingView,ShowsView
    
    

    admin.add_view(ModelView(Movie, db.session))
    admin.add_view(ShowsView(Shows, db.session))
    admin.add_view(BookingView(Booking, db.session))
    admin.add_view(ModelView(Seats, db.session))
    admin.add_view(ModelView(Upcoming, db.session))


    return app 


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')