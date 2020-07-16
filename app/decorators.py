from functools import wraps
from flask import flash, redirect,url_for, request, render_template
from flask_login import current_user
def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('admin.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function
def isAdmin(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if current_user.isAdmin is False:
			flash('You are not authorized to access this page', 'danger')
			return render_template('admin/unauthorized.html')
		return func(*args,**kwargs)
	return decorated_function
