# Doctor Appointment System

A simple web application for booking doctor appointments built with Flask.

## Features

- User registration and login
- View list of doctors
- Book appointments with date and time
- View and cancel appointments
- SQLite database with SQLAlchemy
- Docker deployment ready

## Tech Stack

- Backend: Python Flask
- Database: SQLite with SQLAlchemy
- Frontend: HTML, CSS, Jinja templates
- Authentication: Flask sessions
- Deployment: Docker with Gunicorn

## Setup and Run

### Local Development

1. Install Python 3.11 or higher
2. Clone or download the project
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open http://localhost:5000 in your browser

### Docker Deployment

1. Build the Docker image:
   ```
   docker build -t doctor-appointment .
   ```
2. Run the container:
   ```
   docker run -p 5000:5000 doctor-appointment
   ```
3. Access at http://localhost:5000

### Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the following:
   - Runtime: Docker
   - Build Command: (leave empty)
   - Start Command: (leave empty, uses Dockerfile CMD)
4. Deploy

## Project Structure

```
├── app.py              # Main Flask application
├── models.py           # SQLAlchemy models
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── templates/          # Jinja templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── doctors.html
│   └── book.html
└── static/
    └── css/
        └── style.css
```

## Usage

1. Register a new account or login
2. View available doctors
3. Book an appointment by selecting date and time
4. View your appointments in the dashboard
5. Cancel appointments if needed

## Security Notes

- Change the SECRET_KEY in app.py for production
- Passwords are hashed using Werkzeug
- Basic session-based authentication
- Input validation on forms