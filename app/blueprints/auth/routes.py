from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegistrationForm, LoginForm
from app.models import User
from app import db
from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.home'))
    return render_template('registration/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
    return render_template('registration/login.html', form=form)

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth_bp.route('/delete', methods=['POST'])
@login_required
def delete_account():
    user = User.query.filter_by(id=current_user.id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('main.home'))


