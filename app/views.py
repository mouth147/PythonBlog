import os
from config import basedir, UPLOADED_PHOTOS_DEST
import markdown
from app import app, db, bcrypt, login_manager 
from flask.ext.login import login_required, login_user, current_user, logout_user
from werkzeug import secure_filename
from flask.ext.sqlalchemy import Pagination
from flask import render_template, redirect, url_for, flash, send_from_directory
from app.models import Post, User
from app.forms import loginform, CreateEntry, PhotoForm
from datetime import datetime
from sqlalchemy import desc

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    posts = Post.query.filter_by(published=True).order_by(desc(Post.timestamp)).paginate(page, 3,True)
    return render_template('index.html',
                           posts = posts)

@app.route('/post/<slug>')
def detail(slug):
    posts = Post.query.filter_by(slug=slug).first()
    if posts is None:
        return render_template('404.html', title = "Oops! No post!")
    return render_template('detail.html',
                           posts = posts, title = posts.title)

@app.route('/edit/<slug>', methods = ['GET', 'POST'])
@login_required
def edit(slug):
    post = Post.query.filter_by(slug=slug).first()
    form = CreateEntry(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.published = form.published.data
        post.timestamp = datetime.utcnow()
        post.create_slug()
        db.session.commit()
        if form.published.data:
            return redirect(url_for('detail',slug = post.slug))
        else:
            flash('Entry saved!')
            return redirect(url_for('admin'))
    return render_template('create.html', form = form, title = "Edit Post", action = "Edit", value =
                           "Save Post")

@app.route('/delete/<slug>')
@login_required
def delete(slug):
    post = Post.query.filter_by(slug = slug).first()
    db.session.delete(post)
    db.session.commit()
    flash('Entry deleted!')
    return redirect(url_for('admin'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (current_user.is_authenticated):
        return redirect(url_for('admin'))

    form = loginform()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember = True)
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('admin'))
    return render_template('login.html', form = form)

@app.route('/admin')
@login_required
def admin():
    posts = Post.query.filter_by(published = True).order_by(desc(Post.timestamp))
    drafts = Post.query.filter_by(published = False)
    return render_template('adminhome.html', posts = posts, drafts = drafts)

@app.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
    form = CreateEntry()
    if form.validate_on_submit():
        p = Post(title = form.title.data, body = form.body.data, published = form.published.data,
                 timestamp = datetime.utcnow())
        p.create_slug()
        db.session.add(p)
        db.session.commit()
        if form.published.data:
            return redirect(url_for('detail', slug = p.slug))
        else:
            flash('Entry saved as draft!')
            return redirect(url_for('admin'))
    return render_template('create.html', form = form, title = "New Entry", action = "New", value =
                          "Create Post")

@app.route('/logout')
@login_required
def logout():
    user = current_user
    form = loginform()
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    form = loginform()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title = "Oops, maybe next time")

@app.route('/uploads', methods = ['GET', 'POST'])
@login_required
def upload():
    form = PhotoForm()
    imgs = os.listdir(UPLOADED_PHOTOS_DEST)
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save(os.path.join(UPLOADED_PHOTOS_DEST, filename))
        imgs = os.listdir(UPLOADED_PHOTOS_DEST)
        return render_template('uploads.html', form = form, imgs = imgs)
    return render_template('uploads.html', form = form, imgs = imgs)

@app.route('/about')
def about():
    return render_template('about.html', title = "About This Blog")
