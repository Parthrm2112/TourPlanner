from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_bcrypt import Bcrypt
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tourism.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"  # Needed for sessions

db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()  # Create tables if not exist


# ------------------ ROUTES ------------------ #

# Home route
@app.route('/')
def home():
    return render_template('index.html')


# Signup (GET -> show form, POST -> create user)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'})
    
    return render_template('signup.html')


# Login (GET -> show form, POST -> login check)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Store user in session
        session['user_id'] = user.id

        return jsonify({
            'message': 'Login successful',
            'redirect': '/dashboard'
        })

    return render_template('login.html')


# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # force login if not authenticated
    return render_template('dashboard.html')


# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


# ------------------ MAIN ------------------ #
if __name__ == '__main__':
    app.run(debug=True)
