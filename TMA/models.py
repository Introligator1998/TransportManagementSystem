from datetime import datetime
from TMA import db, app, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Uzytkownicy.query.get(int(user_id))


class Uprawnienia(db.Model):
    __tablename__ = 'uprawnienia'
    id_uprawnien = db.Column(db.Integer, primary_key=True)
    nazwa_uprawnien = db.Column(db.String(50), nullable=False)
    users = db.relationship('Uzytkownicy', backref='user')

    def __repr__(self):
        return f"Uprawnienia('{self.id_uprawnien}', '{self.nazwa_uprawnien}')"


class Samochody(db.Model):
    __tablename__ = 'samochody'
    id_samochodu = db.Column(db.Integer, primary_key = True)
    marka = db.Column(db.String(50))
    nazwa = db.Column(db.String(50))
    model = db.Column(db.String(50))
    nr_rej = db.Column(db.String(12))
    data_przegladu = db.Column(db.String(25))


class Zlecenia (db.Model):
    __tablename__ = 'zlecenia'
    id_zlecenia = db.Column(db.Integer, primary_key = True)
    miejsce = db.Column(db.String(150))
    czas_r = db.Column(db.DateTime, nullable = False)
    cena = db.Column(db.String(30))
    zleceniodawca = db.Column(db.String(50))
    telefon = db.Column(db.String(15))
    id_samochodu = db.Column(db.Integer, db.ForeignKey('samochody.id_samochodu'),nullable=False)
    nazwa_samochodu = db.Column(db.String(50), db.ForeignKey('samochody.nazwa'), nullable=False)
    notatka = db.Column(db.String(500))


class Notatki(db.Model):
    __tablename__ = "notatki"
    id_notatki = db.Column(db.Integer, primary_key=True)
    tytul = db.Column(db.String(30))
    tresc = db.Column(db.String(500))


class Uzytkownicy(db.Model, UserMixin):
    __tablename__ = 'uzytkownicy'
    id_uzytkownika = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=True)
    id_upr = db.Column(db.Integer, db.ForeignKey('uprawnienia.id_uprawnien'),nullable=False)

    def get_id(self):
        return (self.id_uzytkownika)


    def __repr__(self):
        return f"Uzytkownicy('{self.id_uzytkownika}', '{self.imie}','{self.nazwisko}','{self.login}','{self.haslo}')"

