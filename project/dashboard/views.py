from flask import render_template, redirect, url_for, flash, Blueprint, session, request
from flask_login import login_required, current_user

from project.models import Article, db
from .forms import ArticleForm

dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard_blueprint.route('/articles')
def articles():
    articles = Article.query.all()

    return render_template('articles.html', articles=articles)


@dashboard_blueprint.route('/article/<string:id>')
def article(id):
    articles = Article.query.filter_by(id=id).first()

    return render_template('article.html', article=articles)


# Dashboard
@dashboard_blueprint.route('/dashboard')
@login_required
def dashboard():
    articles = Article.query.all()
    if articles:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found!'
    return render_template('dashboard.html', msg=msg)


# Add article
@dashboard_blueprint.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        article = Article(form.title.data, form.body.data, current_user.id)
        db.session.add(article)
        db.session.commit()
        flash('Article Created', 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('add_article.html', form=form)


# Edit Article
@dashboard_blueprint.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    form = ArticleForm(request.form)
    article = Article.query.filter_by(id=id).first()
    if article:
        # Populate article form fields
        form.title.data = article.title
        form.body.data = article.body

        if request.method == 'POST' and form.validate():
            article.title = request.form['title']
            article.body = request.form['body']
            db.session.commit()
            flash('Article Updated', 'success')
            return redirect(url_for('dashboard.dashboard'))

    return render_template('edit_article.html', form=form, article=article)


@dashboard_blueprint.route('/delete_article/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_article(id):
    article = Article.query.filter_by(id=id).first()
    db.session.delete(article)
    db.session.commit()
    flash('Article Deleted', 'success')
    return redirect(url_for('dashboard.dashboard'))
