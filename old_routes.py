@app.route('/change_email', methods=['POST'])
def change_email():
    if request.method == 'POST':
        new_email = request.form['new_email']
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("UPDATE users SET email = %s WHERE email = %s", (new_email, session['user']))
        conn.commit()
        cur.close()
        conn.close()
        session['email'] = new_email
        return redirect(url_for('profile'))
    

    @app.route('/change_username', methods=['POST'])
def change_username():
    if request.method == 'POST':
        new_username = request.form['new_username']
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("UPDATE gebruikers SET username = %s WHERE email = %s", (new_username, session['email']))
        conn.commit()
        cur.close()
        conn.close()
        session['user'] = new_username
        return redirect(url_for('profile'))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        token = 'example_token'
        reset_link = url_for('reset_password', token=token, _external=True)
        return "Password reset link sent to your email."
    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        return "Password reset successful. Redirect to login page."
    return render_template('reset_password.html', token=token)

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

@app.route('/film/popular')
def movie_popular():
    movie_list = movie.get_popular_details()
    return render_template('index.html', movies=movie_list, movieapi=movie)


@app.route('/serie/popular')
def serie_popular():
    serie_list = serie.get_popular_details()
    return render_template('index.html', movies=serie_list, movieapi=serie)

@app.route('/film/popular/<genre>')
def movie_popular(genre):
    movie_list = movie.get_details_filtered_on_genre(genre)
    return render_template('index.html', movies=movie_list, movieapi=movie, genre=genre)


@app.route('/serie/popular/<genre>')
def serie_popular(genre):
    serie_list = serie.get_details_filtered_on_genre(genre)
    return render_template('index.html', movies=serie_list, movieapi=serie, genre=genre)

@app.route('/change_email', methods=['POST'])
def change_email():
    if request.method == 'POST':
        new_email = request.form['new_email']
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("UPDATE users SET email = %s WHERE email = %s", (new_email, session['user']))
        conn.commit()
        cur.close()
        conn.close()
        session['email'] = new_email
        return redirect(url_for('profile'))