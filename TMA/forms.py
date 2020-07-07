from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from TMA.models import Uzytkownicy

class LoginForm(FlaskForm):
    login = StringField('Login',
                        validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Imię', validators=[DataRequired()])
    surname = StringField('Nazwisko', validators=[DataRequired()])
    login = StringField ('Login', validators=[DataRequired()])
    email = StringField ('Email', validators = [Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Powtórz hasło', validators=[DataRequired(), EqualTo('password')])
    permissions = RadioField('Uprawnienia', choices=[
        (1, 'Manager'), (2, 'Logistyk'), (3, 'Kierowca')],
                         default=1, coerce=int)
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Uzytkownicy.query.filter_by(login=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Uzytkownicy.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class AddCar(FlaskForm):
    marka = StringField('Marka Samochodu', validators = [DataRequired()])
    model = StringField('Model Samochodu', validators=[DataRequired()])
    rejestracja = StringField('Numer Rejestracyjny Samochodu', validators=[DataRequired()])
    add = SubmitField('Dodaj Samochód')
