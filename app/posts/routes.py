from flask import render_template, request, redirect, url_for,session,flash,abort,Blueprint
from app.model import User, Post
from app import db
from flask_login import current_user,login_required
from app.posts.forms import postform
posts = Blueprint('posts',__name__)

@posts.route("/post/new", methods =["GET","POST"])
@login_required
def new_post():
    form = postform()
    if form.validate_on_submit():
        post = Post(title = form.title.data,content = form.content.data,author =current_user)
        db.session.add(post)
        db.session.commit()
        flash("You post has been created!",'success')
        return redirect(url_for('main.home'))
    return render_template("create_post.html", title = "New Post",form = form, legend = "New post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title= "Post",post = post)


@posts.route("/post/<int:post_id>/update",methods =["GET","POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = postform()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('your post has been updated','success')
        return redirect(url_for("posts.post",post_id = post.id))
    elif request.method == "GET":    
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html",title='Update post', form=form,post = post, legend ="Update post")


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required  # remove if you don't use Flask-Login
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    print(f"Deleting post {post.id}: {post.title}")

    db.session.delete(post)
    db.session.commit()
    print("Remaining posts:", Post.query.count())

    flash('Post deleted.', 'success')
    return redirect(url_for('main.home')) 