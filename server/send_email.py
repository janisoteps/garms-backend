import os
import json
import random
import string
from hashlib import sha256
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def password_reset_email(db, User, data):
    email = data['email']
    username = data['username']
    user = User.query.filter_by(email=email).first()

    if user is None:
        return json.dumps(False)
    else:
        if user.username != username:
            return json.dumps(False)
        else:
            rand_string = ''.join(random.choice(string.ascii_letters) for m in range(10))
            token = sha256(rand_string.encode('utf-8')).hexdigest()
            user.pw_reset_token = token
            db.session.commit()
            print(token)

            message = Mail(
                from_email='garms-passwords@garms.io',
                to_emails=email,
                subject='Garms Password Reset',
                html_content=f'<h3>Hi {username},</h3><p>Click on the below link to reset your password:<p>'
                + f'<p><a href="https://garms.io/password-reset?t={token}">https://garms.io/password-reset?t={token}</a></p>'
                + f'<p>Cheers, Garms</p>'
            )
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)

                return json.dumps({
                    'status_code': response.status_code
                })
            except Exception as e:
                print(e)
                return json.dumps({
                    'error_message': e
                })
