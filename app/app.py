from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # the key voor de sessie

db_params = {
    'dbname': 'the database name', 'user': 'the username', 'password': 'the password', 'host': 'the host',
    'port': 'the port'}


# moet nog aangepast worden naar de info van de database

@app.route('/')
def index():
    return render_template('main.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'post':
        email = request.form['email']
        password = request.form['password']
        # kan meer info onder zetten als we meer toevoegen

        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['user'] = user[0]
            return redirect(url_for('profile'))
        else:
            return "Wrong email or password"


@app.routes('/profile')
def profile():
    if 'user' in session:
        return f"profile - logged in as {session['user']}"
    else:
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)
