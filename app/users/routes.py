from flask import render_template, request, redirect, url_for,session,flash,abort,Blueprint
from app.model import Post,User
from flask_login import current_user,login_required,login_user,logout_user
from app import db,bcrypt
from app.users.forms import (Registerform,loginform,Updateaccountform,ResetPasswordForm,requestresetform)
from app.users.utils import save_picture, send_reset_email

users = Blueprint('users',__name__)

@users.route('/register',methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
            return redirect(url_for("main.home"))
    form = Registerform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user = User(username = form.username.data, email= form.email.data,password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! you are now able to login","success")
        return redirect(url_for("users.login"))
    return render_template('register.html', title='Register',form=form)

@users.route('/login',methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))  
        else:   
          flash("login unsuccefil,please check the email and password", "danger")
    return render_template('login.html', title='Login',form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account",methods=["GET","POST"])
@login_required
def account():
    form = Updateaccountform()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("your account has been updated","success")
        return redirect(url_for('users.account'))
    else:
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='img/' + current_user.image_file  )
    return render_template("account.html", title="account", image_file=image_file, form=form)

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page',1,type =int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page =page,per_page =3)
    return render_template('user_posts.html', posts=posts,user=user)

@users.route('/reset_password', methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = requestresetform() 
    if form.validate_on_submit():  
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user is not None:
            send_reset_email(user)
        flash('If that email is registered, an email with reset instructions has been sent.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        flash("Your password has been updated! You are now able to log in.", "success")
        return redirect(url_for("users.login"))
    return render_template('reset_token.html', title='Reset Password', form=form)