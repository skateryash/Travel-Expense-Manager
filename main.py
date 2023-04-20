from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import LoginForm, RegisterForm, DataForm             # CreatePostForm, , , CommentForm
from flask_gravatar import Gravatar
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travels.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    admin = db.Column(db.Boolean)


class Records(UserMixin, db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DATE)
    jalgaon_memo = db.Column(db.Integer)
    jalgaon_luggage = db.Column(db.Integer)
    dhule_memo = db.Column(db.Integer)
    manmohan_memo = db.Column(db.Integer)
    nashik_luggage = db.Column(db.Integer)
    rokadi = db.Column(db.Integer)
    return_ = db.Column(db.Integer)
    advance = db.Column(db.Integer)
    disel = db.Column(db.Integer)
    other_expenses = db.Column(db.Integer)
    maintenance = db.Column(db.Integer)
    chart_comission = db.Column(db.Integer)


db.create_all()


def admin_only(f):
    @wraps(f)
    def wrapper_function(*args, **kwargs):
        if current_user.admin != 1:
            return abort(403)
        return f(*args, **kwargs)
    return wrapper_function


@login_manager.user_loader
def load_user(admin):
    return User.query.get(admin)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


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
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8),
            admin=form.admin.data
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


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/table", methods=["GET", "POST"])
@login_required
def table():
    all_records = Records.query.all()
    print(all_records[0])
    return render_template("table.html", all_records=all_records)


@app.route("/chart", methods=["GET", "POST"])
@login_required
@admin_only
def chart():
    return render_template("chart.html")


@app.route("/new-data", methods=["GET", "POST"])
@login_required
def add_new_data():
    form = DataForm()
    if form.validate_on_submit():
        new_data = Records(
            date=form.date.data,
            jalgaon_memo=form.jalgaon_memo.data,
            jalgaon_luggage=form.jalgaon_luggage.data,
            dhule_memo=form.dhule_memo.data,
            manmohan_memo=form.manmohan_memo.data,
            nashik_luggage=form.nashik_luggage.data,
            rokadi=form.rokadi.data,
            return_=form.return_.data,
            advance=form.advance.data,
            disel=form.disel.data,
            other_expenses=form.other_expenses.data,
            maintenance=form.maintenance.data,
            chart_comission=form.chart_comission.data,
        )
        # print(new_data.date)
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for("table"))
    return render_template("add-data.html", form=form)     #, form=form, logged_in=current_user.is_authenticated)


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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
