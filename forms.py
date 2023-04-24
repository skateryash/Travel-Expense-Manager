from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, widgets, DateField, IntegerField, validators, BooleanField
from wtforms.validators import DataRequired, URL
from wtforms.widgets.html5 import NumberInput
from wtforms.fields.html5 import DateField, TimeField


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
    date = DateField('Start Date',  validators=(validators.Optional(),))
    jalgaon_memo = IntegerField("Jalgaon Memo", widget=NumberInput())
    jalgaon_luggage = IntegerField("Jalgaon luggage", widget=NumberInput())
    dhule_memo = IntegerField("Dhule Memo", widget=NumberInput())
    manmohan_memo = IntegerField("Manmohan Memo", widget=NumberInput())
    nashik_luggage = IntegerField("Nashik luggage", widget=NumberInput())
    rokadi = IntegerField("Rokadi", widget=NumberInput())
    return_ = IntegerField("Return", widget=NumberInput())
    advance = IntegerField("Advance", widget=NumberInput())
    disel = IntegerField("Disel", widget=NumberInput())
    other_expenses = IntegerField("Other Expenses", widget=NumberInput())
    maintenance = IntegerField("Maintenance", widget=NumberInput())
    chart_comission = IntegerField("Chart Comission", widget=NumberInput())
    submit = SubmitField("Add")


