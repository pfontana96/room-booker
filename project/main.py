from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user

import sys
from datetime import datetime

from project.models import db, Room, Reservation

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    bookings = db.session.query(Room.name, Reservation.date_time).join(Reservation).filter(Reservation.user_id == current_user.id).all() 
    return render_template('profile.html', name=current_user.name, bookings=bookings)

@main.route('/book', methods=['POST'])
@login_required
def book():
    date = list(map(int, request.form.get('date').split('-'))) # [year, month, day]
    hour = list(map(int, request.form.get('hour').split(':'))) # [hour, minutes]
    date_time = datetime(year = date[0], month = date[1], day = date[2], hour = hour[0])

    today = datetime.now()
    if (date_time < today): # Caso de reserva en el pasado
        flash('Fecha de reserva pasada.')
        return redirect(url_for('main.profile'))

    subquery = db.session.query(Room.id).join(Reservation).filter(Reservation.date_time == date_time).all()
    results = [r for (r,) in subquery]
    available_rooms = Room.query.filter(~Room.id.in_(results)).all()

    return render_template('book.html', rooms=available_rooms, date_time=date_time)

@main.route('/reserve', methods=['POST'])
@login_required
def reserve():
    room_id = request.form.get('room_id')
    date_time = datetime.strptime(request.form.get('date_time'), '%Y-%m-%d %H:%M:%S') # Conversion a formato datetime (SQLAclhemy)
    user_id = current_user.id

    new_booking = Reservation(room_id=room_id, user_id=user_id, date_time=date_time)

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"success" : True}), 200

@main.route("/cancel", methods=['POST'])
@login_required
def cancel():
    # Data viene toda como un string 'Sala YYYY/MM/DD hh:mm:ss'
    room_name, date_time = request.form.get('id').split(' ', 1)
    room_id = db.session.query(Room.id).filter(Room.name == room_name).first()[0]
    date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S') # Conversion a formato datetime (SQLAclhemy)
    
    db.session.query(Reservation).filter(Reservation.user_id == current_user.id).filter( 
                                         Reservation.date_time == date_time).filter( 
                                         Reservation.room_id == room_id).delete()
    db.session.commit()

    return jsonify({"success" : True}), 200
