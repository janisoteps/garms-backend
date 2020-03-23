import os
import json
import random
import string
from hashlib import sha256
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def password_reset_email(db, User, data):
    email = data['email']
    user = User.query.filter_by(email=email).first()

    if user is None:
        return json.dumps(False)
    else:
        rand_string = ''.join(random.choice(string.ascii_letters) for m in range(10))
        token = sha256(rand_string.encode('utf-8')).hexdigest()
        user.pw_reset_token = token
        db.session.commit()
        print(token)

        message = Mail(
            from_email='garms-login@garms.io',
            to_emails=email,
            subject='Garms Password Reset',
            html_content=f'<h3>Hi {user.username},</h3><p>Click on the below link to reset your password:<p>'
            + f'<p><a href="https://garms.io/password-reset?t={token}">https://garms.io/password-reset?t={token}</a></p>'
            + f'<p>Happy Shopping!</p><p>Garms</p>'
        )
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)

            return json.dumps({
                'response': response.status_code
            })
        except Exception as e:
            print(e)
            return json.dumps({
                'response': e
            })


def registration_email(data):
    email = data['email']
    username = data['username']

    if email is None:
        return False
    else:
        message = Mail(
            from_email='garms@garms.io',
            to_emails=email,
            subject='Welcome to Garms',
            html_content=f'<h3>Welcome, {username} :)</h3>'
                         + f'<p>You are now all set to be a part of the fashion revolution.</p>'
                         + f'<p>Happy Shopping!</p><p>Garms</p>'
        )
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            return response.status_code
        except Exception as e:
            print(e)
            return e
