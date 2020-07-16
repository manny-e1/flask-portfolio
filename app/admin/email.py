from flask import url_for, current_app
from flask_mail import Message
from app import mail
from threading import Thread
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(user):
    token = user.generate_token()
    msg = Message('[cms-portfolio]Email Confirmation Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body =  f'''To activate your account, visit the following link:
        { url_for('admin.confirm_mail', token=token, _external=True) }
        If you did not make this request then simply ignore this email and no changes will be made.
        '''
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_change_email(user,email):
    token = user.generate_email_change_token(email)
    msg=Message('[Bloggers]Email Confirmation Request',
                sender=os.environ.get('MAIL_USERNAME'),
                recipients=[email],
                )
    msg.body = f'''To activate your email, visit the following link:
    { url_for('admin.change_email', token=token, _external=True) }
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
