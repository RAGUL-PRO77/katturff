from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Create DB table if not exists
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            phone TEXT,
            email TEXT,
            category TEXT,
            location TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')  # move HTML into templates folder

@app.route('/submit', methods=['POST'])
def submit():
    data = (
        request.form['first_name'],
        request.form['phone'],
        request.form['email'],
        request.form['category'],
        request.form['location'],
        request.form['message']
    )

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO enquiries 
        (first_name, phone, email, category, location, message)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()
    return redirect(url_for('enquiries', email=request.form['email']))

@app.route('/enquiries')
def enquiries():
    email = request.args.get('email')  # get email from URL

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    if email:
        cursor.execute("SELECT * FROM enquiries WHERE email = ?", (email,))
    else:
        cursor.execute("SELECT * FROM enquiries")
    
    data = cursor.fetchall()
    conn.close()

    return render_template('enquiries.html', data=data, email=email)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)