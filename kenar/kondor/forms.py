from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from kondor.models import User
from wtforms.fields.html5 import EmailField

class RegistrationForm(FlaskForm):
    username = StringField("Логін", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Електронна пошта", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    confirm_password = PasswordField("Підтвердіть пароль", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Зареєструватись")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Цей логін уже зайнятий. Будь ласка, виберіть інший')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Аккаунт з цією електронною поштою уже існує')

class LoginForm(FlaskForm):
    email = StringField("Електронна пошта", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Увійти")


class OrderForm(FlaskForm):
    first_name = StringField("Ім'я", validators=[DataRequired(), Length(min=1, max=30)], description="Ім'я")
    last_name = StringField("Прізвище", validators=[DataRequired(), Length(min=1, max=30)], description="Прізвище")
    phone = StringField("Телефон", validators=[DataRequired(), Length(min=1, max=20)], description="Телефон")
    email = EmailField("Електронна пошта", validators=[ Length(min=1, max=120), Email()], description="Електронна пошта")
    vin_code = StringField("VIN-код машини", validators=[DataRequired(), Length(min=1, max=30)], description="VIN-код машини")
    car_model = StringField("Марка та модель машини", validators=[Length(min=1, max=200)], description="Марка та модель машини")
    car_parts = TextAreaField("Запчастини, які Вас цікавлять", validators=[DataRequired()], description="Запчастини, які Вас цікавлять", render_kw={"rows": 70, "cols": 11})
    user_comment = TextAreaField("Додаткові коментарі", description="Додаткові коментарі", render_kw={"rows": 70, "cols": 11})
    submit = SubmitField("Відправити")

class OrderCommentUpdateForm(FlaskForm):
    admin_comment = TextAreaField("Коментар адміністратора", description="Коментар адміністратора")
    submit = SubmitField("Зберегти")

class OrderUpdateForm(FlaskForm):
    first_name = StringField("Ім'я", validators=[DataRequired(), Length(min=1, max=30)], description="Ім'я")
    last_name = StringField("Прізвище", validators=[DataRequired(), Length(min=1, max=30)], description="Прізвище")
    phone = StringField("Телефон", validators=[DataRequired(), Length(min=1, max=20)], description="Телефон")
    email = EmailField("Електронна пошта", validators=[ Length(min=1, max=120), Email()], description="Електронна пошта")
    vin_code = StringField("VIN-код машини", validators=[DataRequired(), Length(min=1, max=30)], description="VIN-код машини")
    address = StringField("Адрес клієнта", validators=[DataRequired(), Length(min=0, max=50)], description="Адрес клієнта")
    car_model = TextAreaField("Марка та модель машини", validators=[Length(min=1, max=200)], description="Марка та модель машини")
    car_parts = TextAreaField("Запчастини, які Вас цікавлять", validators=[DataRequired()], description="Запчастини, які Вас цікавлять")
    user_comment = TextAreaField("Додаткові коментарі", description="Додаткові коментарі")
    admin_comment = TextAreaField("Коментар адміністратора", description="Коментар адміністратора")
    submit = SubmitField("Зберегти")
