from datetime import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView





class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    bookings = db.relationship('Booking', backref= 'user',lazy='dynamic')

    
    def __repr__(self):
        return '<User %r>' % (self.id)

    
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    date = db.Column(db.String(150))
    runTime = db.Column(db.String(150))
    genre = db.Column(db.String(150))
    desc = db.Column(db.String(10000))
    imsrc = db.Column(db.String(200))
    shows = db.relationship('Shows',backref= 'movie',lazy='dynamic')

    
    def __repr__(self):
        return '<Movie %r>' % (self.title)

class Shows(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    theatre = db.Column(db.String(150))
    date = db.Column(db.String(150))
    time = db.Column(db.String(150))
    mov_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    price = db.Column(db.Integer)
    screen_no = db.Column(db.Integer)
    seats = db.relationship('Seats',backref= 'shows',lazy='dynamic')

    
    def __repr__(self):
        return '<Show %r>' % (self.id)

class ShowsView(ModelView):
    form_columns = ['id', 'theatre','date','time','movie','price','screen_no']


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seats_booked = db.relationship('Seats',backref= 'booking',lazy='dynamic')

    
    def __repr__(self):
        return '<Booking %r>' % (self.id)
    

class BookingView(ModelView):
    form_columns = ['id', 'user']

class Seats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_no = db.Column(db.Integer)
    status = db.Column(db.String(150))
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('booking.id'))

    
    def __repr__(self):
        return '<Seat %r>' % (self.id)  

            

class SeatsView(ModelView):
    form_columns = ['id', 'seat_no','status','shows','booking']


class Upcoming(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    date = db.Column(db.String(150))
    runTime = db.Column(db.String(150))
    genre = db.Column(db.String(150))
    desc = db.Column(db.String(10000))
    imsrc = db.Column(db.String(200))
