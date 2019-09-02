from flask import render_template, flash, redirect, url_for, request
from kondor.forms import RegistrationForm, LoginForm, OrderForm, OrderCommentUpdateForm
from kondor.models import User, Order
from kondor import app, db, bcrypt
from flask_login import login_user, current_user, logout_user

posts = [
    {
        'author': 'Iryna',
        'comment': 'hey'
    },
    {
        'author': 'Yulia',
        'comment': 'whatsup'
    },

]

@app.route('/', methods=['GET', 'POST'])
def main():
    form = OrderForm()
    if form.is_submitted():
        order = Order(first_name=form.first_name.data, last_name=form.last_name.data, phone=form.phone.data, email=form.email.data, vin_code=form.vin_code.data, \
                        car_model=form.car_model.data, car_parts=form.car_parts.data, user_comment=form.user_comment.data)
        db.session.add(order)
        db.session.commit()
        flash('Заявка успішно відправлена! Очікуйте дзвінка протягом декількох годин', 'success')
        return redirect(url_for('main', _anchor='contact'))
    return render_template("index.html", form=form)

@app.route('/form_submit', methods=['GET', 'POST'])
def form_submit():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(first_name=form.first_name, last_name=form.last_name, phone=form.phone, email=form.email, vin_code=form.vin_code, \
                        car_model=form.car_model, car_parts=form.car_parts, user_comment=forms.user_comment)
        db.session.add(order)
        db.session.commit()
        flash('Заявка успішно відправлена! Очікуйте дзвінка протягом декількох годин')
    return redirect(url_for('main'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        orders = Order.query.all()
        return render_template("admin.html", orders=orders)

@app.route('/admin_profile')
def admin_profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template("admin_profile.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('admin'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/admin/<int:order_id>/update_comment', methods=['GET', 'POST'])
def update_comment(order_id):
    order = Order.query.get(order_id)
    form = OrderCommentUpdateForm()
    if form.validate_on_submit():
        order.admin_comment = form.admin_comment.data
        db.session.commit()
        flash("Коментар оновлено!", "success")
        return redirect(url_for('admin', order_id=order_id))
    elif request.method=='GET':
        form.admin_comment.data = order.admin_comment
    return redirect(url_for('modal', order_id=order_id, form=form))


@app.route('/admin#order<int:order_id>', methods=['GET', 'POST'])
def modal(order_id):
    orders = Order.query.all()
    form = OrderCommentUpdateForm()
    return render_template('admin.html', form=form, orders=orders)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))
