from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    if not name or not email:
        return "Name and Email are required!", 400  # Error response
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
    except sqlite3.Error as e:
        return f"Database error: {e}", 500  # Error response for database issues
    finally:
        conn.close()
    return f"Data submitted successfully! Name: {name}, Email: {email}"  # Success response


if __name__ == "__main__":
    app.run(debug=True)