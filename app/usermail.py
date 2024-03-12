from flask import render_template, current_app
from flask_mail import Message
from app import app, mail
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, sender, recipients, text_body, html_body):
    """
    Send an email with the specified subject, sender, recipients, text body, and HTML body.
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    """
    Sends a password reset email to the specified user.

    Parameters:
    - user: the user object for whom the password reset email will be sent
    """
    token = user.get_reset_password_token()
    send_mail(
        "[Groepswerk]Password Reset",
        sender=current_app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("reset_password_new.txt", user=user, token=token),
        html_body=render_template("reset_password_new.html", user=user, token=token),
    )
