from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, SelectMultipleField, SelectField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
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
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Zaloguj')


class RegisterForm(FlaskForm):
    name = StringField('Imię')
    surname = StringField('Nazwisko')
    login = StringField ('Login', validators=[DataRequired()])
    #email = StringField ('Email',validator = [Email])
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
    tresc = TextAreaField('Tresc notatki')
    add = SubmitField('Dodaj notatke')


class UpdateNote(FlaskForm):
    tytul = StringField('Tytul notatki')
    tresc = TextAreaField('Tresc notatki')
    add = SubmitField('Zmień notatke')


class AddCar(FlaskForm):
    marka = StringField('Marka i model samochodu')
    nazwa = StringField('Nazwa samochodu')
    wymiary = StringField('Typ i wymiary samochodu')
    rejestracja = StringField('Numer Rejestracyjny Samochodu')
    rok = StringField('Rok produkcji')
    leasing = StringField('Leasing')
    polisa_nr = StringField('Numer polisy')
    polisa_data = StringField('Data ważności polisy')
    pin = StringField('PIN do karty')
    przeglad = StringField('Termin następnego przeglądu')
    add = SubmitField('Dodaj Samochód')

class UpdateCar(FlaskForm):
    marka = StringField('Marka i model samochodu')
    nazwa = StringField('Nazwa samochodu')
    wymiary = StringField('Typ i wymiary samochodu')
    rejestracja = StringField('Numer Rejestracyjny Samochodu')
    rok = StringField('Rok produkcji')
    leasing = StringField('Leasing')
    polisa_nr = StringField('Numer polisy')
    polisa_data = StringField('Data ważności polisy')
    pin = StringField('PIN do karty')
    przeglad = StringField('Termin następnego przeglądu')
    add = SubmitField('Zmień')

class AddOrder(FlaskForm):

    order_id = StringField('ID zlecenia', validators=[DataRequired()])
    customer = StringField('Klient', validators= [DataRequired()])
    city = StringField('Miasto',validators= [DataRequired()])
    place = StringField('Adresy')
    price = StringField('Wartość zlecenia')
    customer_phone = StringField('Telefon do zleceniodawcy')
    date_from = StringField('Czas rozpoczęcia', validators = [DataRequired()])
    id_car = StringField('Dodaj Samochod', validators = [DataRequired()])
    notatka = TextAreaField('Opis')
    sub = SubmitField('Dodaj Zlecenie')
    info = SelectField(u'Skąd się o nas dowiedziałeś ?',choices=[('1', 'Wyszukanie w Google'), ('2', 'Wizytówka Google'), ('3', 'Olx'), ('4', 'Gumtree'), ('5', 'Fixly'), ('6', 'Polecenie'), ('7', 'Stały klient'), ('8', 'Ulotka'),('9', 'Inne')])
    author = StringField('Zlecenie dodał:', validators = [DataRequired()])

class UpdateOrder(FlaskForm):

    #order_id = StringField('ID zlecenia', validators=[DataRequired()])
    customer = StringField('Klient',validators= [DataRequired()])
    miasto = StringField('Miasto',validators= [DataRequired()])
    city = StringField('Miejsce zlecenia')
    price = StringField('Wartość zlecenia')
    customer_phone = StringField('Telefon do zleceniodawcy')
    date_from = StringField('Czas rozpoczęcia')
    cars = StringField('Dodaj Samochod')
    # date_to = StringField('Czas zakończenia', validators=[DataRequired()])
    sub = SubmitField('Aktualizuj Zlecenie')
    notatka = TextAreaField('Opis')
    info = SelectField(u'Skąd się o nas dowiedziałeś ?', choices=[('1', 'Wyszukanie w Google'), ('2', 'Wizytówka Google'), ('3', 'Olx'), ('4', 'Gumtree'), ('5', 'Fixly'), ('6', 'Polecenie'), ('7', 'Stały klient'), ('8', 'Ulotka'), ('9', 'Inne')])
    author = StringField('Zlecenie dodał:', validators = [DataRequired()])

class Date(FlaskForm):

    date = StringField("Wybierz datę", validators = [DataRequired()])
    date_sub = SubmitField('Zatwierdź')

class OrdersForCars(FlaskForm):
    dateorder = StringField("Wybierz datę", validators = [DataRequired()])
    sub = SubmitField('Zatwierdź')

class UpdateUserForm(FlaskForm):

    name = StringField('Imię')
    surname = StringField('Nazwisko')
    login = StringField ('Login', validators=[DataRequired()])
    #email = StringField ('Email',validator = [Email])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Powtórz hasło', validators=[DataRequired(), EqualTo('password')])
    permissions = RadioField('Uprawnienia', choices=[
        (1, 'Manager'), (2, 'Logistyk'), (3, 'Kierowca')],
                         default=1, coerce=int)
    submit = SubmitField("Stwórz Użytkownika")

