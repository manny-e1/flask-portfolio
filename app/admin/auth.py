from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from werkzeug.urls import url_parse
from app.admin.forms import LoginForm, RegistrationForm, UpdateAccountForm,ChangePasswordForm
from app.models import User
from app.admin.email import send_email, send_change_email
from app.decorators import check_confirmed, isAdmin
from cloudinary.uploader import upload
from . import admin


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    if User.query.filter_by(username="adminaman").first() == None:
        user = User(username=current_app.config['ADMIN_USERNAME'], email=current_app.config['ADMIN_EMAIL'],
                     isAdmin=True, confirmed=True)
        user.set_password(current_app.config['ADMIN_PASSWORD'])
        db.session.add(user)
        db.session.commit()
        send_email(user)
        flash('A confirmation email has been sent to you by email.', 'info')
        return redirect(url_for('admin.login'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('admin.login'))
            if not user.check_password(form.password.data):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('admin.login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('admin.index')
            return redirect(next_page)
    return render_template('admin/login.html',  form=form)


@admin.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@admin.route('/index')
@login_required
@check_confirmed
def index():
    return render_template('admin/home.html')


@admin.route('/user/register', methods=['GET', 'POST'])
@login_required
@check_confirmed
@isAdmin
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data,
                        isAdmin=form.isAdmin.data, confirmed=form.confirmed.data, isFriend=form.isFriend.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            send_email(user)
            flash('A confirmation email has been sent to you by email.', 'info')
            return redirect(url_for('admin.login'))

    return render_template('admin/signup.html', form=form)


@admin.route('/confirm/<token>')
@login_required
def confirm_mail(token):
    if current_user.confirmed:
        return redirect(url_for('admin.index'))
    if current_user.confirm_email(token):
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('admin.index'))


@admin.route('/unconfirmed')
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('admin.index'))
    return render_template('admin/unconfirmed.html')


@admin.route('/confirm')
@login_required
def resend_confirmation():
    send_email(current_user)
    flash('A new confirmation email has been sent to you by email.', 'info')
    return redirect(url_for('admin.index'))


@admin.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.', 'info')
    else:
        flash('Invalid request.', 'error')
    return redirect(url_for('admin.account'))


@admin.route("/account/<int:id>", methods=['GET', 'POST'])
@login_required
@check_confirmed
def account(id):
    user = User.query.get(id)
    form = UpdateAccountForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.picture.data:
                picture = upload(form.picture.data)
                user.image = picture['url']
                flash('Your picture has been updated', 'info')
            user.username = form.username.data
            if form.username.data != user.username:
                user.username = form.username.data
                flash('Your username has been updated', 'info')
            if form.email.data != user.email:
                newemail = form.email.data.lower()
                # send_change_email(user=current_user, email=newemail)
                user.email = newemail
                flash('A confirmation email has been sent to you by email.', 'info')
            db.session.commit()
            return redirect(request.referrer)
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    image = user.image
    return render_template('admin/account.html', title='Account',
                           image_file=image, form=form)
@admin.route('/user/change_password', methods=['GET', 'POST'])
@login_required
@check_confirmed
def change_password():
    form = ChangePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated.', 'info')
        return redirect(url_for('admin.index'))
    return render_template('admin/change_password.html', form=form)

@admin.route('/user/delete/<int:id>',  methods=["GET","POST"])
@login_required
@isAdmin
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.users'))