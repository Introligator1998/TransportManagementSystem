from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from TMA.models import Uzytkownicy


# class SelectCar(FlaskForm):
#     id_car = StringField('ID samochodu', validators=[DataRequired()])
#     dateorder = StringField('Data zlecenia', validators=[DataRequired()])
# class CarPageDateTime(FlaskForm):

class OrdersForCars(FlaskForm):
    dateorder = StringField('Data')
    refresh = SubmitField('Odswiez')


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
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
    submit = SubmitField("Stwórz Użytkownika")

    def validate_username(self, username):
        user = Uzytkownicy.query.filter_by(login=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Uzytkownicy.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class AddNote(FlaskForm):
    tytul = StringField('Tytul notatki')
    tresc = StringField('Tresc notatki')
    add = SubmitField('Dodaj notatke')


class UpdateNote(FlaskForm):
    tytul = StringField('Tytul notatki')
    tresc = StringField('Tresc notatki')
    add = SubmitField('Zmień notatke')


class AddCar(FlaskForm):
    marka = StringField('Marka Samochodu')
    nazwa = StringField('Nazwa Samochodu')
    model = StringField('Model Samochodu')
    rejestracja = StringField('Numer Rejestracyjny Samochodu')
    przeglad = StringField('Termin następnego przeglądu')
    add = SubmitField('Dodaj Samochód')

class UpdateCar(FlaskForm):
    marka = StringField('Marka Samochodu')
    model = StringField('Model Samochodu')
    rejestracja = StringField('Numer Rejestracyjny Samochodu')
    nazwa = StringField('Nazwa Samochodu')
    przeglad = StringField('Termin następnego przeglądu')
    add = SubmitField('Dodaj Samochód')


class AddOrder(FlaskForm):
    order_id = StringField('ID zlecenia', validators=[DataRequired()])
    customer = StringField('Klient', validators= [DataRequired()])
    place = StringField('Adresy')
    price = StringField('Wartość zlecenia')
    customer_phone = StringField('Telefon do zleceniodawcy')
    date_from = StringField('Czas rozpoczęcia', validators = [DataRequired()])
    id_car = StringField('Dodaj Samochod', validators = [DataRequired()])
    notatka = TextAreaField('Opis')
    sub = SubmitField('Dodaj Zlecenie')


class UpdateOrder(FlaskForm):
    #order_id = StringField('ID zlecenia', validators=[DataRequired()])
    customer = StringField('Klient')
    place = StringField('Miejsce zlecenia')
    price = StringField('Wartość zlecenia')
    customer_phone = StringField('Telefon do zleceniodawcy')
    date_from = StringField('Czas rozpoczęcia')
    cars = StringField('Dodaj Samochod')
    # date_to = StringField('Czas zakończenia', validators=[DataRequired()])
    sub = SubmitField('Aktualizuj Zlecenie')
    notatka = TextAreaField('Opis')
class Date(FlaskForm):
    date = StringField("Wybierz datę", validators = [DataRequired()])
    date_sub = SubmitField('Zatwierdź')

class OrdersForCars(FlaskForm):
    dateorder = StringField("Wybierz datę", validators = [DataRequired()])
    sub = SubmitField('Zatwierdź')
