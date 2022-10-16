from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Booking, User, Movie, Shows, Seats, Upcoming
from werkzeug.security import generate_password_hash, check_password_hash  
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import random
import string
import pyqrcode 


#making a blueprint for flask application called auth
auth = Blueprint('auth',__name__)

@login_required
@auth.route('/admin',methods=['GET','POST'])
def admin():
    return render_template("admin/index.html",a=100)

 
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again',category='error')
        else:
            flash('Email does not exist',category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')  

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created!',category='success')
            #login_user(user, remember=True)
            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)
        
    
     
@auth.route('/description1',methods=['GET','POST'])
def description():
    
    r = db.session.execute("SELECT * from Movie").fetchall()
    
    a = request.form.get('hello')

    return render_template("description1.html",user=current_user,a=int(a),mov=r)

  
@auth.route('/upcomingmovie',methods=['GET','POST'])
def upcomingmovie():

    r = db.session.execute("SELECT * from Upcoming").fetchall()   

    a = request.form.get('hello')

    return render_template("description2.html",user=current_user,a=int(a),mov=r)



@auth.route('/booking',methods=['GET','POST'])
def booking():
 
   
    movsel = request.form.get("movSel")

    r = db.session.execute("SELECT * from Shows where mov_id="+str(movsel))

    shows = r.fetchall()

    return render_template("booking.html",user=current_user,mov=shows,movsel=movsel)




@auth.route('/seats',methods=['GET','POST'])
def seats():

    
    show_sel  = request.form.get('showsel')

    r = db.session.execute('SELECT * from Seats')
    sho = db.session.execute('SELECT * from Seats where show_id='+str(show_sel))

    
    for i in range(1,101):
        new_booking = Seats(seat_no=i,show_id=int(show_sel))
        db.session.add(new_booking)
    
    #db.session.commit()
    
    
    
    
    seat = r.fetchall()

    show = sho.fetchall()

    seatcount = int(len(show)/2)

    return render_template("seats.html",user=current_user,seats=seat,sh=show,showsel=show_sel,seatcount=seatcount)

@auth.route('/confirmation',methods=['GET','POST'])
@login_required
def confirmation():


    
    li = request.form.getlist('seatList')

    sh = request.form.get('movsel')
    
    newli = request.form.getlist('seatList')
    
    newli.append(sh)
    

    listToStr = ','.join(map(str, newli))

    
    

    movid = str(db.session.execute("SELECT mov_id from Shows where id="+str(sh[0])).fetchall())

    mid =''
    for i in movid:
        if i.isnumeric():
            mid=mid+i


    mt = db.session.execute("SELECT * from Movie where id="+mid).fetchall()

    s = db.session.execute("SELECT * from Shows where id="+sh +" and mov_id="+mid).fetchall()

    r = db.session.execute('SELECT * from Seats').fetchall()

    sho = db.session.execute('SELECT * from Seats where show_id='+str(sh)).fetchall()




    if len(li) <= 10:
        return render_template("confirmation.html",user=current_user,li=li,sh=sh,lilen=len(li),movid=mt,strlist=listToStr,shows=s,m=mid) 
    else:
        flash('Please select less than 10 seats', category='error')
        return render_template("seats.html",user=current_user,seats=r,sh=sho,showsel=sh,seatcount=int(len(sho)/2))


@auth.route('/acknowledgement',methods=['GET','POST'])
def acknowledgement():

    l = request.form.get('confirm')

    user = current_user
    
    showsel = l[-1]

    
    li = request.form.get('confirm')
    
    li = li[:-2]

    li= li.split(',')


    if li:

            new_booking = Booking(user_id=user.id)
            db.session.add(new_booking)
            db.session.commit()
            flash('Booking done!',category='success')
    else:
        flash('Please select a seat',category="error")
    
    a = Booking.query.filter_by(user_id=user.id).all()
    
    a1 = a[len(a)-1]

    bid = a1.id

    u = User.query.filter_by(id=user.id).first()
    uname = u.first_name

    s=''
    if li:
        for i in li:
            a = db.session.execute('SELECT id from Seats where seat_no = '+ i+' and show_id = '+showsel ).fetchall()
            
    s = ','.join(map(str, li)) 
    
    if s:
        for i in li:

                db.session.execute('UPDATE Seats set book_id = '+str(bid)+' where id='+i)
                db.session.execute('UPDATE Seats set status="Booked" where id ='+i)
                db.session.commit()


    movid = str(db.session.execute("SELECT mov_id from Shows where id="+showsel).fetchall())

    mid =''
    for i in movid:
        if i.isnumeric():
            mid=mid+i


    mt = db.session.execute("SELECT * from Movie where id="+mid).fetchall()

    s1 = db.session.execute("SELECT * from Shows where id="+showsel +" and mov_id="+mid).fetchall()

    N = 7
    b =  ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))

    

   
    return render_template("final_page.html",user=current_user,li=li,a=a,showsel=showsel,lilen=len(li),s=s,uname=uname,mov=mt,shows=s1,b=b,bid=bid)


