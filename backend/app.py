from flask import Flask, request, render_template, redirect, url_for, session, flash
import sqlite3
import os
import bcrypt
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

csrf = CSRFProtect(app)

# Secret key for session management
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_fallback_secret_key')

# Secure cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Cookies only sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent access to cookies via JavaScript
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Helps mitigate CSRF attacks
app.config['WTF_CSRF_ENABLED'] = True  # Should be True (default)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            return "Name, Email, and Password are required!", 400

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = sqlite3.connect('database/data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('signup_success'))
    return render_template('signup.html')

# Success page after signup
@app.route('/signup/success')
def signup_success():
    return render_template('signup_success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = sqlite3.connect('database/data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            session['user'] = user[0]
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        else:
            error = "Invalid credentials, please try again."

    return render_template('login.html', error=error)  # Pass the error to the template

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Run with SSL (HTTPS)
    app.run(debug=True, ssl_context=('cert.pem', 'private.pem'))