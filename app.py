from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from datetime import date, datetime
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import LoginForm, RegisterForm, DataForm
from flask_gravatar import Gravatar
from functools import wraps
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
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


class Income(UserMixin, db.Model):
    __tablename__ = "income"
    date = db.Column(db.DATE, primary_key=True)
    jalgaon_memo = db.Column(db.Integer)
    jalgaon_luggage = db.Column(db.Integer)
    dhule_memo = db.Column(db.Integer)
    manmohan_memo = db.Column(db.Integer)
    nashik_luggage = db.Column(db.Integer)
    rokadi = db.Column(db.Integer)
    return_ = db.Column(db.Integer)

    lab_payment = db.Column(db.Integer)
    difference = db.Column(db.Integer)


class Expenses(UserMixin, db.Model):
    __tablename__ = "expenses"
    date = db.Column(db.DATE, primary_key=True)
    advance = db.Column(db.Integer)
    diesel = db.Column(db.Integer)
    other_expenses = db.Column(db.Integer)
    maintenance = db.Column(db.Integer)
    chart_commission = db.Column(db.Integer)

    drivers_salary = db.Column(db.Integer)
    cleaner_salary = db.Column(db.Integer)
    hinduza_finance = db.Column(db.Integer)
    road_tax = db.Column(db.Integer)
    gprs = db.Column(db.Integer)
    bedsheet_washing = db.Column(db.Integer)
    jay_ambe = db.Column(db.Integer)
    pigmi = db.Column(db.Integer)
    staff_payment = db.Column(db.Integer)


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


def get_monthly_data(month, year, table):
    # print(month, year)
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if month in num:
        month = '0' + str(month)
    query = f'''
                    SELECT *
                    FROM {table}
                    WHERE strftime('%m', date) = '{month}'
                    AND strftime('%Y', date) = '{year}'
                    ORDER BY date ASC;
                '''
    # print(query)

    # SQLAlchemy connectable
    cnx = create_engine(os.getenv('DATABASE_URL')).connect()

    # table named 'records' will be returned as a dataframe.
    dataframe = pd.read_sql_query(query, con=cnx)

    return dataframe


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    income_category = ['Jalgaon memo', 'Jalgaon luggage', 'Dhule office memo', 'Manmohan memo', 'Nashik office luggage',
                       'Rokadi', 'Return ticket payment', 'Lab payment', 'Difference amount of payment']
    expenses_category = ['Advance', 'Diseal', 'Other Expenses', 'Maintainance', 'Chart commision', 'Drivers payment',
                         'Cleaner Payment', 'Hinduza finance', 'Road tax', 'GPRS', 'Bed sheet washing', 'Jay ambe',
                         'pigmi', 'Staff payment']

    income_df = get_monthly_data(month=date.today().month, year=date.today().year, table="income").iloc[:, 1:].sum().to_frame().reset_index()
    # income_df = get_monthly_data(month="03", year="2023", table="income").iloc[:, 1:].sum().to_frame().reset_index()
    income_df.columns = ['Column', 'Value']
    income_df['Column'] = income_category
    income_df.loc[len(income_df)] = ['Total', income_df['Value'].sum()]

    expenses_df = get_monthly_data(month=date.today().month, year=date.today().year, table="expenses").iloc[:, 1:].sum().to_frame().reset_index()
    # expenses_df = get_monthly_data(month="03", year="2023", table="expenses").iloc[:, 1:].sum().to_frame().reset_index()
    expenses_df.columns = ['Column', 'Value']
    expenses_df['Column'] = expenses_category
    expenses_df.loc[len(expenses_df)] = ['Total', expenses_df['Value'].sum()]

    # print(income_df)
    # print(type(expenses_df))

    return render_template("dashboard.html", user=current_user, income=income_df, expenses=expenses_df)


def monthly_data(month, year):
    category = ['Date', 'Jalgaon memo', 'Jalgaon luggage', 'Dhule memo', 'Manmohan memo', 'Nashik luggage',
                'Rokadi', 'Return Ticket', 'Advance', 'Diseal', 'Other Expenses', 'Maintainance', 'Chart commision']
    income_df = get_monthly_data(month=month, year=year, table="income").iloc[:, :8]
    expenses_df = get_monthly_data(month=month, year=year, table="expenses").iloc[:, 1:6]

    df = pd.concat([income_df, expenses_df], axis=1)
    df.columns = category
    df = pd.concat([df, df.sum(numeric_only=True).rename('Total').to_frame().T], ignore_index=True)

    df.fillna('Total', inplace=True)

    return df


@app.route("/table", methods=["GET", "POST"])
@login_required
def table():
    df = monthly_data(month=date.today().month, year=date.today().year)

    if request.method == "POST":
        month = request.form.get("mpicker")[5:]
        year = request.form.get("mpicker")[:4]
        df = monthly_data(month=month, year=year)
        return render_template("table.html", df=df)

    return render_template("table.html", df=df)


@app.route("/chart", methods=["GET", "POST"])
@login_required
def chart():
    return render_template("chart.html")


@app.route("/new-data", methods=["GET", "POST"])
@login_required
def add_new_data():
    form = DataForm()
    if form.validate_on_submit():
        new_income_data = Income(
            date=form.date.data,
            jalgaon_memo=form.jalgaon_memo.data,
            jalgaon_luggage=form.jalgaon_luggage.data,
            dhule_memo=form.dhule_memo.data,
            manmohan_memo=form.manmohan_memo.data,
            nashik_luggage=form.nashik_luggage.data,
            rokadi=form.rokadi.data,
            return_=form.return_.data,
            lab_payment=form.lab_payment.data,
            difference=form.difference.data
        )

        new_expenses_data = Expenses(
            date=form.date.data,
            advance=form.advance.data,
            diesel=form.diesel.data,
            other_expenses=form.other_expenses.data,
            maintenance=form.maintenance.data,
            chart_commission=form.chart_commission.data,
            drivers_salary=form.drivers_salary.data,
            cleaner_salary=form.cleaner_salary.data,
            hinduza_finance=form.hinduza_finance.data,
            road_tax=form.road_tax.data,
            gprs=form.gprs.data,
            bedsheet_washing=form.bedsheet_washing.data,
            jay_ambe=form.jay_ambe.data,
            pigmi=form.pigmi.data,
            staff_payment=form.staff_payment.data,
        )

        db.session.add(new_income_data)
        db.session.add(new_expenses_data)
        db.session.commit()
        return redirect(url_for("table"))
    return render_template("add-data.html", form=form)  # , form=form, logged_in=current_user.is_authenticated)


@app.route("/edit-post/<string:date_value>", methods=["GET", "POST"])
@login_required
def edit_record(date_value):
    date_obj = datetime.strptime(date_value, "%Y-%m-%d").date()  # Convert the string to a Python date object
    income_to_edit = Income.query.get(date_obj)
    expenses_to_edit = Expenses.query.get(date_obj)

    edit_form = DataForm(
        date=income_to_edit.date,
        jalgaon_memo=income_to_edit.jalgaon_memo,
        jalgaon_luggage=income_to_edit.jalgaon_luggage,
        dhule_memo=income_to_edit.dhule_memo,
        manmohan_memo=income_to_edit.manmohan_memo,
        nashik_luggage=income_to_edit.nashik_luggage,
        rokadi=income_to_edit.rokadi,
        return_=income_to_edit.return_,
        lab_payment=income_to_edit.lab_payment,
        difference=income_to_edit.difference,

        advance=expenses_to_edit.advance,
        diesel=expenses_to_edit.diesel,
        other_expenses=expenses_to_edit.other_expenses,
        maintenance=expenses_to_edit.maintenance,
        chart_commission=expenses_to_edit.chart_commission,
        drivers_salary=expenses_to_edit.drivers_salary,
        cleaner_salary=expenses_to_edit.cleaner_salary,
        hinduza_finance=expenses_to_edit.hinduza_finance,
        road_tax=expenses_to_edit.road_tax,
        gprs=expenses_to_edit.gprs,
        bedsheet_washing=expenses_to_edit.bedsheet_washing,
        jay_ambe=expenses_to_edit.jay_ambe,
        pigmi=expenses_to_edit.pigmi,
        staff_payment=expenses_to_edit.staff_payment,
    )

    if edit_form.validate_on_submit():
        income_to_edit.date = edit_form.date.data
        income_to_edit.jalgaon_memo = edit_form.jalgaon_memo.data
        income_to_edit.jalgaon_luggage = edit_form.jalgaon_luggage.data
        income_to_edit.dhule_memo = edit_form.dhule_memo.data
        income_to_edit.manmohan_memo = edit_form.manmohan_memo.data
        income_to_edit.nashik_luggage = edit_form.nashik_luggage.data
        income_to_edit.rokadi = edit_form.rokadi.data
        income_to_edit.return_ = edit_form.return_.data
        income_to_edit.lab_payment = edit_form.lab_payment.data
        income_to_edit.difference = edit_form.difference.data

        expenses_to_edit.date = edit_form.date.data
        expenses_to_edit.advance = edit_form.advance.data
        expenses_to_edit.diesel = edit_form.diesel.data
        expenses_to_edit.other_expenses = edit_form.other_expenses.data
        expenses_to_edit.maintenance = edit_form.maintenance.data
        expenses_to_edit.chart_commission = edit_form.chart_commission.data
        expenses_to_edit.drivers_salary = edit_form.drivers_salary.data
        expenses_to_edit.cleaner_salary = edit_form.cleaner_salary.data
        expenses_to_edit.hinduza_finance = edit_form.hinduza_finance.data
        expenses_to_edit.road_tax = edit_form.road_tax.data
        expenses_to_edit.gprs = edit_form.gprs.data
        expenses_to_edit.bedsheet_washing = edit_form.bedsheet_washing.data
        expenses_to_edit.jay_ambe = edit_form.jay_ambe.data
        expenses_to_edit.pigmi = edit_form.pigmi.data
        expenses_to_edit.staff_payment = edit_form.staff_payment.data

        db.session.commit()
        return redirect(url_for("table"))

    return render_template("edit-data.html", form=edit_form)


@app.route("/delete/<string:date_value>")
@login_required
def delete_record(date_value):
    date_obj = datetime.strptime(date_value, "%Y-%m-%d").date()  # Convert the string to a Python date object
    income_to_delete = Income.query.get(date_obj)
    expenses_to_delete = Expenses.query.get(date_obj)
    db.session.delete(income_to_delete)
    db.session.delete(expenses_to_delete)
    db.session.commit()
    return redirect(url_for('table'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
