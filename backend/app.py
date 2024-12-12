from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Secret key for session management
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_fallback_secret_key')

# Secure cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Cookies only sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent access to cookies via JavaScript
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Helps mitigate CSRF attacks

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

        try:
            # Connect to the database
            conn = sqlite3.connect('database/data.db')
            cursor = conn.cursor()

            # Insert the new user with password
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
        except sqlite3.Error as e:
            return f"Database error: {e}", 500
        finally:
            conn.close()
        
        # Redirect to the success page
        return redirect(url_for('signup_success'))  # Corrected to 'signup_success'
    
    return render_template('signup.html')

# Success page after signup
@app.route('/signup/success')
def signup_success():
    return render_template('signup_success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Email and Password are required!", 400

        try:
            # Connect to the database
            conn = sqlite3.connect('database/data.db')
            cursor = conn.cursor()

            # Check if the user exists and the password matches
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                return render_template('login_success.html', name=user[1])  # Pass the name for a personalized message
            else:
                return "Invalid email or password!", 401
        except sqlite3.Error as e:
            return f"Database error: {e}", 500

    # If GET, render the login form
    return render_template('login.html')


if __name__ == "__main__":
    # Run with SSL (HTTPS)
    app.run(debug=True, ssl_context=('cert.pem', 'private.pem'))
