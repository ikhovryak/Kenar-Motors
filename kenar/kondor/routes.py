from flask import render_template, flash, redirect, url_for, request
from kondor.forms import RegistrationForm, LoginForm, OrderForm, OrderCommentUpdateForm
from kondor.models import User, Order
from kondor import app, db, bcrypt
from flask_login import login_user, current_user, logout_user
from sqlalchemy import desc

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
        orders = Order.query.order_by(desc(Order.date_posted)).all()
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
        return redirect(url_for('order', order_id=order_id))
    elif request.method=='GET':
        form.admin_comment.data = order.admin_comment
    return render_template('order.html', order_id=order_id, form=form, order=order)


@app.route('/admin/<int:order_id>', methods=['GET', 'POST'])
def order(order_id):
    order = Order.query.get(order_id)
    order.is_read = True
    db.session.commit()
    return render_template('order.html', order=order)

@app.route('/admin/<int:order_id>/delete', methods=['GET', 'POST'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Замовлення видалено!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/<int:order_id>/mark_undone')
def mark_undone(order_id):
    order = Order.query.get(order_id)
    order.is_completed = False
    db.session.commit()
    return redirect(url_for('order', order_id=order_id))

@app.route('/admin/<int:order_id>/mark_done')
def mark_done(order_id):
    order = Order.query.get(order_id)
    order.is_completed = True
    db.session.commit()
    return redirect(url_for('order', order_id=order_id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))
