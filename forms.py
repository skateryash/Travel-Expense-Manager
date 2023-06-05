from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, validators, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import NumberInput
from wtforms.fields import DateField


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    admin = BooleanField("Admin")
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class DataForm(FlaskForm):
    # Income fields
    date = DateField('Start Date', validators=[validators.Optional()], default=datetime.today)
    jalgaon_memo = IntegerField("Jalgaon Memo", widget=NumberInput(), default=0)
    jalgaon_luggage = IntegerField("Jalgaon Luggage", widget=NumberInput(), default=0)
    dhule_memo = IntegerField("Dhule Memo", widget=NumberInput(), default=0)
    manmohan_memo = IntegerField("Manmohan Memo", widget=NumberInput(), default=0)
    nashik_luggage = IntegerField("Nashik Luggage", widget=NumberInput(), default=0)
    rokadi = IntegerField("Rokadi", widget=NumberInput(), default=0)
    return_ = IntegerField("Return", widget=NumberInput(), default=0)

    lab_payment = IntegerField("Lab Payment", widget=NumberInput(), default=0)
    difference = IntegerField("Difference", widget=NumberInput(), default=0)

    # Expenses
    advance = IntegerField("Advance", widget=NumberInput(), default=0)
    diesel = IntegerField("Diesel", widget=NumberInput(), default=0)
    other_expenses = IntegerField("Other Expenses", widget=NumberInput(), default=0)
    maintenance = IntegerField("Maintenance", widget=NumberInput(), default=0)
    chart_commission = IntegerField("Chart Commission", widget=NumberInput(), default=0)

    drivers_salary = IntegerField("Drivers Salary", widget=NumberInput(), default=0)
    cleaner_salary = IntegerField("Cleaner Salary", widget=NumberInput(), default=0)
    hinduza_finance = IntegerField("Hinduza Finance", widget=NumberInput(), default=0)
    road_tax = IntegerField("Road Tax", widget=NumberInput(), default=0)
    gprs = IntegerField("GPRS", widget=NumberInput(), default=0)
    bedsheet_washing = IntegerField("Bedsheet Washing", widget=NumberInput(), default=0)
    jay_ambe = IntegerField("Jay Ambe", widget=NumberInput(), default=0)
    pigmi = IntegerField("Pigmi", widget=NumberInput(), default=0)
    staff_payment = IntegerField("Staff Payment", widget=NumberInput(), default=0)

    submit = SubmitField("Add")
