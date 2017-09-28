# -*- coding: utf-8 -*-
from itsdangerous import URLSafeTimedSerializer
import smtplib
from flask import current_app

def send_email(app, to, msg):
    with app.app_context():
        server = smtplib.SMTP(current_app.config['EMAIL_CONFIRM_SMTP'], current_app.config['EMAIL_CONFIRM_SMTP_PORT'])
        server.starttls()
        server.ehlo()
        server.login(current_app.config['EMAIL_CONFIRM_USERNAME'], current_app.config['EMAIL_CONFIRM_PASSWORD'])
        server.sendmail(current_app.config['EMAIL_CONFIRM_USERNAME'], to, msg)
        server.quit()
        server.close()

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

