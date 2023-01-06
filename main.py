from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import LoginForm, RegisterForm             # CreatePostForm, , , CommentForm
from flask_gravatar import Gravatar
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travels.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


##CONFIGURE TABLES
# DataBase Visualize Diagram: https://github.com/SadSack963/day-69_blog_with_users/blob/master/docs/Class_Diagram.png
# class BlogPost(db.Model):
#     __tablename__ = "blog_posts"
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     subtitle = db.Column(db.String(250), nullable=False)
#     date = db.Column(db.String(250), nullable=False)
#     body = db.Column(db.Text, nullable=False)
#     img_url = db.Column(db.String(250), nullable=False)
#
#     # Create Foreign Key, "users.id" the users refers to the tablename of User.
#     author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     # Create reference to the User object, the "posts" refers to the posts property in the User class.
#     author = relationship("User", back_populates="posts")  # db.Column(db.String(250), nullable=False)
#
#     comments = relationship("Comment", back_populates="post")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))

    # This will act like a List of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    # posts = relationship("BlogPost", back_populates="author")
    # comments = relationship("Comment", back_populates="commenter")


# class Comment(db.Model):
#     __tablename__ = "comments"
#     id = db.Column(db.Integer, primary_key=True)
#     comment_body = db.Column(db.Text, nullable=False)
#     date = db.Column(db.String(250), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"), nullable=False)
#     post = db.relationship("BlogPost", back_populates="comments")
#     commenter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     commenter = db.relationship("User", back_populates="comments")


db.create_all()


def admin_only(f):
    @wraps(f)
    def wrapper_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return wrapper_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("You have already signed up with this email, login instead")
            return redirect(url_for("login"))

        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email address doesn't exist, please try again.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Incorrect password, please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("dashboard"))

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# @app.route("/post/<int:post_id>", methods=["GET", "POST"])
# def show_post(post_id):
#     requested_post = BlogPost.query.get(post_id)
#     form = CommentForm()
#     if form.validate_on_submit():
#         if not current_user.is_authenticated:
#             flash("You need to login or register to comment.")
#             return redirect(url_for("login"))
#
#         new_comment = Comment(
#             comment_body=form.comment_body.data,
#             date=date.today(),
#             commenter=current_user,
#             post=requested_post
#         )
#         db.session.add(new_comment)
#         db.session.commit()
#     return render_template("post.html", post=requested_post, logged_in=current_user.is_authenticated, form=form)


@app.route("/about")
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("testing.html")


# @app.route("/contact")
# def contact():
#     return render_template("contact.html", logged_in=current_user.is_authenticated)
#
#
# @app.route("/new-post", methods=["GET", "POST"])
# @login_required
# @admin_only
# def add_new_post():
#     form = CreatePostForm()
#     if form.validate_on_submit():
#         new_post = BlogPost(
#             title=form.title.data,
#             subtitle=form.subtitle.data,
#             body=form.body.data,
#             img_url=form.img_url.data,
#             author=current_user,
#             date=date.today().strftime("%B %d, %Y")
#         )
#         db.session.add(new_post)
#         db.session.commit()
#         return redirect(url_for("get_all_posts"))
#     return render_template("make-post.html", form=form, logged_in=current_user.is_authenticated)
#
#
# @app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
# @login_required
# @admin_only
# def edit_post(post_id):
#     post = BlogPost.query.get(post_id)
#     edit_form = CreatePostForm(
#         title=post.title,
#         subtitle=post.subtitle,
#         img_url=post.img_url,
#         author=post.author,
#         body=post.body
#     )
#     if edit_form.validate_on_submit():
#         post.title = edit_form.title.data
#         post.subtitle = edit_form.subtitle.data
#         post.img_url = edit_form.img_url.data
#         post.author = request.form.get("author")          # edit_form.author.data
#         post.body = edit_form.body.data
#         db.session.commit()
#         return redirect(url_for("show_post", post_id=post.id))
#
#     return render_template("make-post.html", form=edit_form, logged_in=current_user.is_authenticated)
#
#
# @app.route("/delete/<int:post_id>")
# @login_required
# @admin_only
# def delete_post(post_id):
#     post_to_delete = BlogPost.query.get(post_id)
#     db.session.delete(post_to_delete)
#     db.session.commit()
#     return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True)
