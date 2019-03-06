from flask import request, render_template, url_for, Blueprint, redirect, session, flash
from flask_login import login_user, login_required, logout_user
from .forms import LoginForm, RegisterForm
from project.models import User, bcrypt, db
users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.username == request.form['username']).first()
        if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            session['logged_in'] = True
            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            error = 'Invalid username or password.'

    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered you can log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


# Logout
@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    flash('You are now logged out', 'success')
    return redirect(url_for('users.login'))
