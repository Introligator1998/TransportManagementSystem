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
    marka = db.Column(db.String(50), nullable = False)
    model = db.Column(db.String(50), nullable = False)
    nr_rej = db.Column(db.String(12), nullable = False, unique = True)
    data_przegladu = db.Column(db.Date, nullable = True)
    db.relationship('ZleceniaSamochody', backref = 'zs')


class Zlecenia (db.Model):
    __tablename__ = 'zlecenia'
    id_zlecenia = db.Column(db.Integer, primary_key = True)
    miejsce = db.Column(db.String(50), nullable = False)
    data = db.Column(db.Date, nullable = False)
    godzina_r = db.Column(db.Time, nullable = False)
    godzina_z = db.Column(db.Time)
    cena = db.Column(db.Float)
    nazwa = db.Column(db.String(50),nullable = False)
    db.relationship('ZleceniaSamochody', backref='zle')



class Uzytkownicy(db.Model, UserMixin):
    __tablename__ = 'uzytkownicy'
    id_uzytkownika = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=True)
    id_upr = db.Column(db.Integer, db.ForeignKey('uprawnienia.id_uprawnien'),nullable=False)
    db.relationship('ZleceniaSamochody', backref='zled')

    def get_id(self):
        return (self.id_uzytkownika)


    def __repr__(self):
        return f"Uzytkownicy('{self.id_uzytkownika}', '{self.imie}','{self.nazwisko}','{self.login}','{self.haslo}')"


class ZleceniaSamochody (db.Model):
    __tablename__ = 'zleceniasamochody'
    id_zs = db.Column(db.Integer, primary_key = True)
    id_samochodu = db.Column(db.Integer, db.ForeignKey('samochody.id_samochodu'), nullable = False)
    id_zlecenia = db.Column(db.Integer, db.ForeignKey('zlecenia.id_zlecenia'), nullable = False)
    id_uzytkownika = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id_uzytkownika'), nullable = False)
