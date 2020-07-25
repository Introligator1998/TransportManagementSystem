import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from TMA import app, db, bcrypt
from TMA.forms import  LoginForm, RegisterForm, AddCar, AddOrder
from TMA.models import Uzytkownicy, Uprawnienia, Samochody, Zlecenia, ZleceniaSamochody
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, DateField
from datetime import datetime

from sqlalchemy import text
db.create_all()

class MyForm(FlaskForm):
    date = DateField(id='datepick')

@app.route('/date')
def index():
    form = MyForm()
    return render_template('datepicker.html', form=form)
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title = 'Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Uzytkownicy(name = form.name.data,surname = form.surname.data, login=form.login.data, email=form.email.data, password=hashed_password,id_upr=form.permissions.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/addorder", methods=['GET', 'POST'])
def add_order():
    form = AddOrder()
    Order = Zlecenia.query.all()
    Cars = Samochody.query.all()
    if form.is_submitted():
        date_time_obj = datetime.strptime(form.date_from.data, '%Y/%m/%d %H:%M')

        order = Zlecenia(miejsce=form.place.data, cena=form.price.data, zleceniodawca=form.customer.data,
                         telefon=form.customer_phone.data, czas_r=date_time_obj, id_samochodu=form.id_car.data)
        # TODO zapisywanie relacji samochod-zlecenie
        db.session.add(order)
        db.session.commit()
        flash('Zlecenie zostało dodane!', 'success')
        return redirect(url_for('add_order'))
    return render_template('addorder.html', title='Dodaj zlecenie', form = form, Order=Order, Cars = Cars)


@app.route("/showorder", methods=['GET', 'POST'])
def show_order():
    Orders = Zlecenia.query.all()
    return render_template('showorder.html', Orders=Orders)

# TODO
@app.route("/showcarorder", methods=['GET', 'POST'])
def show_car_order():
    id_car = request.form['id_car']
    dateorder_with_time = request.form['dateorder']
    dateorder = datetime.strptime(dateorder_with_time, '%Y/%m/%d %H:%M')

    # Cars = Samochody.query.all()
    print(id_car)
    Orders = Zlecenia.query.filter(id_samochodu=id_car)

    print(Orders)
    # sql = text(f"SELECT * FROM Zlecenia WHERE id_samochodu={id_car}")
    # result = db.engine.execute(sql)
    # print(result)
    # print(type(result))
    # Orders = [row[0] for row in result]
    # print(Orders)
    #
    # for order in Orders:
    #     print("order:")
    #     print(order)
    # car_orders = Orders.query.filter_by(id_car=id_car)
    # Orders = Zlecenia.query.filter(Zlecenia.id_samochodu == id_car).all()
    # print(Orders)
    # Orders = Zlecenia.query.filter_by(id_samochodu=id_car).first()
    # print(Orders)
    # Orders = Zlecenia.query.filter(Zlecenia.czas_r == dateorder).filter(Zlecenia.id_samochodu == id_car)
    # print(car_orders.czas_r)
    # filtered_orders = car_orders.query.filter(car_orders.czas_r == dateorder)

    return render_template('showorder.html', Orders = Orders)

@app.route("/showcars", methods=['GET', 'POST'])
def show_cars():
    Cars = Samochody.query.all()
    return render_template('showcars.html', Cars = Cars)


@app.route("/showordersforcar", methods=['GET', 'POST|'])
def show_orders_for_car():
    pass
    # TODO zlecenia dla samochodu
    # Orders = Zlecenia.query.filter_by(ZleceniaSamochody)
    # return render_template('showorder.html', Orders = Orders)


#@app.route("/saveorder", methods=['POST'])
#def save_order():
    # date_from =request.form['datepicker_from']
    # date_to =request.form['datepicker_to']
    # print(date_from)

    # return redirect('/')



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
       return redirect(url_for('home'))
    form = LoginForm()
    if form.is_submitted():
        user = Uzytkownicy.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if current_user.id_upr == 1:
                return redirect('showcars')
            # TODO na podstawie uprawnień
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


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


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


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
'''