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