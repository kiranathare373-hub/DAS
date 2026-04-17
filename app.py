from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Doctor, Appointment
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables and seed doctors
with app.app_context():
    db.create_all()
    # Seed some doctors if not exist
    if not Doctor.query.first():
        doctors = [
            Doctor(name='Dr. John Smith', specialty='Cardiology', email='john@example.com'),
            Doctor(name='Dr. Jane Doe', specialty='Dermatology', email='jane@example.com'),
            Doctor(name='Dr. Bob Johnson', specialty='Orthopedics', email='bob@example.com'),
        ]
        for doctor in doctors:
            db.session.add(doctor)
        db.session.commit()

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    appointments = Appointment.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, appointments=appointments)

@app.route('/doctors')
def doctors():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)

@app.route('/book/<int:doctor_id>', methods=['GET', 'POST'])
def book(doctor_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    doctor = Doctor.query.get_or_404(doctor_id)
    if request.method == 'POST':
        date_str = request.form['date']
        time_str = request.form['time']
        try:
            app_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            app_time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            flash('Invalid date or time format', 'error')
            return redirect(url_for('book', doctor_id=doctor_id))
        
        # Check if slot is available
        existing = Appointment.query.filter_by(doctor_id=doctor_id, date=app_date, time=app_time).first()
        if existing:
            flash('This time slot is already booked', 'error')
            return redirect(url_for('book', doctor_id=doctor_id))
        
        appointment = Appointment(user_id=session['user_id'], doctor_id=doctor_id, date=app_date, time=app_time)
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('dashboard'))
    today = date.today()
    return render_template('book.html', doctor=doctor, today=today)

@app.route('/cancel/<int:appointment_id>')
def cancel(appointment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.user_id != session['user_id']:
        flash('Unauthorized', 'error')
        return redirect(url_for('dashboard'))
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment cancelled', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)