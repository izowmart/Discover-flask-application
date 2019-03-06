from flask import render_template, redirect, flash, url_for, Blueprint

home_blueprint = Blueprint('home', __name__, template_folder='templates')


@home_blueprint.route('/')
def index():
    return render_template('home.html')


@home_blueprint.route('/about')
def about():
    return render_template('about.html')
