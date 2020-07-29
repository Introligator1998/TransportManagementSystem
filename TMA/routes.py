import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from TMA import app, db, bcrypt
from TMA.forms import  LoginForm, RegisterForm, AddCar, AddOrder, UpdateOrder,UpdateCar
from TMA.models import Uzytkownicy, Uprawnienia, Samochody, Zlecenia, ZleceniaSamochody
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, DateField
from datetime import datetime, timedelta

from sqlalchemy import text
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
        user = Uzytkownicy(name = form.name.data,surname = form.surname.data, login=form.login.data, email=form.email.data, password=hashed_password,id_upr=form.permissions.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/addorder", methods=['GET', 'POST'])
def add_order():
    form = AddOrder()
    Order = Zlecenia.query.all()
    Cars = Samochody.query.all()
    print(Cars)
    if form.is_submitted():
        car_name = Samochody.query.filter_by(id_samochodu=form.id_car.data).first().nazwa
        print(car_name)
        date_time_obj = datetime.strptime(form.date_from.data, '%Y/%m/%d %H:%M')
        order = Zlecenia(miejsce=form.place.data, cena=form.price.data, zleceniodawca=form.customer.data,
                         telefon=form.customer_phone.data, czas_r=date_time_obj, id_samochodu=form.id_car.data,notatka = form.notatka.data,
                         nazwa_samochodu=car_name)
        # TODO zapisywanie relacji samochod-zlecenie
        db.session.add(order)
        db.session.commit()
        flash('Zlecenie zostało dodane!', 'success')
        return redirect(url_for('add_order'))
    return render_template('addorder.html', title='Dodaj zlecenie', form = form, Order=Order, Cars = Cars)

@app.route("/car/<int:id_car>")
def car(id_car):
    Car = Samochody.query.get_or_404(id_car)
    return render_template('car.html', car = Car)


@app.route("/showordersforcars/<int:cars_orders_page>", methods=['GET', 'POST'])
def show_orders_for_cars(cars_orders_page):
    min_car_id = cars_orders_page*3-2
    max_car_id = cars_orders_page*3

    Cars = Samochody.query\
        .filter(Samochody.id_samochodu >= min_car_id)\
        .filter(Samochody.id_samochodu <=max_car_id)\
        .all()

    return render_template('showordersforcars.html', Cars=Cars)


@app.route("/car/<int:id_car>/update", methods=['GET', 'POST'])
@login_required
def update_car(id_car):
    Car = Samochody.query.get_or_404(id_car)
    # if post.author != current_user:
    #     abort(403)
    form = UpdateCar()
    if form.validate_on_submit():
        Car.marka = form.marka.data
        Car.model = form.model.data
        Car.nr_rej = form.rejestracja.data
        Car.data_przegladu = form.przeglad.data
        Car.nazwa = form.nazwa.data
        db.session.commit()
        flash('Pomyślnie zaktualizowano samochod', 'success')
        return redirect(url_for('car', id_car=Car.id_samochodu))
    # elif request.method == 'GET':
    #     form.title.data = post.title
    #     form.content.data = post.content
    return render_template('updatecar.html', title='Update Car',
                            legend='Update Car',Car = Car, form = form)

@app.route("/car/<int:id_car>/delete", methods=['GET', 'POST'])
@login_required
def delete_car(id_car):
    Car = Samochody.query.get_or_404(id_car)
    db.session.delete(Car)
    db.session.commit()
    flash('Zlecenie zostało usunięte', 'success')
    return redirect(url_for('show_cars'))

@app.route("/order/<int:id_order>")
def order(id_order):
    Order = Zlecenia.query.get_or_404(id_order)
    Cars = Samochody.query.all();
    return render_template('order.html', order = Order, cars = Cars)

@app.route("/order/<int:id_order>/update", methods=['GET', 'POST'])
@login_required
def update_order(id_order):
    Order = Zlecenia.query.get_or_404(id_order)
    Cars = Samochody.query.all()
    # if post.author != current_user:
    #     abort(403)
    form = UpdateOrder()
    if form.validate_on_submit():
        Order.zleceniodawca = form.customer.data
        Order.miejsce = form.place.data
        Order.czar_r = form.date_from.data
        Order.cena = form.price.data
        Order.notatka = form.notatka.data
        Order.telefon = form.customer_phone.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('order', id_order=Order.id_zlecenia))
    # elif request.method == 'GET':
    #     form.title.data = post.title
    #     form.content.data = post.content
    return render_template('updateorder.html', title='Update Order',
                            legend='Update Order',Order = Order,Cars = Cars, form = form)

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

# TODO
@app.route("/showcarorder", methods=['GET', 'POST'])
def show_car_order():
    id_car = request.form['id_car']
    dateorder_with_time = request.form['dateorder']
    dateorder = datetime.strptime(dateorder_with_time, '%Y-%m-%d')
    datefinish = dateorder + timedelta(days=1)

    Orders = Zlecenia.query.filter_by(id_samochodu=id_car).filter(Zlecenia.czas_r < datefinish).filter(Zlecenia.czas_r >= dateorder).all()

    return render_template('showorder.html', Orders = Orders)


@app.route("/showcars", methods=['GET', 'POST'])
def show_cars():
    Cars = Samochody.query.all()
    if current_user.id_upr == 3:
        return render_template('drivercars.html', Cars=Cars)
    else:
        return render_template('showcars.html', Cars = Cars)


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
        car = Samochody(marka = form.marka.data, nazwa = form.nazwa.data, model = form.model.data, nr_rej=form.rejestracja.data, data_przegladu = form.przeglad.data)
        db.session.add(car)
        db.session.commit()
        flash('Samochód został dodany!', 'success')
        return redirect(url_for('login'))
    return render_template('addcar.html', form = form)
'''
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')



'''