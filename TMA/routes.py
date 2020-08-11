import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from TMA import app, db, bcrypt
from TMA.forms import  LoginForm, RegisterForm, AddCar, AddOrder, UpdateOrder,UpdateCar, OrdersForCars, AddNote, UpdateNote
from TMA.models import Uzytkownicy, Uprawnienia, Samochody, Zlecenia, Notatki
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, DateField
from datetime import datetime, timedelta, date

from sqlalchemy import text, asc
db.create_all()


@app.route('/date')
def index():
    return render_template('datepicker.html')


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title = 'Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    #if current_user.is_authenticated:
     #   return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Uzytkownicy(name = form.name.data,surname = form.surname.data, login=form.login.data, password=hashed_password,id_upr=form.permissions.data)
        db.session.add(user)
        db.session.commit()
        flash('Twoje konto zostało stworzeone, teraz możesz się zalogować.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/addorder", methods=['GET', 'POST'])
def add_order():
    form = AddOrder()
    Order = Zlecenia.query.all()
    Cars = Samochody.query.all()

    if form.is_submitted():
        car_name = Samochody.query.filter_by(id_samochodu=form.id_car.data).first().nazwa

        date_time_obj = datetime.strptime(form.date_from.data, '%Y/%m/%d %H:%M')
        order = Zlecenia(miejsce=form.place.data, cena=form.price.data, zleceniodawca=form.customer.data,
                         telefon=form.customer_phone.data, czas_r=form.date_from.data, id_samochodu=form.id_car.data,notatka = form.notatka.data,
                         nazwa_samochodu=car_name)
        
        db.session.add(order)
        db.session.commit()
        flash('Zlecenie zostało dodane!', 'success')
        return redirect(url_for('add_order'))
    return render_template('addorder.html', title='Dodaj zlecenie', form = form, Order=Order, Cars = Cars)


@app.route("/car/<int:id_car>")
def car(id_car):
    Car = Samochody.query.get_or_404(id_car)
    return render_template('car.html', car = Car)


@app.route("/car/<int:id_car>/update", methods=['GET', 'POST'])
@login_required
def update_car(id_car):
    Car = Samochody.query.get_or_404(id_car)
    datecheck = datetime.now()

    form = UpdateCar()
    if form.validate_on_submit():
        #date_check = datetime.strptimetime(form.przeglad.data, '%Y-%m-%d')
        #date_check1 = datetime.strptime(form.polisa_data.data, '%Y-%m-%d')

        Car.marka = form.marka.data
        Car.wymiary = form.wymiary.data
        Car.nr_rej = form.rejestracja.data
        Car.polisa_data = form.polisa_data.data
        Car.polisa_nr = form.polisa_nr.data
        Car.leasing = form.leasing.data
        Car.nazwa = form.nazwa.data
        Car.data_przegladu = form.przeglad.data
        Car.pin = form.pin.data
        Car.rok = form.rok.data

        db.session.commit()
        flash('Pomyślnie zaktualizowano samochod', 'success')
        return redirect(url_for('car', id_car=Car.id_samochodu))
    elif request.method == 'GET':
        #date_check = datetime.strftime(Car.data_przegladu, '%Y-%m-%d')
        #date_check1 = datetime.strftime(Car.polisa_data, '%Y-%m-%d')

        form.marka.data = Car.marka
        form.wymiary.data = Car.wymiary
        form.rejestracja.data = Car.nr_rej
        #form.przeglad.data = date_check
        #form.polisa_nr.data = date_check1
        form.polisa_data.data = Car.polisa_data
        form.przeglad.data = Car.data_przegladu
        form.leasing.data = Car.leasing
        form.polisa_nr.data = Car.polisa_nr
        form.rok.data = Car.rok
        form.nazwa.data = Car.nazwa
        form.pin.data = Car.pin

    # elif request.method == 'GET':
    #     form.title.data = post.title
    #     form.content.data = post.content
    return render_template('updatecar.html', title='Update Car',
                            legend='Update Car',Car = Car, form = form, datecheck=datecheck)


@app.route("/car/<int:id_car>/delete", methods=['GET', 'POST'])
@login_required
def delete_car(id_car):
    Car = Samochody.query.get_or_404(id_car)
    db.session.delete(Car)
    db.session.commit()
    flash('Zlecenie zostało usunięte', 'success')
    return redirect(url_for('show_cars'))


@app.route("/showordersforcars", methods=['GET', 'POST'])
def show_orders_for_cars():
    form = OrdersForCars()

    min_car_id = int(request.form['page_number'])*3-2
    max_car_id = int(request.form['page_number'])*3

    datestart = datetime.strptime(request.form['dateorder'], '%Y-%m-%d')

    datefinish = datestart + timedelta(days=1)

    Cars = Samochody.query\
        .filter(Samochody.id_samochodu >= min_car_id)\
        .filter(Samochody.id_samochodu <=max_car_id)\
        .all()

    Orders = Zlecenia.query\
        .filter(Zlecenia.id_samochodu >= min_car_id)\
        .filter(Zlecenia.id_samochodu <= max_car_id)\
        .filter(Zlecenia.czas_r < datefinish)\
        .filter(Zlecenia.czas_r >= datestart)\
        .order_by(asc(Zlecenia.czas_r))\
        .all()

    return render_template('showordersforcars.html', Cars=Cars, Orders=Orders, form=form, datestart=datestart)


@app.route("/order/<int:id_order>")
def order(id_order):
    Order = Zlecenia.query.get_or_404(id_order)
    Cars = Samochody.query.all()
    return render_template('order.html', order = Order, cars = Cars)


@app.route("/order/<int:id_order>/update", methods=['GET', 'POST'])
@login_required
def update_order(id_order):
    Order = Zlecenia.query.get_or_404(id_order)
    Cars = Samochody.query.all()
    # if post.author != current_user:
    #     abort(403)
    form = UpdateOrder()
    czas_r = datetime.now()

    if form.validate_on_submit():
        czas_r = datetime.strptime(form.date_from.data, '%Y/%m/%d %H:%M')
        Order.zleceniodawca = form.customer.data
        Order.miejsce = form.place.data
        Order.czas_r = form.date_from.data
        Order.cena = form.price.data
        Order.notatka = form.notatka.data
        Order.telefon = form.customer_phone.data
        db.session.commit()
        flash('Zlecenie zostało zaktualizowane!', 'success')
        return redirect(url_for('order', id_order=Order.id_zlecenia))
    elif request.method == 'GET':
        form.customer.data = Order.zleceniodawca
        form.place.data = Order.miejsce
        czas_r = Order.czas_r
        form.price.data = Order.cena
        form.notatka.data = Order.notatka
        form.customer_phone.data = Order.telefon


    return render_template('updateorder.html', title='Update Order',
                            legend='Update Order',Order = Order,Cars = Cars, form = form, czas_r = czas_r)


@app.route("/order/<int:id_order>/delete", methods=['GET', 'POST'])
@login_required
def delete_order(id_order):
    Order = Zlecenia.query.get_or_404(id_order)
    db.session.delete(Order)
    db.session.commit()
    flash('Zlecenie zostało usunięte', 'success')
    return redirect(url_for('show_order'))


@app.route("/showorder", methods=['GET', 'POST'])
def show_order():
    Orders = Zlecenia.query.all()
    Car = Samochody.query.all()
    return render_template('showorder.html', Orders=Orders, Car = Car)


@app.route("/user/<int:id_user>")
def user(id_user):
    User = Uzytkownicy.query.get_or_404(id_user)
    return render_template('user.html', user = User)


@app.route("/user/<int:id_user>/delete", methods=['GET', 'POST'])
@login_required
def delete_user(id_user):
    User = Uzytkownicy.query.get_or_404(id_user)
    db.session.delete(User)
    db.session.commit()
    flash('Zlecenie zostało usunięte', 'success')
    return redirect(url_for('show_users'))


@app.route("/showcarorder", methods=['GET', 'POST'])
def show_car_order():
    id_car = request.form['id_car']
    dateorder_with_time = request.form['dateorder']
    dateorder = datetime.strptime(dateorder_with_time, '%Y-%m-%d')
    datefinish = dateorder + timedelta(days=1)

    Orders = Zlecenia.query\
        .filter_by(id_samochodu=id_car)\
        .filter(Zlecenia.czas_r < datefinish)\
        .filter(Zlecenia.czas_r >= dateorder)\
        .all()

    return render_template('showorder.html', Orders = Orders)


def split_list(domain, interval):
    return [domain[i:i + interval] for i in range(0, len(domain), interval)]


@app.route("/showlogisticcars", methods=['GET', 'POST'])
def show_logistic_cars():
    Cars = Samochody.query.all()
    car_pages_split = split_list(Cars, 3)
    car_names = list()

    for page in car_pages_split:
        page_car_names = '/'.join([car.nazwa for car in page])
        car_names.append(page_car_names)

    return render_template('logisticcars.html', car_names=car_names)


@app.route("/showcars", methods=['GET', 'POST'])
def show_cars():
    Cars = Samochody.query.all()
    if current_user.id_upr == 3:
        return render_template('drivercars.html', Cars=Cars)
    else:
        return render_template('showcars.html', Cars = Cars)


@app.route("/showusers", methods=['GET', 'POST'])
def show_users():
    Users = Uzytkownicy.query.all()
    return render_template('users.html', Users = Users)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
       return redirect(url_for('home'))
    form = LoginForm()
    if form.is_submitted():
        user = Uzytkownicy.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if current_user.id_upr == 3:
                return redirect('showcars')
            else:
                return redirect('home')
        else:
            flash('Login Nieudane. Sprawdź poprawność loginu i hasła', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/addcar", methods=['GET', 'POST'])
def add_car():
    form = AddCar()
    if form.validate_on_submit():
        car = Samochody(marka = form.marka.data, nazwa = form.nazwa.data, nr_rej=form.rejestracja.data,rok = form.rok.data,leasing = form.leasing.data,wymiary= form.wymiary.data, polisa_nr = form.polisa_nr.data, polisa_data = form.polisa_data.data, pin = form.pin.data, data_przegladu = form.przeglad.data)
        db.session.add(car)
        db.session.commit()
        flash('Samochód został dodany!', 'success')
        return redirect(url_for('login'))
    return render_template('addcar.html', form = form)


@app.route("/addnote", methods=['GET', 'POST'])
def add_note():
    form = AddNote()
    if form.validate_on_submit():
        note = Notatki(tytul=form.tytul.data, tresc=form.tresc.data)
        db.session.add(note)
        db.session.commit()
        flash('Dodano notatkę!', 'success')
        return redirect(url_for('login'))
    return render_template('addnote.html', form=form)


@app.route("/shownotes", methods=['GET', 'POST'])
def show_notes():
    notes = Notatki.query.all()
    return render_template('shownotes.html', notes=notes)


@app.route("/note/<int:id_note>")
def note(id_note):
    note = Notatki.query.get_or_404(id_note)

    return render_template('note.html', note=note)


@app.route("/note/<int:id_note>/update", methods=['GET', 'POST'])
@login_required
def update_note(id_note):
    note = Notatki.query.get_or_404(id_note)
    form = UpdateNote()

    if form.validate_on_submit():
        note.tytul = form.tytul.data
        note.tresc = form.tresc.data
        db.session.commit()
        flash('Notatka została zaktualizowana!', 'success')
        return redirect(url_for('note', id_note=note.id_notatki))
    elif request.method == 'GET':
        form.tytul.data = note.tytul
        form.tresc.data = note.tresc

    return render_template('updatenote.html', title='Update Note', legend='Update Note',note=note, form = form)


@app.route("/note/<int:id_note>/delete", methods=['GET', 'POST'])
@login_required
def delete_note(id_note):
    note = Notatki.query.get_or_404(id_note)
    db.session.delete(note)
    db.session.commit()
    flash('Notatka została usunięta', 'success')
    return redirect(url_for('show_notes'))